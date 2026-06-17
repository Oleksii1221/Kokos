from __future__ import annotations

import asyncpg


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    is_bot BOOLEAN NOT NULL DEFAULT FALSE,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    start_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS chats (
    chat_id BIGINT PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT,
    username TEXT,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS user_chat_activity (
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    chat_id BIGINT NOT NULL REFERENCES chats(chat_id) ON DELETE CASCADE,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, chat_id)
);

CREATE TABLE IF NOT EXISTS link_events (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    chat_id BIGINT REFERENCES chats(chat_id) ON DELETE SET NULL,
    url TEXT NOT NULL,
    platform TEXT NOT NULL,
    status TEXT NOT NULL,
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cached_videos (
    url TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    telegram_file_id TEXT NOT NULL,
    file_unique_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_used_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    use_count BIGINT NOT NULL DEFAULT 1
);
"""


class Database:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(self._dsn, min_size=1, max_size=10)
        async with self.pool.acquire() as conn:
            await conn.execute(SCHEMA)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    async def upsert_user(self, user) -> None:
        if not user or not self.pool:
            return
        await self.pool.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name, language_code, is_bot)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                language_code = EXCLUDED.language_code,
                is_bot = EXCLUDED.is_bot,
                last_seen_at = now()
            """,
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code,
            user.is_bot,
        )

    async def mark_started(self, user) -> None:
        if not user or not self.pool:
            return
        await self.upsert_user(user)
        await self.pool.execute(
            "UPDATE users SET start_count = start_count + 1, last_seen_at = now() WHERE user_id = $1",
            user.id,
        )

    async def upsert_chat(self, chat, is_active: bool = True) -> None:
        if not chat or not self.pool:
            return
        await self.pool.execute(
            """
            INSERT INTO chats (chat_id, type, title, username, is_active)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (chat_id) DO UPDATE SET
                type = EXCLUDED.type,
                title = EXCLUDED.title,
                username = EXCLUDED.username,
                is_active = EXCLUDED.is_active,
                last_seen_at = now()
            """,
            chat.id,
            chat.type,
            getattr(chat, "title", None),
            getattr(chat, "username", None),
            is_active,
        )

    async def record_activity(self, user, chat) -> None:
        if not user or not chat or not self.pool:
            return
        await self.upsert_user(user)
        await self.upsert_chat(chat)
        await self.pool.execute(
            """
            INSERT INTO user_chat_activity (user_id, chat_id, message_count)
            VALUES ($1, $2, 1)
            ON CONFLICT (user_id, chat_id) DO UPDATE SET
                last_seen_at = now(),
                message_count = user_chat_activity.message_count + 1
            """,
            user.id,
            chat.id,
        )

    async def add_link_event(self, user_id: int | None, chat_id: int | None, url: str, platform: str, status: str, error: str | None = None) -> None:
        if not self.pool:
            return
        await self.pool.execute(
            """
            INSERT INTO link_events (user_id, chat_id, url, platform, status, error)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            user_id,
            chat_id,
            url,
            platform,
            status,
            error[:500] if error else None,
        )

    async def get_cached_video(self, url: str) -> str | None:
        if not self.pool:
            return None
        row = await self.pool.fetchrow("SELECT telegram_file_id FROM cached_videos WHERE url = $1", url)
        if not row:
            return None
        await self.pool.execute(
            "UPDATE cached_videos SET last_used_at = now(), use_count = use_count + 1 WHERE url = $1",
            url,
        )
        return row["telegram_file_id"]

    async def save_cached_video(self, url: str, platform: str, file_id: str, file_unique_id: str | None) -> None:
        if not self.pool:
            return
        await self.pool.execute(
            """
            INSERT INTO cached_videos (url, platform, telegram_file_id, file_unique_id)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (url) DO UPDATE SET
                telegram_file_id = EXCLUDED.telegram_file_id,
                file_unique_id = EXCLUDED.file_unique_id,
                last_used_at = now(),
                use_count = cached_videos.use_count + 1
            """,
            url,
            platform,
            file_id,
            file_unique_id,
        )

    async def public_stats(self) -> dict[str, int]:
        if not self.pool:
            return {}
        row = await self.pool.fetchrow(
            """
            SELECT
                (SELECT count(*) FROM users) AS total_users,
                (SELECT count(*) FROM users WHERE start_count > 0) AS started_users,
                (SELECT count(*) FROM chats WHERE type IN ('group', 'supergroup') AND is_active) AS active_chats,
                (SELECT count(DISTINCT user_id) FROM user_chat_activity WHERE last_seen_at >= now() - interval '30 days') AS active_users_30d,
                (SELECT count(*) FROM link_events WHERE status = 'success') AS successful_videos,
                (SELECT count(*) FROM link_events) AS total_links
            """
        )
        return dict(row) if row else {}

