# 🎧 yt-mp3-downloader

A simple Python CLI tool to download **audio-only MP3s (192 kbps)** from a list of YouTube URLs using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and `ffmpeg`.

---

## 📦 Features
- Downloads only audio (MP3 @ 192 kbps)
- Supports batch downloads from a text file (`list.txt`)
- Skips files already downloaded
- Multi-threaded (configurable)
- Cross-platform compatible (Windows, macOS, Linux)
- Detailed progress and colored terminal output

---

## 🧰 Prerequisites
1. **Python 3.8+**
2. **ffmpeg** installed and added to your system PATH
   - **Windows:** Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/)
   - **macOS:** `brew install ffmpeg`
   - **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`

---

## ⚙️ Installation

1. Clone the repo or download ZIP:
   ```bash
   git clone https://github.com/sayhan1610/ytdld.git
   cd ytdld
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 📝 Usage

1. Create a file called `list.txt` in the same folder:

   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   https://youtu.be/VIDEO_ID
   ```

2. Run the downloader:

   ```bash
   python dl.py --list list.txt --out downloads --workers 4
   ```

   or, if you're on **Windows**, just double-click `app.bat`.

3. Files will be saved in the `downloads/` folder as `.mp3`.

---

## ⚡ Optional Arguments

| Flag               | Description                  | Default     |
| ------------------ | ---------------------------- | ----------- |
| `--list` / `-l`    | Path to your URL list        | `list.txt`  |
| `--out` / `-o`     | Output directory             | `downloads` |
| `--workers` / `-w` | Number of parallel downloads | `4`         |
| `--bitrate` / `-b` | MP3 bitrate                  | `192K`      |

Example:

```bash
python dl.py --list list.txt --out songs --workers 6 --bitrate 256K
```

---

## 🧹 Notes

* URLs starting with `#` are ignored.
* Duplicate sanitized titles are skipped.
* If you want to re-download, delete the existing `.mp3` first.




