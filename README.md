# Vatteluttu Inscription Dataset

Photographs of Tamil Vatteluttu stone inscriptions, with character-level bounding boxes and labels, plus the browser tool used to annotate them.

Each character carved in the stone is marked with a box and labelled with the modern Tamil letter it represents (for example க, ழு, கொ). The labels cover all 247 Tamil letters, and new labels can be added when needed.

## Repository layout

```
vateluttu_dataset/
├── image/                     source photographs (503 .jpg, not in git — see below). Never edited by the tool.
├── dataset/
│   ├── <photo name>.json      the boxes and letters for one photograph
│   └── image/<photo name>.jpg the same photograph with its boxes drawn on it
├── annotator.html             the annotation tool (runs in the browser)
├── annotator_server.py        small local server that lets the tool read image/ and save to dataset/
├── run_annotator.bat          start the tool on Windows
├── run_annotator.sh           start the tool on macOS / Linux
├── ANNOTATION_GUIDE.md        how to annotate: the standard procedure
└── README.md
```

A photograph is annotated when `dataset/` has a JSON file with the same name. For example, `image/IMG20251003071354.jpg` is annotated in `dataset/IMG20251003071354.json`.

## Quick start

You need **Python 3.8 or newer** (no extra packages) and **Google Chrome or Microsoft Edge**.

```bash
git clone <this repository URL>
cd vateluttu_dataset
```

**Add the photographs.** The 503 photographs (about 8 GB) are too large for GitHub, so they are not in the repository. Get them from the dataset owner and copy all the `.jpg` files **directly** into the `image/` folder (not into a subfolder).

Then start the annotator:

- **Windows:** double-click `run_annotator.bat`.
- **macOS / Linux:** run `sh run_annotator.sh`.

The annotator opens in your browser at `http://127.0.0.1:8777/` with all photographs loaded. Keep the black terminal window open while you work, and close it when you are done.

Everything saves automatically to `dataset/` as you draw. There is no save button. Wait for **"All changes saved"** at the top right before closing.

> **Without Python:** open `annotator.html` directly in Chrome or Edge, click **Load Folder** and choose the `vateluttu_dataset` folder (the one that contains `image`). It works the same way and saves to the same `dataset/` folder.

Before you annotate, read **[ANNOTATION_GUIDE.md](ANNOTATION_GUIDE.md)**. It covers how to draw boxes, which letter to choose, and how to split the work so that two people never edit the same photograph.

## The annotator

**Annotate tab**
- Drag on the photograph to draw a box. Press **L** (or **Enter**) to choose its letter.
- In the letter window you can search in Tamil or English: `ka` finds க, `zhu` finds ழு, `kai` finds கை.
- Drag a box to move it, or drag its edge to resize it.
- The **Annotations** panel lists every box on the photograph. Boxes with a letter are green; boxes without one are orange.
- **Lock** prevents accidental edits while you only look.

**Gallery tab**
- Every box is cropped and grouped under its letter, so mistakes stand out.
- Drag crops onto a letter folder (or use **Move →**) to relabel them. Click a folder to see its crops.
- Folders can be renamed, reordered, deleted or created. Renaming a folder relabels every box in it.

**Load Annotations** imports boxes from another JSON file into the matching photographs and saves them to `dataset/`. It accepts this tool's own files and COCO-style `annotations.json` / `dataset.json` files, including those from the palm-leaf annotator.

### Keyboard shortcuts

Press **?** in the annotator to see the full list.

| Key | Action |
|---|---|
| `D` / `P` | Draw mode / Pan mode |
| `L` or `Enter` | Choose the letter for the selected box (`L` with nothing selected: lock / unlock) |
| `Del` | Delete the selected box |
| `Tab` / `Shift+Tab` | Select the next / previous box |
| `Esc` | Let go of the selected box |
| `← → ↑ ↓` | Scroll the photograph. If you clicked a box, they move that box 1 px instead (10 px with `Shift`) |
| `Page Up` / `Page Down`, `Ctrl+←` / `Ctrl+→` | Previous / next photograph |
| `+` / `−`, mouse wheel | Zoom around the mouse cursor |
| `F` | Fit the photograph to the screen |
| `Space` + drag, right-drag | Pan |
| `Ctrl+Z` | Undo |
| `Ctrl+S` | Save now (it also saves by itself) |

## Annotation format

One JSON file per photograph, in `dataset/`:

```json
{
  "info": { "description": "Vatteluttu Inscription Character Dataset", "version": "1.0", "date_modified": "2026-11-15T13:41:56.796Z" },
  "image": { "file_name": "IMG20251003071354.jpg", "width": 1755, "height": 2535, "annotated_image": "image/IMG20251003071354.jpg" },
  "annotations": [
    { "id": 1, "bbox": [981, 865, 153, 176], "area": 26928, "char_label": "வ", "source": "human" },
    { "id": 2, "bbox": [1126, 892, 139, 163], "area": 22657, "char_label": null, "source": "human" }
  ]
}
```

| Field | Meaning |
|---|---|
| `bbox` | `[x, y, width, height]` in pixels of the original photograph, with the origin at the top-left (COCO convention) |
| `char_label` | The modern Tamil letter, or `null` if the box has not been labelled yet |
| `id` | Box number within this photograph, in the order the boxes were drawn |
| `annotated_image` | Path, relative to `dataset/`, of the picture with the boxes drawn on it |

To read the whole dataset in Python:

```python
import json, pathlib

for path in sorted(pathlib.Path("dataset").glob("*.json")):
    doc = json.loads(path.read_text(encoding="utf-8"))
    photo = pathlib.Path("image") / doc["image"]["file_name"]
    for box in doc["annotations"]:
        if box["char_label"]:                  # skip boxes that are not labelled yet
            x, y, w, h = box["bbox"]
            print(photo, box["char_label"], x, y, w, h)
```

## Troubleshooting

- **"No pictures found" / nothing loads:** the photographs must be directly inside `image/`.
- **The page keeps reloading:** you opened it through VS Code Live Server or Live Preview. Use `run_annotator.bat` / `run_annotator.sh` instead.
- **"The annotator is already running":** it is already open. The script opens the existing page in your browser.
- **Port 8777 is in use by something else:** set another port first, for example `set ANNOTATOR_PORT=8800` (Windows) or `export ANNOTATOR_PORT=8800` (macOS / Linux).
- **Annotations saved in the wrong place:** they always go to `dataset/` next to `image/`. If you chose the `image` folder itself, the tool asks you to choose `vateluttu_dataset` instead.
