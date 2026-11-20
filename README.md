# Mandarin Zest games

Classroom games by [Mandarin Zest](https://www.mandarinzest.com).

## Oracle Bone Mystery 甲骨之謎 (`oracle-bone/`)

Project it in class. Teams guess what each 3,000-year-old oracle bone glyph shows, then which modern character it became.

- Live: https://antoinesjc.github.io/games/oracle-bone/
- Chapter 0: 7 slides on what oracle bones are. Chapters 1 to 5: 6 bones each plus a final challenge.
- Add player names on the start screen (commas work: `Anna, Ben, Chloé`). When someone types a right answer, click their name under "Who got it?" to give 10 points.
- Answers are typed: an English word for the meaning (synonyms are accepted), then the modern character (simplified or traditional).
- Teacher keys (when not typing in a box): **M** reveal meaning · **C** reveal character · **F** fun fact · **H** clue · **Space/T** timer · **← →** previous / next bone. **Esc** leaves a text box.
- Jump links: `#0` = slides · `#3-2` = chapter 3, bone 2 · `#3-end` = chapter 3 final challenge
- Scores and names are kept in the browser until you press **Reset scores**.
- All the text (slides, stories, accepted answers, facts) is in `oracle-bone/chapters.js`.

### Images
Glyphs are public-domain SVGs from Wikimedia Commons (Ancient Chinese characters project, based on Richard Sears' Chinese Etymology data). Photos of real oracle bones are from Wikimedia Commons under CC BY-SA 3.0. All sources and licenses are in `oracle-bone/img/credits.json`.

To add characters, add them to `GLYPHS` in `scripts/fetch_images.py` and push: the **Fetch oracle bone images** GitHub Action downloads them into `oracle-bone/img/`.
