#!/usr/bin/env python3
"""把 app-server.zh.md 组装成复刻 learn.chatgpt.com 文档版式的单页 index.html。

- 代码块高亮配色取自原页 shiki github-light 实测值：
  命令 #6F42C1、旗标 #005CC5、字符串 #032F62、数字/键 #005CC5、默认 #24292E
- 标题 id 用英文原文件标题的 slug（与原页锚点一致，文内 (#anchor) 链接可直接命中）
- 两处 Info callout（原页为带 ⓘ 的提示框，.md 孪生版退化为普通段落）按内容前缀还原
"""
import re
import html as htmllib
import pathlib

import markdown

BASE = pathlib.Path(__file__).resolve().parent
EN = BASE / "app-server.en.md"
ZH = BASE / "app-server.zh.md"
TPL = BASE / "template.html"

CALLOUT_PREFIXES = (
    "如果你要自动化任务或在 CI 中运行 Codex",
    "如果你已经使用 Codex app-server 认证构建了本地或开源应用",
)
INFO_ICON = (
    '<svg class="ico" width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M13 12a1 1 0 1 0-2 0v4a1 1 0 1 0 2 0v-4Zm-1-2.5A1.25 1.25 0 1 0 12 7a1.25 1.25 0 0 0 0 2.5Z"/>'
    '<path fill-rule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2ZM4 12a8 8 0 1 1 16 0 8 8 0 0 1-16 0Z" clip-rule="evenodd"/></svg>'
)

# ── 语法高亮（配色对齐原页 shiki github-light）─────────────────────────────

def _tok(text, cls):
    return '<span class="%s">%s</span>' % (cls, htmllib.escape(text)) if cls else htmllib.escape(text)

def hl_json(code):
    out, i, n = [], 0, len(code)
    tok_re = re.compile(r'"(?:[^"\\]|\\.)*"|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null')
    while i < n:
        m = tok_re.search(code, i)
        if not m:
            out.append(htmllib.escape(code[i:])); break
        out.append(htmllib.escape(code[i:m.start()]))
        t = m.group(0)
        if t.startswith('"'):
            rest = code[m.end():m.end() + 4].lstrip()
            cls = "tk-num" if rest.startswith(":") else "tk-str"   # 键 → 蓝，值 → 深蓝
        elif t[0].isdigit() or t[0] == "-":
            cls = "tk-num"
        else:
            cls = "tk-num"                                          # true/false/null
        out.append(_tok(t, cls))
        i = m.end()
    return "".join(out)

def hl_bash(code):
    out = []
    for line in code.split("\n"):
        if line.lstrip().startswith("#"):
            out.append(_tok(line, "tk-cmt")); continue
        pos, first = 0, True
        tok_re = re.compile(r'"(?:[^"\\]|\\.)*"|\'[^\']*\'|--?[A-Za-z][\w=.-]*|\S+|\s+')
        for m in tok_re.finditer(line):
            t = m.group(0)
            if t.strip() == "":
                out.append(htmllib.escape(t)); continue
            if t.startswith(("-",)) and not t.startswith("--"):
                cls = "tk-flag" if re.match(r"^-{1,2}[A-Za-z]", t) else None
            elif t.startswith("--"):
                cls = "tk-flag"
            elif t[0] in "\"'":
                cls = "tk-str"
            elif first:
                cls = "tk-cmd"                                      # 行首命令
            else:
                cls = "tk-str"                                      # 参数/子命令
            out.append(_tok(t, cls))
            first = False
        out.append("\n")
    return "".join(out)[:-1]

TS_KW = {"import", "from", "const", "let", "var", "as", "if", "else", "return",
         "new", "await", "async", "function", "type", "interface", "export",
         "for", "of", "in", "null", "true", "false", "void", "unknown"}

def hl_ts(code):
    out, i, n = [], 0, len(code)
    tok_re = re.compile(
        r"//[^\n]*|`(?:[^`\\]|\\.)*`|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'"
        r"|\b\d+(?:\.\d+)?\b|\b[A-Za-z_$][\w$]*\b|\s+|.")
    for m in tok_re.finditer(code):
        t = m.group(0)
        if t.startswith("//"):
            out.append(_tok(t, "tk-cmt"))
        elif t[0] in "\"'`":
            out.append(_tok(t, "tk-str"))
        elif t[0].isdigit():
            out.append(_tok(t, "tk-num"))
        elif re.match(r"[A-Za-z_$]", t):
            nxt = code[m.end():m.end() + 2].lstrip()
            if t in TS_KW:
                out.append(_tok(t, "tk-kw"))
            elif nxt.startswith("("):
                out.append(_tok(t, "tk-fn"))
            elif t[0].isupper():
                out.append(_tok(t, "tk-fn"))
            else:
                out.append(htmllib.escape(t))
        else:
            out.append(htmllib.escape(t))
    return "".join(out)

def highlight(code, lang):
    if lang == "json":
        return hl_json(code)
    if lang == "bash":
        return hl_bash(code)
    if lang in ("typescript", "ts"):
        return hl_ts(code)
    return htmllib.escape(code)

# ── 标题锚点（沿用原页英文 slug）───────────────────────────────────────────

def slugify(h):
    s = h.strip().lower().replace("`", "")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    # 原站 slugger 不折叠连续分隔符："pagination & filters" → "pagination--filters"
    return re.sub(r"[\s_]", "-", s).strip("-")

def en_heading_slugs(text):
    slugs = []
    for m in re.finditer(r"^#{1,4} (.+?)\s*$", text, flags=re.M):
        slugs.append(slugify(m.group(1)))
    return slugs

def inject_heading_ids(body, slugs):
    idx = [0]
    def repl(m):
        if idx[0] >= len(slugs):
            return m.group(0)
        sid = slugs[idx[0]]; idx[0] += 1
        inner = '%s<a class="anchor" href="#%s">#</a>' % (m.group(2), sid)
        return '<%s id="%s">%s</%s>' % (m.group(1), sid, inner, m.group(1))
    return re.sub(r"<(h[234])>(.*?)</\1>", repl, body, flags=re.S)

# ── 主流程 ────────────────────────────────────────────────────────────────

def main():
    zh = ZH.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")

    # 模板已渲染 h1 标题区，去掉 md 自身的文档标题（避免重复 h1）
    zh = re.sub(r"^# .+?\n+", "", zh, count=1)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    body = md.convert(zh)

    # 代码块：高亮 + 包一层 codewrap（悬停复制按钮）
    pre_re = re.compile(r'<pre><code class="language-([\w-]+)">(.*?)</code></pre>', re.S)
    n_pre = [0]
    def fix_pre(m):
        n_pre[0] += 1
        lang, inner = m.group(1), m.group(2)
        code = htmllib.unescape(inner)
        return ('<div class="codewrap"><button class="copy-btn" type="button">复制</button>'
                '<pre><code class="language-%s">%s</code></pre></div>'
                % (htmllib.escape(lang), highlight(code, lang)))
    body = pre_re.sub(fix_pre, body)

    # Info callout 还原
    for prefix in CALLOUT_PREFIXES:
        pat = re.compile(r"<p>(%s.*?)</p>" % re.escape(prefix), re.S)
        body = pat.sub(lambda m: '<div class="callout">%s<div class="callout-body"><p>%s</p></div></div>'
                       % (INFO_ICON, m.group(1)), body, count=1)

    # 标题锚点
    body = inject_heading_ids(body, en_heading_slugs(en))

    tpl = TPL.read_text(encoding="utf-8")
    out = tpl.replace("{{CONTENT}}", body)
    (BASE / "index.html").write_text(out, encoding="utf-8")
    print("index.html written: %d KB, %d code blocks" % (len(out) // 1024, n_pre[0]))

if __name__ == "__main__":
    main()
