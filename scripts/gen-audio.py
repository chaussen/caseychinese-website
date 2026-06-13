#!/usr/bin/env python3
"""
Generate audio files for all characters, words, and sentences in char-data.js
using edge-tts (Microsoft Azure Neural voices, free, no API key required).

Usage:
    pip install edge-tts   # or: pipx install edge-tts
    python3 scripts/gen-audio.py

Output: learn/audio/char-{i}.mp3, word-{i}.mp3, sent-{i}.mp3  (0-indexed)

Safe to re-run — skips files that already exist. Delete a file to regenerate it.
"""

import asyncio
import json
import os
import re
import sys

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts not installed. Run: pip install edge-tts  (or pipx install edge-tts)")

VOICE = "zh-CN-XiaoxiaoNeural"   # natural Mandarin female; change to zh-CN-YunxiNeural for male
RATE  = "-10%"                    # slightly slower — clearer for learners
OUT   = os.path.join(os.path.dirname(__file__), "..", "learn", "audio")


def load_char_data():
    path = os.path.join(os.path.dirname(__file__), "..", "learn", "char-data.js")
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"window\.CHAR_DATA\s*=\s*(\[.*\])", content, re.DOTALL)
    if not m:
        sys.exit("Could not parse char-data.js")
    return json.loads(m.group(1))


async def speak(text, path):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(path)


async def main():
    os.makedirs(OUT, exist_ok=True)
    data = load_char_data()

    tasks = []
    labels = []

    for i, d in enumerate(data):
        # single character
        char_path = os.path.join(OUT, f"char-{i}.mp3")
        if not os.path.exists(char_path):
            tasks.append(speak(d["ch"], char_path))
            labels.append(f"char-{i}  {d['ch']}")

        # word (2–3 characters)
        if d.get("word"):
            word_text = "".join(p[0] for p in d["word"]["seg"])
            word_path = os.path.join(OUT, f"word-{i}.mp3")
            if not os.path.exists(word_path):
                tasks.append(speak(word_text, word_path))
                labels.append(f"word-{i}  {word_text}")

        # example sentence
        if d.get("ex"):
            sent_text = "".join(p[0] for p in d["ex"]["seg"])
            sent_path = os.path.join(OUT, f"sent-{i}.mp3")
            if not os.path.exists(sent_path):
                tasks.append(speak(sent_text, sent_path))
                labels.append(f"sent-{i}  {sent_text}")

    if not tasks:
        print("All audio files already exist. Nothing to do.")
        return

    print(f"Generating {len(tasks)} audio files into learn/audio/ ...")
    print(f"Voice: {VOICE}  Rate: {RATE}\n")

    # Run in batches to avoid hammering the API
    batch = 10
    for start in range(0, len(tasks), batch):
        chunk = tasks[start:start + batch]
        chunk_labels = labels[start:start + batch]
        await asyncio.gather(*chunk)
        for label in chunk_labels:
            print(f"  ✓ {label}")

    print(f"\nDone. {len(tasks)} files written to learn/audio/")


if __name__ == "__main__":
    asyncio.run(main())
