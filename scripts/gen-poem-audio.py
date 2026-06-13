#!/usr/bin/env python3
"""
Generate a single audio file for the 咏鹅 poem: title, author, then lines.

Usage:
    pip install edge-tts   # or: pipx install edge-tts
    python3 scripts/gen-poem-audio.py

Output: learn/audio/poem-yonge.mp3
"""

import asyncio
import os
import sys

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts not installed. Run: pip install edge-tts  (or pipx install edge-tts)")

VOICE = "zh-CN-XiaoxiaoNeural"
RATE  = "-15%"   # slightly slower for poetry — more expressive pacing
OUT   = os.path.join(os.path.dirname(__file__), "..", "learn", "audio")

# Full recitation text: title, author, then the four lines
TEXT = "咏鹅。骆宾王。鹅，鹅，鹅，曲项向天歌。白毛浮绿水，红掌拨清波。"


async def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "poem-yonge.mp3")
    if os.path.exists(path):
        print(f"Already exists: {path}  (delete to regenerate)")
        return
    print(f"Generating {path} ...")
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    await communicate.save(path)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
