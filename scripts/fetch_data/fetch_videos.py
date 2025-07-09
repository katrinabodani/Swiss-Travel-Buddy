# scripts/fetch_video.py

from youtube_transcript_api import YouTubeTranscriptApi
import os
from urllib.parse import urlparse, parse_qs

# Where to dump transcripts
OUTPUT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,  # scripts/
        os.pardir,  # project root
        'data',
        'cleaned'
    )
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc == 'youtu.be':
        return parsed.path.lstrip('/')
    qs = parse_qs(parsed.query)
    return qs.get('v', [None])[0]

def fetch_transcript(url: str):
    vid = get_video_id(url)
    if not vid:
        print(f"[!] Could not parse video ID from {url}")
        return
    try:
        segments = YouTubeTranscriptApi.get_transcript(vid)
        text = ' '.join(seg['text'] for seg in segments)
        out_path = os.path.join(OUTPUT_DIR, f"{vid}_transcript.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved transcript for {vid} → {out_path}")
    except Exception as e:
        print(f"[!] Error fetching {vid}: {e}")

if __name__ == '__main__':
    # List your Swiss travel YouTube URLs here
    video_urls = [
        "https://www.youtube.com/watch?v=xLTCivIB4kU",
        "https://www.youtube.com/watch?v=jThz8eeDHUk",
        "https://www.youtube.com/watch?v=6pF1MDHSeAc",
        "https://www.youtube.com/watch?v=tgz_IQKBz4M",
        "https://www.youtube.com/watch?v=TRtLDVi9Ues&t=46s"
    ]
    for url in video_urls:
        fetch_transcript(url)
