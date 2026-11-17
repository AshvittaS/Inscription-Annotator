# Annotation Guide: Standard Procedure

Follow this procedure for every photograph so that the dataset stays consistent no matter who annotated it.

**Goal:** for each photograph, draw one box around every carved character and label it with the modern Tamil letter it represents.

---

## 1. Before you start (once)

1. Install **Python 3.8+** and **Chrome** or **Edge**.
2. Clone the repository and open the folder:
   ```bash
   git clone <this repository URL>
   cd vateluttu_dataset
   ```
3. Copy the photographs you received from the dataset owner directly into the `image/` folder. They are not in the repository because they are too large.
4. Agree on **which photographs are yours** with the rest of the team. Use a range of file names, for example *photos 1–100 in the list → Person A, 101–200 → Person B*. Never annotate a photograph that someone else is working on: two people editing the same JSON file causes merge conflicts.

## 2. At the start of every session

1. Get the latest work from the others:
   ```bash
   git pull
   ```
2. Start the annotator: double-click `run_annotator.bat` (Windows) or run `sh run_annotator.sh` (macOS / Linux).
3. In the image list on the left, choose **Not annotated** in the filter menu to see only the photographs that still need work, then click the first one in your range.

## 3. Annotating one photograph

1. **Look at the whole stone first.** Press `F` to fit the photograph to the screen and find where the inscription lines are.
2. **Zoom in on the first line.** Put the mouse on it and press `+` or use the wheel. Work at a zoom where each character is clearly visible.
3. **Work in reading order:** line by line from the top, and left to right within a line. Boxes are saved in the order you draw them, so drawing in reading order keeps each line's characters in sequence.
4. For **each character**:
   1. Drag a box around it (see the box rules in section 4).
   2. Press `L` (or `Enter`). The letter window opens.
   3. Type the letter in Tamil or in English (`ka` → க, `zhu` → ழு, `kai` → கை) and press `Enter`, or click it in the list.
   4. The box turns **green**. Draw the next one.

   Tip: tick **"Ask for the letter after drawing"** at the bottom right, and the letter window opens by itself after every box.
5. **Move along the inscription** with the arrow keys (`→` shows more to the right, `↓` shows more below). The arrows scroll the photograph unless you have clicked a box; press `Esc` to let go of a box.
6. **Fix mistakes as you go:**
   - Click a box to select it, then drag it to move it or drag its edge to resize it. Arrow keys move it 1 px (10 px with `Shift`).
   - `Del` deletes the selected box, and `Ctrl+Z` undoes.
   - To change a letter, select the box and press `L` again.
7. **Check the photograph before moving on:**
   - The **Annotations** panel on the right should have no orange (unlabelled) boxes, except characters you deliberately left unlabelled (section 5).
   - Press `F` and look over the whole stone once more for characters you missed.
8. Go to the next photograph with `Page Down` (or `Ctrl+→`).

## 4. Box rules

| Rule | Details |
|---|---|
| **One box = one letter** | A letter is what you would write as one Tamil letter: a vowel (அ), a consonant (க), a consonant with its vowel sign (கா, கி, கு, கெ, கொ, கை …) or a pure consonant (க்). |
| **Include the vowel signs** | Signs written before or after the consonant belong to the same box. கொ is **one** box covering ெ + க + ா, not three. |
| **Include the pulli** | The dot of a pure consonant (க்) goes inside the box. |
| **Tight, but complete** | Box edges should touch the outer edge of the carved strokes, with only a few pixels of stone around them. No stroke may be cut off. |
| **Overlaps are fine** | Neighbouring letters often overlap. Boxes may overlap too. Hold `Shift` while dragging to start a new box inside an existing one. |
| **Carving only** | Do not box cracks, stains, chisel marks, modern scratches, or the edge of the stone. |
| **Every legible letter** | Box every character you can see, even small or faded ones. |

## 5. Choosing the letter

- Always label with the **modern Tamil letter** that the Vatteluttu character stands for, even though the shapes are different.
- **If you are not sure,** still draw the box but **leave it unlabelled** (orange). Do not guess. Unlabelled boxes are reviewed later with the filter **Has unlabelled boxes**.
- **Badly damaged characters:** draw the box only if you can see that a character was there. If you cannot read it, leave it unlabelled.
- **Numerals and other symbols:** use a folder named after them. To create one, type the name in the letter window and press `Enter`. Before creating a new folder, check with the team, so that everyone uses the same names (for example `numeral_1`, `symbol_shri`).
- Never create a folder for a letter that already exists under another spelling. Search for it in English first (`ka`, `nna`, `zha`…).

## 6. Review (once a batch is finished)

1. Open the **Gallery** tab and tick **"Only folders with crops"**.
2. Click each letter folder. All its crops should look like the same character. Any crop that looks different is probably mislabelled:
   - Select it in the left panel (Ctrl+click to select several) and drag it onto the correct folder, or use **Move →**.
   - Crops with a **red** border have no letter yet. Assign them if you can now read them.
3. Back in the Annotate tab, set the filter to **Has unlabelled boxes** and go through what remains.

## 7. At the end of every session

1. Wait until the top right says **"All changes saved"**, then close the browser tab and the terminal window.
2. Share your work:
   ```bash
   git pull
   git add dataset
   git commit -m "Annotate IMG20251003071354 – IMG20251003072210"
   git push
   ```
   Commit only the `dataset/` folder. The photographs in `image/` never change.

## 8. Do not

- Do not rename, edit, rotate or delete files in `image/`. Annotations are linked to the photograph by file name and pixel position.
- Do not edit the JSON files by hand. Use the annotator.
- Do not open `annotator.html` through VS Code Live Server. The page will keep reloading.
- Do not annotate photographs outside your agreed range.

---

### Quick reference

| Task | Keys |
|---|---|
| Draw a box | drag (in Draw mode, `D`) |
| Choose its letter | `L` or `Enter` → type `ka` / `zhu` / க → `Enter` |
| Delete / undo | `Del` / `Ctrl+Z` |
| Scroll the photograph | `← → ↑ ↓` (with `Shift`: further) |
| Let go of a box | `Esc` |
| Zoom | `+` `−` or wheel (around the cursor), `F` to fit |
| Next / previous photograph | `Page Down` / `Page Up` |
| All shortcuts | `?` |
