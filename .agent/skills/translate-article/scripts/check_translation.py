#!/usr/bin/env python3
"""翻译一致性自检：对比 en/zh markdown 的结构指标。

用法：
  check_translation.py <en.md> <zh.md>                # 单对文件
  check_translation.py -p <en目录> <zh目录>            # 目录下同名文件逐对检查

检查项（全部通过 exit 0，否则 exit 1）：
  1. 围栏代码块数量一致（围栏状态机，正确处理 4 反引号嵌套与 ~~~）
  2. 代码块内容逐字节一致（含语言标注首 token）
  3. JSX 组件数量一致（Accordion/Card/CardGroup/Note/Tip/Info/CodeGroup）
  4. 标题数量一致（# ~ ####）
  5. 行数偏差 ≤ 15%
  6. frontmatter 的 url 一致
"""
import re
import sys
import pathlib

FENCE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(\s*)(.*)$")
HEADING = re.compile(r"^#{1,4} ", re.M)
COMPONENTS = ["<Accordion", "<Card ", "<CardGroup", "<Note>", "<Tip>", "<Info>", "<CodeGroup"]


def strip_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def split_fences(text):
    """返回 (无代码块的正文, [代码块内容...])。按围栏状态机走，改写过的语言标注（build.py
    的 sanitize_fences 会丢掉 wrap 等属性）按首 token 对齐比较。"""
    open_char, open_len = None, 0
    body_lines, blocks, cur = [], [], []
    for line in text.split("\n"):
        m = FENCE.match(line)
        if not m:
            if open_char:
                cur.append(line)
            else:
                body_lines.append(line)
            continue
        indent, fence, info = m.group(1), m.group(2), m.group(4).strip()
        if open_char is None:
            open_char, open_len = fence[0], len(fence)
            cur = [indent + fence + (info.split()[0] if info else "")]
        elif fence[0] == open_char and len(fence) >= open_len and not info:
            blocks.append("\n".join(cur))
            open_char, cur = None, []
        else:
            cur.append(line)
    if cur:  # 未闭合围栏：并回正文以暴露问题
        body_lines.extend(cur)
    return "\n".join(body_lines), blocks


def check(en_path, zh_path):
    en = pathlib.Path(en_path).read_text(encoding="utf-8")
    zh = pathlib.Path(zh_path).read_text(encoding="utf-8")
    en_meta, en_body = strip_frontmatter(en)
    zh_meta, zh_body = strip_frontmatter(zh)
    problems = []

    en_text, en_blocks = split_fences(en_body)
    zh_text, zh_blocks = split_fences(zh_body)
    if len(en_blocks) != len(zh_blocks):
        problems.append(f"围栏代码块数不一致: en={len(en_blocks)} zh={len(zh_blocks)}")
    else:
        for i, (a, b) in enumerate(zip(en_blocks, zh_blocks)):
            if a != b:
                problems.append(f"代码块 #{i+1} 内容不一致: en 首行={a.splitlines()[0][:40]!r}")

    for comp in COMPONENTS:
        c_en, c_zh = en_text.count(comp), zh_text.count(comp)
        if c_en != c_zh:
            problems.append(f"组件 {comp}: en={c_en} zh={c_zh}")

    h_en, h_zh = len(HEADING.findall(en_text)), len(HEADING.findall(zh_text))
    if h_en != h_zh:
        problems.append(f"标题数不一致: en={h_en} zh={h_zh}")

    l_en, l_zh = len(en_body.split("\n")), len(zh_body.split("\n"))
    if l_en and abs(l_zh - l_en) / l_en > 0.15:
        problems.append(f"行数偏差 {abs(l_zh-l_en)/l_en:.0%} 超过 15% (en={l_en} zh={l_zh})")

    if en_meta.get("url") and en_meta.get("url") != zh_meta.get("url"):
        problems.append(f"frontmatter url 不一致: {en_meta.get('url')!r} vs {zh_meta.get('url')!r}")

    status = "PASS" if not problems else "FAIL"
    print(f"[{status}] {pathlib.Path(en_path).name}")
    for p in problems:
        print(f"    - {p}")
    return not problems


def main():
    args = sys.argv[1:]
    ok = True
    if len(args) == 3 and args[0] == "-p":
        en_dir, zh_dir = pathlib.Path(args[1]), pathlib.Path(args[2])
        for en_f in sorted(en_dir.glob("*.md")):
            zh_f = zh_dir / en_f.name
            if not zh_f.exists():
                print(f"[FAIL] {en_f.name}: 缺少对应译文 {zh_f}")
                ok = False
                continue
            ok = check(en_f, zh_f) and ok
    elif len(args) == 2:
        ok = check(args[0], args[1])
    else:
        sys.exit(__doc__)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
