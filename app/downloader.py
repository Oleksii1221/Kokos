from __future__ import annotations

import asyncio
import logging
import shutil
import uuid
from pathlib import Path


log = logging.getLogger(__name__)


class DownloadError(RuntimeError):
    pass


async def download_video(url: str, downloads_dir: Path, max_video_mb: int, timeout: int) -> Path:
    job_dir = downloads_dir / str(uuid.uuid4())
    job_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(job_dir / "%(id)s.%(ext)s")
    command = [
        "yt-dlp",
        "--no-playlist",
        "--max-filesize",
        f"{max_video_mb}M",
        "-f",
        "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
        "--merge-output-format",
        "mp4",
        "-o",
        output_template,
        url,
    ]

    log.info("Downloading video: %s", url)
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.TimeoutError as exc:
        process.kill()
        shutil.rmtree(job_dir, ignore_errors=True)
        raise DownloadError("Download timed out") from exc

    if process.returncode != 0:
        shutil.rmtree(job_dir, ignore_errors=True)
        details = (stderr or stdout).decode("utf-8", errors="ignore").strip()
        raise DownloadError(details or "yt-dlp failed")

    candidates = sorted(job_dir.glob("*.mp4"), key=lambda path: path.stat().st_size, reverse=True)
    if not candidates:
        candidates = sorted(job_dir.iterdir(), key=lambda path: path.stat().st_size if path.is_file() else 0, reverse=True)
    if not candidates:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise DownloadError("Downloaded file was not found")

    video = candidates[0]
    size_mb = video.stat().st_size / 1024 / 1024
    if size_mb > max_video_mb:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise DownloadError(f"Video is too large: {size_mb:.1f} MB")

    return video


def cleanup_download(path: Path) -> None:
    shutil.rmtree(path.parent, ignore_errors=True)

