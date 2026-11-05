# HTML 排版与 PDF 渲染

## 路线一：单篇文章（复刻原页面）

参照 `01-面向AI智能体的有效上下文工程/index.html`。要点：

- **自包含单文件**：CSS 内嵌，图片走 `assets/` 相对路径，无外部依赖（离线可开、可渲染）。
- **复刻原站视觉**：从原页面 HTML/CSS 提取品牌变量。Anthropic 文章页实测值：
  背景 `#FAF9F5`（slate-050）、正文 `#141413`、分隔线 `#E8E6DC`、强调色 `#D97757`；
  正文衬线（中文回退 Songti SC）、图注/眉线用 mono 小字。
- **阅读栏 ~680px 居中；图表栏更宽**（原站 media-column 会破栏）：屏幕端
  `width: min(920px, calc(100vw - 48px)); margin: 40px calc((632px - min(...))) / 2) 44px;`
- **图片放 `<figure class="media">`**，figcaption 用原页面 figcaption 的译文，位置与原文一致（常在图下方）。
- **文内链接全部保留**并指向原始 URL；新增的"原文↗"链接放 byline 或页脚。
- **打印样式**（`@media print` + `@page { size: A4; margin: 15mm 14mm 17mm }`）：
  字号切换为 pt（正文 10.5pt，标题 21/14/12/10.5pt）；`figure { break-inside: avoid }`；
  `h2/h3/h4 { break-after: avoid }`；`print-color-adjust: exact` 保住背景色。

## 路线二：文档合集（build.py 组装）

参照 `02-提示词工程/`（build.py + template.html + zh/*.md → index.html）。直接复制这两个文件改文案，
**不要重写**。已内置的三个关键修复（踩坑记录，勿回退）：

1. **围栏语言标注含空格**：python-markdown 的 fenced_code 不认 ` ```text wrap `（info string 含空格时
   整行不当围栏，开栏被吞进段落、闭栏反而开新块，代码块成对丢失）。build.py 的 `sanitize_fences()`
   用围栏状态机只改写开栏行：保留第一个 token 作语言，丢弃 `wrap` 等显示属性；闭栏与代码内容逐字节不动，
   并正确处理 4 反引号嵌套。
2. **CodeGroup 可带属性**（如 `<CodeGroup exclude="shell">`）：正则必须 `<CodeGroup[^>]*>`。
3. **组件内容转换用占位符策略**：不要用 md_in_html 扩展——它对组件内缩进围栏代码的处理不可靠。
   build.py 的做法：组件整块提取 → 内容 dedent 后单独跑 markdown 转换 → 存入 frags 列表，
   正文里留 `%%COMPn%%` 占位符，转换后回填。

其它内置能力：frontmatter 解析（title 作章标题）、h2 锚点生成与侧栏目录、
用英文原文件的标题 slug 建立 en锚点→中文锚点映射（跨页链接改写为 `#chNN` / `#chNN-sK`）、
Accordion→details、Note/Info/Tip→callout、CardGroup/Card→链接卡片。

渲染后检查 index.html：`<pre>` 数 = zh markdown 围栏块数；无 `<Accordion`、`<Note>`、`<CodeGroup`、
`%%COMP`、`<p>``` ` 残留。

## PDF 渲染与校验

渲染命令见 SKILL.md 第 3 节。渲染后用 pymupdf 校验（系统 Python 受 PEP 668 保护，先
`python3 -m venv /tmp/pdfvenv && /tmp/pdfvenv/bin/pip install pymupdf`）：

```python
import pymupdf
doc = pymupdf.open("文章中文标题.pdf")
for i, page in enumerate(doc):
    r = page.rect
    over = [w for w in page.get_text("words") if w[2] > r.width - 3 or w[3] > r.height - 3]
    if over:
        print("page", i + 1, "overflow", len(over), over[0][4][:40])
# 抽样渲染验收页
for p in [0, 1, 2, len(doc) // 2, len(doc) - 1]:
    doc[p].get_pixmap(dpi=100).save(f"/tmp/judge_pg{p+1}.png")
```

视觉验收：把抽样 PNG 交给 pdf:visual-judge 子代理（一次不超过 5-6 页，页数多会超时）。
判定失败或子代理连续两次超时：以程序化校验结果为准，交付说明中如实注明视觉验收未完成。
