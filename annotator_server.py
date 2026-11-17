"""Local server for annotator.html.

Serves the page and reads/writes files next to this script:
    image/                  source pictures (never modified)
    dataset/<name>.json     annotations for each picture
    dataset/image/<name>    the annotated picture

Start it with run_annotator.bat (or: python annotator_server.py).
"""
import json
import os
import shutil
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annotator.html")
IMG = os.path.join(ROOT, "image")
DATA = os.path.join(ROOT, "dataset")
OUT = os.path.join(DATA, "image")
PORT = int(os.environ.get("ANNOTATOR_PORT", "8777"))
IMG_EXT = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".bmp": "image/bmp", ".webp": "image/webp"}


def names(folder, exts):
    if not os.path.isdir(folder):
        return []
    return sorted(n for n in os.listdir(folder)
                  if os.path.splitext(n)[1].lower() in exts and os.path.isfile(os.path.join(folder, n)))


def locate(url, writing):
    """Map a request path to (folder, file name), or None if it is not an allowed file."""
    parts = [unquote(p) for p in urlsplit(url).path.strip("/").split("/")]
    if len(parts) == 2 and parts[0] == "image" and not writing:
        folder, exts = IMG, IMG_EXT
    elif len(parts) == 2 and parts[0] == "dataset":
        folder, exts = DATA, {".json"}
    elif len(parts) == 3 and parts[:2] == ["dataset", "image"]:
        folder, exts = OUT, IMG_EXT
    else:
        return None
    name = parts[-1]
    if not name or name.startswith(".") or name != os.path.basename(name) or "/" in name or "\\" in name:
        return None
    if os.path.splitext(name)[1].lower() not in exts:
        return None
    return folder, name


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def reply(self, code, body=b"", ctype="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def same_site(self):
        origin = self.headers.get("Origin")
        return not origin or origin in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}")

    def send_file(self, path, ctype):
        try:
            f = open(path, "rb")
        except OSError:
            return self.reply(404, "not found")
        with f:
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(os.fstat(f.fileno()).st_size))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ("/", "/annotator.html"):
            return self.send_file(PAGE, "text/html; charset=utf-8")
        if path == "/api/list":
            body = json.dumps({"images": names(IMG, IMG_EXT), "jsons": names(DATA, {".json"}), "outs": names(OUT, IMG_EXT)})
            return self.reply(200, body, "application/json")
        where = locate(self.path, writing=False)
        if not where:
            return self.reply(404, "not found")
        folder, name = where
        ext = os.path.splitext(name)[1].lower()
        self.send_file(os.path.join(folder, name), IMG_EXT.get(ext, "application/json; charset=utf-8"))

    def do_PUT(self):
        length = int(self.headers.get("Content-Length") or 0)
        data = self.rfile.read(length)
        where = locate(self.path, writing=True)
        if not where or not self.same_site():
            return self.reply(403, "not allowed")
        folder, name = where
        os.makedirs(folder, exist_ok=True)
        target = os.path.join(folder, name)
        tmp = target + ".part"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, target)
        self.reply(200, "saved")

    def do_DELETE(self):
        where = locate(self.path, writing=True)
        if not where or not self.same_site():
            return self.reply(403, "not allowed")
        try:
            os.remove(os.path.join(*where))
        except FileNotFoundError:
            pass
        self.reply(200, "removed")


def main():
    if not os.path.isdir(IMG):
        sys.exit(f'No "image" folder found in {ROOT}')
    os.makedirs(OUT, exist_ok=True)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"The annotator is already running. Opening http://127.0.0.1:{PORT}/")
        webbrowser.open(f"http://127.0.0.1:{PORT}/")
        return
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Annotator running at {url}")
    print(f"  pictures : {IMG}  ({len(names(IMG, IMG_EXT))} found)")
    print(f"  saving to: {DATA}")
    print("Keep this window open while you annotate. Close it (or press Ctrl+C) when you are done.")
    if not os.environ.get("ANNOTATOR_NO_BROWSER"):
        threading.Timer(0.5, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
