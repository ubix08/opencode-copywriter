#!/usr/bin/env python3
"""
Article Preview Server
Serves rendered HTML from markdown articles with live-reload.
Binds to 0.0.0.0 for public access on VPS.

Usage:
    python3 scripts/preview.py [article.md] [--port 8080] [--host 0.0.0.0]

If no article is specified, serves an index of all articles.
"""

import argparse
import glob
import json
import os
import re
import socket
import sys
import threading
import time
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

try:
    import markdown
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError as e:
    print(f"Error: {e}")
    print("Install dependencies: pip install markdown pygments watchdog")
    sys.exit(1)

# Configuration
CONTENT_DIR = "content"
ARTICLES_DIR = os.path.join(CONTENT_DIR, "articles")
IMAGES_DIR = os.path.join(CONTENT_DIR, "images")
DEFAULT_PORT = 8080
DEFAULT_HOST = "0.0.0.0"

# Global state for live-reload
file_mtimes = {}
reload_lock = threading.Lock()


class ReloadHandler(FileSystemEventHandler):
    """Watch for file changes and track modification times."""

    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            with reload_lock:
                file_mtimes[event.src_path] = time.time()

    def on_created(self, event):
        if event.src_path.endswith(".md"):
            with reload_lock:
                file_mtimes[event.src_path] = time.time()


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, match.group(2)


def highlight_code(code: str, lang: str) -> str:
    """Highlight code block using Pygments."""
    try:
        lexer = get_lexer_by_name(lang)
        formatter = HtmlFormatter(
            style="github-dark",
            linenos=False,
            cssclass="codehilite",
            noclasses=False,
        )
        return highlight(code, lexer, formatter)
    except ClassNotFound:
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<div class="codehilite"><pre><code>{escaped}</code></pre></div>'


def preprocess_markdown(content: str) -> str:
    """Preprocess markdown to handle code blocks with Pygments."""
    pattern = r"```(\w+)?\n(.*?)```"

    def replacer(match):
        lang = match.group(1) or "text"
        code = match.group(2)
        return highlight_code(code, lang)

    return re.sub(pattern, replacer, content, flags=re.DOTALL)


def render_article(filepath: str) -> str:
    """Render a markdown article to HTML."""
    with open(filepath, "r") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)
    body = preprocess_markdown(body)

    md = markdown.Markdown(extensions=[
        "tables",
        "fenced_code",
        "toc",
        "attr_list",
        "md_in_html",
        "smarty",
    ])
    html_body = md.convert(body)
    toc = md.toc

    title = frontmatter.get("title", os.path.basename(filepath))
    description = frontmatter.get("description", "")
    date = frontmatter.get("date", "")
    author = frontmatter.get("author", "")
    tags = frontmatter.get("tags", "")

    if tags:
        tags = [t.strip() for t in tags.strip("[]").split(",")]
    else:
        tags = []

    slug = os.path.splitext(os.path.basename(filepath))[0]

    # Build Key Takeaways styling if present
    if "**Key Takeaways:**" in html_body:
        html_body = html_body.replace(
            "<p><strong>Key Takeaways:</strong></p>",
            '<div class="key-takeaways"><h3>Key Takeaways</h3>'
        )
        # Find the next </p> after Key Takeaways and close the div
        html_body = re.sub(
            r'(<div class="key-takeaways">.*?</ul>)\s*</p>',
            r'\1</div>',
            html_body,
            flags=re.DOTALL
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {f'<meta name="description" content="{description}">' if description else ''}
    <style>
        :root {{
            --bg: #0d1117;
            --fg: #c9d1d9;
            --link: #58a6ff;
            --border: #30363d;
            --code-bg: #161b22;
            --header-bg: #161b22;
            --accent: #238636;
            --tag-bg: #1f2937;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--fg);
            line-height: 1.7;
            font-size: 16px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}
        .header {{
            background: var(--header-bg);
            border-bottom: 1px solid var(--border);
            padding: 1.5rem 0;
            margin-bottom: 2rem;
        }}
        .header .container {{ padding-top: 0; padding-bottom: 0; }}
        .meta {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: #8b949e;
        }}
        .tags {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }}
        .tag {{
            background: var(--tag-bg);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            color: #8b949e;
        }}
        h1 {{ font-size: 2rem; margin-bottom: 0.5rem; color: #f0f6fc; }}
        h2 {{ font-size: 1.5rem; margin: 2rem 0 1rem; color: #f0f6fc; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
        h3 {{ font-size: 1.25rem; margin: 1.5rem 0 0.75rem; color: #f0f6fc; }}
        h4 {{ font-size: 1.1rem; margin: 1.25rem 0 0.5rem; color: #f0f6fc; }}
        p {{ margin: 1rem 0; }}
        a {{ color: var(--link); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul, ol {{ margin: 1rem 0; padding-left: 2rem; }}
        li {{ margin: 0.5rem 0; }}
        blockquote {{
            border-left: 4px solid var(--accent);
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            background: rgba(35, 134, 54, 0.1);
            border-radius: 0 6px 6px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            overflow-x: auto;
            display: block;
        }}
        th, td {{
            border: 1px solid var(--border);
            padding: 0.75rem 1rem;
            text-align: left;
        }}
        th {{ background: var(--header-bg); font-weight: 600; }}
        tr:nth-child(even) {{ background: rgba(255,255,255,0.02); }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1.5rem 0;
            border: 1px solid var(--border);
        }}
        .codehilite {{
            background: var(--code-bg);
            border-radius: 8px;
            padding: 1rem;
            margin: 1.5rem 0;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}
        .codehilite pre {{ margin: 0; }}
        .codehilite code {{
            font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
            font-size: 0.875rem;
            line-height: 1.6;
        }}
        .codehilite .c {{ color: #8b949e; font-style: italic; }}
        .codehilite .k {{ color: #ff7b72; }}
        .codehilite .s {{ color: #a5d6ff; }}
        .codehilite .n {{ color: #c9d1d9; }}
        .codehilite .o {{ color: #ff7b72; }}
        .codehilite .p {{ color: #c9d1d9; }}
        .codehilite .mi {{ color: #79c0ff; }}
        .codehilite .nf {{ color: #d2a8ff; }}
        .codehilite .nb {{ color: #ffa657; }}
        .codehilite .bp {{ color: #ffa657; }}
        .codehilite .kn {{ color: #ff7b72; }}
        .codehilite .kc {{ color: #79c0ff; }}
        .codehilite .ow {{ color: #ff7b72; }}
        .codehilite .w {{ color: #6e7681; }}
        .codehilite .m {{ color: #79c0ff; }}
        .codehilite .l {{ color: #a5d6ff; }}
        .codehilite .err {{ color: #f85149; }}
        .codehilite .gr {{ color: #f85149; }}
        .codehilite .gh {{ color: #79c0ff; }}
        .codehilite .gi {{ color: #56d364; }}
        .codehilite .go {{ color: #8b949e; }}
        .codehilite .gp {{ color: #8b949e; }}
        .codehilite .gs {{ font-weight: bold; }}
        .codehilite .gu {{ color: #79c0ff; }}
        .codehilite .gt {{ color: #ff7b72; }}
        .codehilite .gd {{ color: #ffa198; }}
        .codehilite .cm {{ color: #8b949e; font-style: italic; }}
        .codehilite .cp {{ color: #8b949e; font-style: italic; }}
        .codehilite .c1 {{ color: #8b949e; font-style: italic; }}
        .codehilite .cs {{ color: #8b949e; font-style: italic; }}
        .codehilite .se {{ color: #79c0ff; }}
        .codehilite .na {{ color: #c9d1d9; }}
        .codehilite .nc {{ color: #ffa657; }}
        .codehilite .no {{ color: #79c0ff; }}
        .codehilite .nd {{ color: #d2a8ff; }}
        .codehilite .ni {{ color: #ffa657; }}
        .codehilite .ne {{ color: #ffa657; }}
        .codehilite .nl {{ color: #79c0ff; }}
        .codehilite .nn {{ color: #ffa657; }}
        .codehilite .py {{ color: #c9d1d9; }}
        .codehilite .nt {{ color: #7ee787; }}
        .codehilite .nv {{ color: #79c0ff; }}
        .codehilite .vc {{ color: #79c0ff; }}
        .codehilite .vg {{ color: #79c0ff; }}
        .codehilite .vi {{ color: #79c0ff; }}
        .codehilite .vm {{ color: #79c0ff; }}
        .codehilite .ld {{ color: #a5d6ff; }}
        .codehilite .sr {{ color: #79c0ff; }}
        .codehilite .ss {{ color: #a5d6ff; }}
        .codehilite .sx {{ color: #a5d6ff; }}
        .codehilite .s1 {{ color: #a5d6ff; }}
        .codehilite .s2 {{ color: #a5d6ff; }}
        .codehilite .sh {{ color: #a5d6ff; }}
        .codehilite .si {{ color: #79c0ff; }}
        .codehilite .sd {{ color: #a5d6ff; }}
        .codehilite .dl {{ color: #a5d6ff; }}
        .codehilite .sb {{ color: #a5d6ff; }}
        .codehilite .sc {{ color: #a5d6ff; }}
        .codehilite .ch {{ color: #8b949e; font-style: italic; }}
        .codehilite .fm {{ color: #d2a8ff; }}
        .codehilite .cpf {{ color: #8b949e; }}
        .key-takeaways {{
            background: rgba(56, 139, 253, 0.1);
            border: 1px solid rgba(56, 139, 253, 0.3);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }}
        .key-takeaways h3 {{
            margin-top: 0;
            color: #58a6ff;
            border: none;
        }}
        .key-takeaways ul {{
            margin: 0.5rem 0 0;
            padding-left: 1.5rem;
        }}
        .key-takeaways li {{
            margin: 0.5rem 0;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 1.5rem;
            color: #8b949e;
        }}
        .back-link:hover {{
            color: var(--link);
        }}
        .article-list {{
            list-style: none;
            padding: 0;
        }}
        .article-list li {{
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            margin: 1rem 0;
        }}
        .article-list a {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        .article-list .date {{
            color: #8b949e;
            font-size: 0.875rem;
        }}
        footer {{
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            color: #8b949e;
            font-size: 0.875rem;
            text-align: center;
        }}
        .reload-indicator {{
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            background: var(--accent);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }}
        .reload-indicator.active {{
            opacity: 1;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 1rem; }}
            h1 {{ font-size: 1.5rem; }}
            h2 {{ font-size: 1.25rem; }}
            table {{ font-size: 0.875rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <a href="/" class="back-link">← All Articles</a>
            <h1>{title}</h1>
            <div class="meta">
                {f'<span>{date}</span>' if date else ''}
                {f'<span>By {author}</span>' if author else ''}
            </div>
            {f'<div class="tags">{"".join(f"<span class=\"tag\">{t}</span>" for t in tags)}</div>' if tags else ''}
        </div>
    </div>
    <div class="container">
        {html_body}
        <footer>
            <p>Preview Server • Auto-reload enabled • {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </footer>
    </div>
    <div class="reload-indicator" id="reload-indicator">Reloading...</div>
    <script>
        let lastCheck = {int(os.path.getmtime(filepath) if os.path.exists(filepath) else 0)};
        setInterval(async () => {{
            try {{
                const resp = await fetch('/api/modified?file={filepath}');
                const data = await resp.json();
                if (data.modified) {{
                    const el = document.getElementById('reload-indicator');
                    if (el) el.classList.add('active');
                    setTimeout(() => location.reload(), 500);
                }}
            }} catch (e) {{}}
        }}, 1000);
    </script>
</body>
</html>"""
    return html


def render_index() -> str:
    """Render an index page listing all articles."""
    articles = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.md")), reverse=True)

    items = []
    for filepath in articles:
        with open(filepath, "r") as f:
            content = f.read()
        frontmatter, _ = parse_frontmatter(content)
        title = frontmatter.get("title", os.path.basename(filepath))
        date = frontmatter.get("date", "")
        slug = os.path.splitext(os.path.basename(filepath))[0]
        items.append(f"""
            <li>
                <a href="/article/{slug}">{title}</a>
                {f'<br><span class="date">{date}</span>' if date else ''}
            </li>
        """)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Preview</title>
    <style>
        :root {{
            --bg: #0d1117;
            --fg: #c9d1d9;
            --link: #58a6ff;
            --border: #30363d;
            --header-bg: #161b22;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--fg);
            line-height: 1.7;
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }}
        h1 {{ font-size: 2rem; margin-bottom: 1.5rem; color: #f0f6fc; }}
        ul {{ list-style: none; padding: 0; }}
        li {{
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            margin: 1rem 0;
        }}
        a {{ color: var(--link); text-decoration: none; font-size: 1.1rem; font-weight: 600; }}
        a:hover {{ text-decoration: underline; }}
        .date {{ color: #8b949e; font-size: 0.875rem; }}
        footer {{
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            color: #8b949e;
            font-size: 0.875rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Article Preview Server</h1>
        <ul class="article-list">
            {"".join(items) if items else '<li>No articles found. Create markdown files in content/articles/</li>'}
        </ul>
        <footer>
            <p>Preview Server • Bind: {args.host}:{args.port} • {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </footer>
    </div>
</body>
</html>"""
    return html


class PreviewHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the preview server."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(render_index().encode())

        elif path.startswith("/article/"):
            slug = path.split("/article/")[1]
            articles = glob.glob(os.path.join(ARTICLES_DIR, f"{slug}.md"))
            if articles:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(render_article(articles[0]).encode())
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>404 - Article not found</h1>")

        elif path.startswith("/api/modified"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            file_path = parsed.query.split("=")[1] if "=" in parsed.query else ""
            modified = False
            with reload_lock:
                if file_path in file_mtimes:
                    modified = True
                    del file_mtimes[file_path]
            self.wfile.write(json.dumps({"modified": modified}).encode())

        elif path.startswith("/content/images/"):
            filepath = os.path.join(".", path.lstrip("/"))
            if os.path.exists(filepath):
                self.send_response(200)
                ext = os.path.splitext(filepath)[1].lower()
                content_types = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".gif": "image/gif",
                    ".svg": "image/svg+xml",
                    ".webp": "image/webp",
                }
                self.send_header("Content-Type", content_types.get(ext, "application/octet-stream"))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[preview] {args[0]}")


def get_public_ip():
    """Get the server's public IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def main():
    global args
    parser = argparse.ArgumentParser(description="Article Preview Server")
    parser.add_argument("article", nargs="?", help="Article file to preview (optional)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host (default: {DEFAULT_HOST})")
    args = parser.parse_args()

    os.makedirs(ARTICLES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Start file watcher
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, CONTENT_DIR, recursive=True)
    observer.start()

    public_ip = get_public_ip()

    print(f"\n{'='*60}")
    print(f"  Article Preview Server")
    print(f"{'='*60}")
    print(f"  Local:   http://localhost:{args.port}")
    print(f"  Network: http://{public_ip}:{args.port}")
    print(f"{'='*60}")
    print(f"  Watching: {os.path.abspath(CONTENT_DIR)}")
    print(f"  Auto-reload: enabled (polling)")
    print(f"{'='*60}")

    if args.article:
        slug = os.path.splitext(os.path.basename(args.article))[0]
        print(f"\n  Article: {args.article}")
        print(f"  URL: http://{public_ip}:{args.port}/article/{slug}")
        print(f"       http://localhost:{args.port}/article/{slug}")

    print(f"\n  Press Ctrl+C to stop\n")

    server = HTTPServer((args.host, args.port), PreviewHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down preview server...")
        observer.stop()
        server.shutdown()


if __name__ == "__main__":
    main()
