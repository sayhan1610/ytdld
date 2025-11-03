#!/usr/bin/env python3
"""
yt_mp3_dl.py
Download only audio from a list of YouTube URLs (list.txt),
convert to 192kbps MP3 using ffmpeg via yt-dlp, multithreaded.

run with: python dl.py --list list.txt
"""

import os
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init as colorama_init
import yt_dlp

colorama_init(autoreset=True)


def download_one(url: str, out_dir: Path, bitrate: str = "192K") -> tuple[str, bool, str]:
    """Download single YouTube URL as mp3 using yt-dlp."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": bitrate[:-1]  # remove 'K'
        }],
        "overwrites": False,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "untitled")
            mp3_path = out_dir / f"{title}.mp3"
            if mp3_path.exists():
                return title, True, "Skipped (already exists)"
            ydl.download([url])
        return title, True, "Downloaded & converted"
    except Exception as e:
        return url, False, str(e)


def parse_list(list_file: Path):
    if not list_file.exists():
        sys.exit(f"{Fore.RED}List file not found: {list_file}{Style.RESET_ALL}")
    with list_file.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", default="list.txt", help="Path to list of YouTube URLs.")
    parser.add_argument("--out", "-o", default="downloads", help="Output directory.")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Concurrent downloads.")
    parser.add_argument("--bitrate", "-b", default="192K", help="MP3 bitrate (default 192K).")
    args = parser.parse_args()

    urls = parse_list(Path(args.list))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{Fore.GREEN}Downloading {len(urls)} videos → {args.bitrate} MP3s{Style.RESET_ALL}")
    summary = {"ok": 0, "fail": 0, "skip": 0, "fails": []}

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(download_one, url, out_dir, args.bitrate): url for url in urls}
        for fut in tqdm(as_completed(futures), total=len(urls), desc="Progress", unit="file"):
            title, ok, msg = fut.result()
            if ok:
                if "skip" in msg.lower():
                    summary["skip"] += 1
                    print(f"{Fore.CYAN}SKIP{Style.RESET_ALL}: {title}")
                else:
                    summary["ok"] += 1
                    print(f"{Fore.GREEN}OK{Style.RESET_ALL}: {title}")
            else:
                summary["fail"] += 1
                summary["fails"].append((title, msg))
                print(f"{Fore.RED}FAIL{Style.RESET_ALL}: {title} — {msg}")

    print("\n" + "="*40)
    print(f"{Fore.MAGENTA}Summary{Style.RESET_ALL}")
    print(f"Success: {summary['ok']} | Skipped: {summary['skip']} | Failed: {summary['fail']}")
    if summary["fails"]:
        for t, m in summary["fails"]:
            print(f" - {t[:60]} : {m}")


if __name__ == "__main__":
    main()
