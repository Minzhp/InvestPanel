# -*- coding: utf-8 -*-
"""把投资面板打包成可部署目录 invest-publish/。

做的事：
  1. 复制 index.html 并注入 <meta robots noindex>
  2. 复制四个数据目录（trading_records / dividend_records / payment_records / navs）
  3. 生成 Cloudflare Pages 的 _headers（禁止搜索引擎索引）

用法：
    python build_publish.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "invest-publish"
DATA_DIRS = ["trading_records", "dividend_records", "payment_records", "navs"]

ROBOTS_META = '<meta name="robots" content="noindex,nofollow">\n'

HEADERS = """/*
  X-Robots-Tag: noindex, nofollow
"""


def main():
    src_html = ROOT / "index.html"
    if not src_html.exists():
        sys.exit("错误：未找到 index.html")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    html = src_html.read_text(encoding="utf-8")
    if "</head>" not in html:
        sys.exit("错误：index.html 结构异常，缺少 </head>")

    html = html.replace("</head>", ROBOTS_META + "</head>", 1)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / "_headers").write_text(HEADERS, encoding="utf-8")

    count = 2
    for d in DATA_DIRS:
        src = ROOT / d
        if not src.exists():
            print(f"  ! 跳过（目录不存在）: {d}")
            continue
        shutil.copytree(src, OUT / d)
        count += sum(1 for p in src.rglob("*") if p.is_file())

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"已生成 {OUT}")
    print(f"  文件 {count} 个，共 {total / 1024:.1f} KB")
    print("下一步部署：")
    print(f'  npx.cmd wrangler pages deploy "{OUT}" --project-name=your-project-name')


if __name__ == "__main__":
    main()
