"""本地静态服务：与 python -m http.server 相同，但禁用缓存，避免页面/数据更新后浏览器仍显示旧内容。"""
import http.server
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8686


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), NoCacheHandler) as srv:
        print(f"Serving at http://localhost:{PORT}/index.html (no-store)")
        srv.serve_forever()
