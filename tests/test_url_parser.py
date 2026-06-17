from app.url_parser import detect_platform, extract_supported_urls


def test_extracts_supported_urls_once() -> None:
    text = "one https://vm.tiktok.com/abc/ and again https://vm.tiktok.com/abc/"

    assert extract_supported_urls(text) == ["https://vm.tiktok.com/abc/"]


def test_extracts_youtube_shorts_without_trailing_punctuation() -> None:
    text = "watch https://youtube.com/shorts/abc123)."

    assert extract_supported_urls(text) == ["https://youtube.com/shorts/abc123"]


def test_detects_platforms() -> None:
    assert detect_platform("https://tiktok.com/@user/video/1") == "tiktok"
    assert detect_platform("https://youtube.com/shorts/1") == "youtube_shorts"

