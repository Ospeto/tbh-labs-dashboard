"""
Competitor Analysis — YouTube Multi-Channel Data Pipeline
==========================================================
Fetches all public videos from competitor channels + TBH Labs Myanmar,
and exports unified metrics to Competitor_Videos.csv.

Columns: channel_handle, video_id, title, view_count, like_count,
         comment_count, duration, duration_seconds, upload_date,
         upload_hour, day_of_week
"""

import re
import csv
from datetime import datetime
from googleapiclient.discovery import build

# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = "AIzaSyCgR1peEdx_U6Q8gac9DBAWOd4mcfu_nEo"
OUTPUT_CSV = "Competitor_Videos.csv"

CHANNELS = [
    "@TBHLabsMyanmar",
    "@MMTR",
    "@MyTechMyanmar",
    "@zestvlog",
    "@technity17",
    "@T4U2MM",
]

COLUMNS = [
    "channel_handle", "channel_name", "video_id", "title",
    "view_count", "like_count", "comment_count",
    "duration", "duration_seconds",
    "upload_date", "upload_hour", "day_of_week",
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def parse_iso8601_duration(iso_duration: str) -> tuple[str, int]:
    """Convert ISO 8601 duration (PT#H#M#S) to (MM:SS string, total_seconds int)."""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not match:
        return "0:00", 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    total_seconds = hours * 3600 + minutes * 60 + seconds
    total_minutes = hours * 60 + minutes
    return f"{total_minutes}:{seconds:02d}", total_seconds


def resolve_channel_id(youtube, handle: str) -> tuple[str, str]:
    """Resolve a @handle to (channel_id, channel_title)."""
    resp = youtube.channels().list(
        part="id,snippet",
        forHandle=handle.lstrip("@")
    ).execute()
    if resp.get("items"):
        item = resp["items"][0]
        return item["id"], item["snippet"]["title"]
    raise ValueError(f"Could not resolve channel ID for {handle}")


def get_uploads_playlist_id(youtube, channel_id: str) -> str:
    """Get the 'uploads' playlist ID from a channel."""
    resp = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    return resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def fetch_all_video_ids(youtube, playlist_id: str) -> list[str]:
    """Page through a playlist and collect every video ID."""
    video_ids = []
    next_page = None
    while True:
        resp = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
        ).execute()
        for item in resp["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        next_page = resp.get("nextPageToken")
        if not next_page:
            break
    return video_ids


def fetch_video_details(youtube, video_ids: list[str], handle: str, channel_name: str) -> list[dict]:
    """Fetch statistics, content details, and snippet for batches of 50 videos."""
    rows = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        resp = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(batch)
        ).execute()

        for item in resp["items"]:
            snippet = item["snippet"]
            stats = item["statistics"]
            content = item["contentDetails"]
            published = datetime.fromisoformat(
                snippet["publishedAt"].replace("Z", "+00:00")
            )
            duration_str, duration_secs = parse_iso8601_duration(content["duration"])

            rows.append({
                "channel_handle": handle,
                "channel_name": channel_name,
                "video_id": item["id"],
                "title": snippet["title"],
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "duration": duration_str,
                "duration_seconds": duration_secs,
                "upload_date": published.strftime("%Y-%m-%d"),
                "upload_hour": published.strftime("%H:%M"),
                "day_of_week": published.strftime("%A"),
            })
    return rows


# ── Main Pipeline ────────────────────────────────────────────────────────────
def main():
    print("🔧 Building YouTube API client…")
    youtube = build("youtube", "v3", developerKey=API_KEY)

    all_rows = []

    for handle in CHANNELS:
        print(f"\n{'━'*60}")
        print(f"📡 Processing {handle}…")

        try:
            channel_id, channel_name = resolve_channel_id(youtube, handle)
            print(f"   ✅ Channel: {channel_name} ({channel_id})")
        except Exception as e:
            print(f"   ❌ Failed to resolve: {e}")
            continue

        playlist_id = get_uploads_playlist_id(youtube, channel_id)
        print(f"   📂 Uploads playlist: {playlist_id}")

        video_ids = fetch_all_video_ids(youtube, playlist_id)
        print(f"   📥 Found {len(video_ids)} videos")

        rows = fetch_video_details(youtube, video_ids, handle, channel_name)
        all_rows.extend(rows)
        print(f"   ✅ Fetched details for {len(rows)} videos")

    # Sort by upload date (newest first)
    all_rows.sort(key=lambda r: r["upload_date"], reverse=True)

    print(f"\n{'━'*60}")
    print(f"💾 Writing {len(all_rows)} total rows to {OUTPUT_CSV}…")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n✅ Done! {len(all_rows)} videos across {len(CHANNELS)} channels → {OUTPUT_CSV}")

    # Summary
    from collections import Counter
    ch_counts = Counter(r["channel_handle"] for r in all_rows)
    print("\n📊 Per-channel breakdown:")
    for ch, count in ch_counts.most_common():
        print(f"   • {ch}: {count} videos")


if __name__ == "__main__":
    main()
