import re


SUPPORTED_URL_RE = re.compile(
    r"https?://(?:www\.|m\.)?(?:"
    r"tiktok\.com/[^\s<>()]+|"
    r"vm\.tiktok\.com/[^\s<>()]+|"
    r"vt\.tiktok\.com/[^\s<>()]+|"
    r"youtube\.com/shorts/[^\s<>()]+|"
    r"youtu\.be/[^\s<>()]+"
    r")",
    re.IGNORECASE,
)


def extract_supported_urls(text: str | None) -> list[str]:
    if not text:
        return []
    seen: set[str] = set()
    urls: list[str] = []
    for match in SUPPORTED_URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;:!?)]}")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def detect_platform(url: str) -> str:
    lowered = url.lower()
    if "tiktok.com" in lowered:
        return "tiktok"
    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "youtube_shorts"
    return "unknown"

