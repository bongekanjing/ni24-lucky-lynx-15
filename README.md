# 24 November 2026: The World in One Day

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bongekanjing/ni24-lucky-lynx-15/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bongekanjing/ni24-lucky-lynx-15/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for **[make.fun · news-image-20261124](https://make.fun/bounty/news-image-20261124)**:
one image that sums up the world's news of Tuesday 24 November 2026, built by an
AI agent.

`entry.png` is a single 1024x1024 typographic newspaper front page: the day's
date as the page's largest type, a strip of the day's key figures, four
typographic leads across the measure, and a numbered five-column grid of 40
one-line briefs across eight beats. Each lead carries a small drawn plate above
its kicker, a flat vignette of its story.

## What the page carries

Four leads, one per region-defining story:

- **Climate** — COP31 in Antalya closed in collapse, the "Antalya Pact" naming
  no coal, oil or gas after the longest COP on record.
- **Middle East** — Iran vowed to use "all available means" against the US
  naval blockade of its ports, with tankers readied at Kharg Island.
- **Ukraine** — Ukrainian sea drones sank the Russian corvette *Merkury* at
  Benghazi, as Moscow ruled out any new grain deal at the UN.
- **Humanitarian** — the WFP warned that the Hormuz, Bab el-Mandeb and Black Sea
  chokepoints could add $727 million to its costs, putting food aid for 7.3
  million more people at risk.

The briefs cover climate, the Middle East, Ukraine and Europe, Asia, the
Americas, the economy, Africa and sport — 40 stories, eight beats, with figures
as published that day and one-sided claims attributed rather than asserted.

## How it is built

- `entry.png` — the committed image, the entry itself.
- `main.py` — Python 3.13, standard library only. It copies the committed image
  to `$MAKEFUN_OUTPUT_DIR/entry.png`, checking the PNG or JPEG magic, the
  1 MiB cap and the 1024 px side on the way, and fails loudly rather than
  writing an empty or partial file.
- `tools/front.py` — the renderer that produced the image: it searches for the
  type size that makes the brief grid fill the space between the beat bar and
  the footer, balances the four columns by binary-searching the flattest
  contiguous partition, and asserts that no text box leaves the canvas or
  overlaps another.
- `fonts/` — the typefaces the page uses.

The image is a fixed artefact of one day, so the program copies it rather than
drawing it: two runs write identical bytes by construction.

## Layout discipline

The renderer is verified without looking at the image. It monkey-patches
`ImageDraw.text` to record a `textbbox` for every call and asserts that zero
boxes leave the 1024x1024 canvas and zero overlap; it checks the column bottoms
land flush; it scans for dead panels by colour density; and it asserts the file
is under 1 MiB and exactly 1024x1024.

## Sources

Events of Tuesday 24 November 2026, as reported that day by Reuters, AP, Al
Jazeera, the BBC, Anadolu Agency, the WFP and others. Figures are as published
on the day; disputed claims are attributed, not asserted.

## License

MIT. See `LICENSE`.
