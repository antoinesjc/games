# Mandarin Zest games

Classroom games by [Mandarin Zest](https://www.mandarinzest.com).

## Oracle Bone Mystery 甲骨之謎 (`oracle-bone/`)

Project it in class. Teams guess what each 3,000-year-old oracle bone glyph shows, then which modern character it became.

- Live: https://antoinesjc.github.io/games/oracle-bone/
- Teacher keys: **M** reveal meaning · **C** reveal character · **F** story & fact · **H** clue · **Space/T** timer · **1–4** +10 to a team · **← →** previous / next bone
- You can also click the answer the class shouts: wrong answers shake, right ones turn green.
- Jump links: `#1-3` = chapter 1, bone 3 · `#2-end` = chapter 2 finale
- Scores are kept in the browser until you press **Reset scores**.

### Images
Glyphs are public-domain SVGs from Wikimedia Commons (Ancient Chinese characters project, based on Richard Sears' Chinese Etymology data). Photos of real oracle bones are from Wikimedia Commons under CC BY-SA 3.0. All sources and licenses are in `oracle-bone/img/credits.json`.

To add characters, add them to `GLYPHS` in `scripts/fetch_images.py` and push: the **Fetch oracle bone images** GitHub Action downloads them into `oracle-bone/img/`.
