#!/usr/bin/env python3
"""把 zh/*.markdown 组装成 docs 风格的单页 HTML（屏幕侧栏 + 打印分章）。"""
import re, glob, html, sys, pathlib

import markdown

BASE = pathlib.Path(__file__).resolve().parent
ZH = BASE / "zh"

CHAPTERS = []  # (num, file, meta, html_body, [(id, title)])

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]

def slugify(h):
    s = h.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", s).strip("-")

FENCE_LINE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(\s*)(.*)$")

def sanitize_fences(text):
    """python-markdown 不接受含空格的围栏语言标注（如 ```text wrap）。
    按围栏状态机只改写开栏行：保留第一个 token 作为语言，丢弃 wrap 等显示属性。
    代码块内容与闭栏行逐字节不动。"""
    open_char, open_len = None, 0
    out = []
    for line in text.split("\n"):
        m = FENCE_LINE.match(line)
        if not m:
            out.append(line)
            continue
        indent, fence, info = m.group(1), m.group(2), m.group(4).strip()
        if open_char is None:
            if info:
                out.append(indent + fence + info.split()[0])
            else:
                out.append(line)
            open_char, open_len = fence[0], len(fence)
        else:
            if fence[0] == open_char and len(fence) >= open_len and not info:
                open_char, open_len = None, 0
            out.append(line)
    return "\n".join(out)

def convert_md(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    return md.convert(text)

def dedent(text):
    lines = text.split("\n")
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    m = min(indents) if indents else 0
    return "\n".join(l[m:] if len(l) >= m else l for l in lines)

def _card_html(attrs, inner):
    t = re.search(r'title="([^"]*)"', attrs)
    h = re.search(r'href="([^"]*)"', attrs)
    title = html.escape(t.group(1)) if t else ""
    href = html.escape(h.group(1)) if h else "#"
    text = html.escape(re.sub(r"\s+", " ", inner).strip())
    return ('<a class="card" href="%s"><span class="card-title">%s <span class="card-arrow">&#8599;'
            '</span></span><span class="card-text">%s</span></a>') % (href, title, text)

def process_components(body, stash):
    """把 Mintlify JSX 组件整块转换为 HTML 片段并暂存为占位符。"""

    # CardGroup / Card → 链接卡片
    def cardgroup(m):
        cards = re.findall(r"<Card ([^>]*)>(.*?)</Card>", m.group(1), re.S)
        return stash('<div class="card-group">%s</div>' % "".join(_card_html(a, t) for a, t in cards))
    body = re.sub(r"<CardGroup[^>]*>(.*?)</CardGroup>", cardgroup, body, flags=re.S)
    body = re.sub(r"<Card ([^>]*)>(.*?)</Card>", lambda m: stash(_card_html(m.group(1), m.group(2))), body, flags=re.S)

    # Accordion → details/summary（内部 markdown 单独转换）
    def accordion(m):
        attrs, inner = m.group(1), m.group(2)
        t = re.search(r'title="([^"]*)"', attrs)
        title = html.escape(t.group(1)) if t else "示例"
        inner_html = convert_md(dedent(inner))
        return stash('<details class="acc" open>\n<summary>%s</summary>\n'
                     '<div class="acc-body">%s</div>\n</details>' % (title, inner_html))
    body = re.sub(r"<Accordion([^>]*)>(.*?)</Accordion>", accordion, body, flags=re.S)

    # Note / Info / Tip → callout
    for tag, cls in (("Note", "co-note"), ("Info", "co-note"), ("Tip", "co-tip")):
        def callout(m, cls=cls):
            return stash('<div class="callout %s">%s</div>' % (cls, convert_md(dedent(m.group(1)))))
        body = re.sub(r"<%s>(.*?)</%s>" % (tag, tag), callout, body, flags=re.S)

    # CodeGroup → 代码块分组（打印/单页场景退化为紧凑堆叠）
    def codegroup(m):
        return stash('<div class="code-group">%s</div>' % convert_md(dedent(m.group(1))))
    body = re.sub(r"<CodeGroup[^>]*>(.*?)</CodeGroup>", codegroup, body, flags=re.S)

    return body

def convert(body):
    body = sanitize_fences(body)
    frags = []
    def stash(frag):
        frags.append(frag)
        return "\n\n%%COMP%d%%\n\n" % (len(frags) - 1)
    body = process_components(body, stash)
    out = convert_md(body)
    for i, frag in enumerate(frags):
        out = out.replace("<p>%%COMP%d%%</p>" % i, frag).replace("%%COMP%d%%" % i, frag)
    return out

def add_h2_ids(num, body_html, sections):
    """给 h2 分配 id，收集侧栏小节。"""
    count = [0]
    def repl(m):
        count[0] += 1
        sid = "ch%02d-s%d" % (num, count[0])
        title = re.sub(r"<[^>]+>", "", m.group(1))
        sections.append((sid, title))
        return '<h2 id="%s">%s</h2>' % (sid, m.group(1))
    return re.sub(r"<h2>(.*?)</h2>", repl, body_html, flags=re.S)

def main():
    files = sorted(glob.glob(str(ZH / "*.md")))
    en_files = sorted(glob.glob(str(BASE / "en" / "*.md")))
    chapters = []
    url_map = {}   # 原页面 URL → 章节锚点
    anchor_map = {}  # (页面url, en锚点) → 章节内锚点

    for idx, f in enumerate(files):
        num = int(pathlib.Path(f).name[:2])
        meta, body = parse_frontmatter(pathlib.Path(f).read_text(encoding="utf-8"))
        html_body = convert(body)
        sections = []
        html_body = add_h2_ids(num, html_body, sections)
        chapters.append(dict(num=num, meta=meta, body=html_body, sections=sections))
        if meta.get("url"):
            url_map[meta["url"]] = "ch%02d" % num

    # 用英文原文件的小节锚点建立 en锚点 → 章内锚点 映射
    for ch, ef in zip(chapters, en_files):
        _, en_body = parse_frontmatter(pathlib.Path(ef).read_text(encoding="utf-8"))
        en_h2s = re.findall(r"^## +(.+?)\s*$", en_body, flags=re.M)
        for i, h in enumerate(en_h2s):
            if i < len(ch["sections"]):
                anchor_map[(ch["meta"].get("url", ""), slugify(h))] = ch["sections"][i][0]

    def rewrite_links(html_text):
        def rep(m):
            url = m.group(1)
            frag = ""
            if "#" in url:
                base, frag = url.split("#", 1)
            else:
                base = url
            if base in url_map:
                target = url_map[base]
                if frag and (base, frag) in anchor_map:
                    target = anchor_map[(base, frag)]
                return 'href="#%s"' % target
            return 'href="%s"' % url
        return re.sub(r'href="(https?://platform\.claude\.com[^"]*)"', rep, html_text)

    for ch in chapters:
        ch["body"] = rewrite_links(ch["body"])

    # ── 侧栏 ──
    side_items = []
    for ch in chapters:
        subs = "".join('<a class="side-sub" href="#%s">%s</a>' % (sid, html.escape(t)) for sid, t in ch["sections"])
        side_items.append(
            '<div class="side-item"><a class="side-ch" href="#ch%02d">%02d · %s</a>%s</div>'
            % (ch["num"], ch["num"], html.escape(ch["meta"].get("title", "")),
               '<div class="side-subs">%s</div>' % subs if subs else ""))
    sidebar = "\n".join(side_items)

    # ── 章节正文 ──
    chap_html = []
    for ch in chapters:
        src = ch["meta"].get("url", "")
        desc = ch["meta"].get("description", "")
        chap_html.append(
            '<section class="chapter" id="ch%02d">\n'
            '<p class="chap-eyebrow">第 %02d 章 · <a class="chap-src" href="%s">原文 ↗</a></p>\n'
            '<h1>%s</h1>\n<p class="chap-desc">%s</p>\n%s\n</section>'
            % (ch["num"], ch["num"], html.escape(src),
               html.escape(ch["meta"].get("title", "")), html.escape(desc), ch["body"]))
    content = "\n".join(chap_html)

    # ── 打印目录页 ──
    toc_items = "".join(
        '<li><span class="toc-num">%02d</span><a href="#ch%02d">%s</a></li>'
        % (ch["num"], ch["num"], html.escape(ch["meta"].get("title", "")))
        for ch in chapters)

    tpl = (BASE / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{SIDEBAR}}", sidebar)
              .replace("{{CONTENT}}", content)
              .replace("{{TOC}}", toc_items))
    (BASE / "index.html").write_text(out, encoding="utf-8")
    print("index.html written: %d chapters, %d KB" % (len(chapters), len(out) // 1024))

if __name__ == "__main__":
    main()
