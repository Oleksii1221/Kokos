from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction, ChatMemberStatus, ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, ChatMemberUpdated

from app.config import get_settings
from app.db import Database
from app.downloader import DownloadError, cleanup_download, download_video
from app.url_parser import detect_platform, extract_supported_urls


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("kokos.bot")

settings = get_settings()
db = Database(settings.database_url)
dp = Dispatcher()
download_semaphore = asyncio.Semaphore(settings.max_parallel_downloads)
downloads_dir = Path("downloads")


@dp.message(Command("start"))
async def start(message: Message) -> None:
    await db.mark_started(message.from_user)
    await db.upsert_chat(message.chat)
    if settings.bot_maintenance:
        await message.answer("KokoClip зараз на технічній перерві. Я повернусь трохи пізніше.")
        return
    await message.answer(
        "Привіт. Кидай TikTok або YouTube Shorts, а я відповім самим відео.\n\n"
        "У групах мені треба бачити повідомлення, тому privacy mode має бути вимкнений у BotFather."
    )


@dp.message(Command("stats"))
async def stats(message: Message) -> None:
    await db.record_activity(message.from_user, message.chat)
    if not settings.public_stats and message.from_user and message.from_user.id != settings.owner_id:
        await message.answer("Публічна статистика вимкнена.")
        return

    data = await db.public_stats()
    await message.answer(
        "Статистика KokoClip\n"
        f"Користувачів: {data.get('total_users', 0)}\n"
        f"Активували /start: {data.get('started_users', 0)}\n"
        f"Активних за 30 днів: {data.get('active_users_30d', 0)}\n"
        f"Активних чатів: {data.get('active_chats', 0)}\n"
        f"Відео відправлено: {data.get('successful_videos', 0)}\n"
        f"Посилань оброблено: {data.get('total_links', 0)}"
    )


@dp.message(Command("admin_stats"))
async def admin_stats(message: Message) -> None:
    await db.record_activity(message.from_user, message.chat)
    if not message.from_user or message.from_user.id != settings.owner_id:
        await message.answer("Ця команда доступна тільки власнику.")
        return
    data = await db.public_stats()
    await message.answer(f"<pre>{data}</pre>", parse_mode=ParseMode.HTML)


@dp.message(Command("health"))
async def health(message: Message) -> None:
    await db.record_activity(message.from_user, message.chat)
    mode = "maintenance" if settings.bot_maintenance else "active"
    await message.answer(f"KokoClip online. Mode: {mode}.")


@dp.my_chat_member()
async def bot_chat_member(update: ChatMemberUpdated) -> None:
    active = update.new_chat_member.status not in {ChatMemberStatus.KICKED, ChatMemberStatus.LEFT}
    await db.upsert_chat(update.chat, is_active=active)
    log.info("Bot chat status changed: chat_id=%s active=%s", update.chat.id, active)


@dp.message(F.text | F.caption)
async def handle_message(message: Message, bot: Bot) -> None:
    await db.record_activity(message.from_user, message.chat)

    text = message.text or message.caption
    urls = extract_supported_urls(text)
    if not urls:
        return

    if settings.bot_maintenance:
        await message.reply("Зараз технічна перерва. Посилання побачив, але відео поки не обробляю.")
        return

    for url in urls[:3]:
        await process_url(message, bot, url)


async def process_url(message: Message, bot: Bot, url: str) -> None:
    platform = detect_platform(url)
    user_id = message.from_user.id if message.from_user else None
    chat_id = message.chat.id if message.chat else None
    status_message = await message.reply("Завантажую відео...")

    try:
        cached_file_id = await db.get_cached_video(url)
        if cached_file_id:
            sent = await message.reply_video(cached_file_id)
            await db.add_link_event(user_id, chat_id, url, platform, "success")
            await status_message.delete()
            log.info("Sent cached video: chat_id=%s url=%s message_id=%s", chat_id, url, sent.message_id)
            return

        async with download_semaphore:
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            video_path = await download_video(
                url=url,
                downloads_dir=downloads_dir,
                max_video_mb=settings.max_video_mb,
                timeout=settings.download_timeout_seconds,
            )

        try:
            sent = await message.reply_video(FSInputFile(video_path))
            if sent.video:
                await db.save_cached_video(url, platform, sent.video.file_id, sent.video.file_unique_id)
            await db.add_link_event(user_id, chat_id, url, platform, "success")
            await status_message.delete()
            log.info("Sent new video: chat_id=%s url=%s", chat_id, url)
        finally:
            cleanup_download(video_path)

    except DownloadError as exc:
        await db.add_link_event(user_id, chat_id, url, platform, "failed", str(exc))
        await status_message.edit_text("Не зміг дістати відео з цього посилання.")
        log.warning("Download failed: url=%s error=%s", url, exc)
    except Exception as exc:
        await db.add_link_event(user_id, chat_id, url, platform, "failed", str(exc))
        await status_message.edit_text("Сталася помилка під час обробки відео.")
        log.exception("Unexpected error while processing url=%s", url)


async def main() -> None:
    downloads_dir.mkdir(exist_ok=True)
    await db.connect()
    bot = Bot(token=settings.bot_token)
    log.info("KokoClip bot started. maintenance=%s", settings.bot_maintenance)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
