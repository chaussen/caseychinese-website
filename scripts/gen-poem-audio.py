#!/usr/bin/env python3
"""
Generate a single audio file for the 咏鹅 poem: title, author, then lines.

Uses SSML <break> tags so each 鹅 is a distinct exclamation with a natural
pause, and line endings breathe properly — rather than being read as a list.

Usage:
    pip install edge-tts   # or: pipx install edge-tts
    python3 scripts/gen-poem-audio.py

Output: learn/audio/poem-yonge.mp3  (delete to regenerate)
"""

import asyncio
import os
import sys

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts not installed. Run: pip install edge-tts  (or pipx install edge-tts)")

VOICE = "zh-CN-XiaoxiaoNeural"
RATE  = "-15%"
OUT   = os.path.join(os.path.dirname(__file__), "..", "learn", "audio")

# SSML: explicit pauses between each 鹅 and at line breaks for natural recitation
SSML = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="zh-CN">
  <voice name="zh-CN-XiaoxiaoNeural">
    <prosody rate="-15%">
      咏鹅。
      <break time="600ms"/>
      骆宾王。
      <break time="900ms"/>
      鹅，<break time="450ms"/>鹅，<break time="450ms"/>鹅，
      <break time="500ms"/>
      曲项向天歌。
      <break time="600ms"/>
      白毛浮绿水，
      <break time="400ms"/>
      红掌拨清波。
    </prosody>
  </voice>
</speak>"""


async def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "poem-yonge.mp3")
    if os.path.exists(path):
        print(f"Already exists: {path}  (delete to regenerate)")
        return
    print(f"Generating {path} using SSML ...")
    communicate = edge_tts.Communicate(SSML, VOICE)
    await communicate.save(path)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
