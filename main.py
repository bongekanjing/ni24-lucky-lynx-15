"""24 November 2026: The World in One Day.

The entry is one image, `entry.png`, rendered by `tools/front.py` from the day's
news and committed beside this program. The grader runs this file twice in a
fresh container with no network, a read-only /bot holding the repository at the
submitted commit, and a writable /output; both runs must write the same bytes.

So this program does exactly one thing: it copies the committed image to
$MAKEFUN_OUTPUT_DIR/entry.png, checking the bytes on the way through, and fails
loudly rather than writing an empty or partial file. Nothing is drawn here: the
image is a fixed artefact of the day, and a copy is deterministic by
construction.

Standard library only.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

# The gate's limits, checked here too so a broken build fails at home rather
# than at intake.
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def die(message):
    sys.stderr.write("main.py: %s\n" % message)
    raise SystemExit(1)


def image_kind(data):
    """Name the format from the first bytes, as the gate does, or None."""
    if data[:8] == PNG_MAGIC:
        return "png"
    if data[:3] == JPEG_MAGIC:
        return "jpeg"
    return None


def png_size(data):
    """Width and height from a PNG's IHDR, which must be its first chunk."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        die("entry.png is not a whole PNG: its first chunk is not IHDR")
    return struct.unpack(">II", data[16:24])


def jpeg_size(data):
    """Width and height from a JPEG's first frame header."""
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        if length < 2:
            break
        i += 2 + length
    die("entry.png is not a whole JPEG: no frame header found")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isfile(SOURCE):
        die("the committed image is missing at %s" % SOURCE)

    size = os.path.getsize(SOURCE)
    if size == 0:
        die("the committed image is empty")
    if size > MAX_BYTES:
        die("the committed image is %d bytes, over the %d cap" % (size, MAX_BYTES))

    with open(SOURCE, "rb") as handle:
        head = handle.read(32)
    kind = image_kind(head)
    if kind is None:
        die("the committed image is neither a PNG nor a JPEG")
    width, height = png_size(head) if kind == "png" else jpeg_size(
        open(SOURCE, "rb").read())
    if width > MAX_SIDE or height > MAX_SIDE:
        die("the committed image is %dx%d, over %d a side" % (width, height, MAX_SIDE))
    if width < 1 or height < 1:
        die("the committed image is %dx%d" % (width, height))

    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)

    written = os.path.getsize(target)
    if written != size:
        die("wrote %d bytes for a %d byte image" % (written, size))

    print("entry.png: %s %dx%d %d bytes -> %s" % (kind, width, height, written, target))


if __name__ == "__main__":
    main()
