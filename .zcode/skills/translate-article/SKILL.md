---
name: translate-article
description: >-
  本仓库的标准 AI 文献翻译流程：抓取英文原文（文章或文档站），建立「编号+中文标题」目录，
  产出 en/zh markdown、复刻原版排版的 index.html 和以文章中文标题命名的 PDF，并通过一致性自检。
  当用户要求"翻译这篇文章/这篇文档/这个主题并翻译"、"收集整理并翻译"、给出一个 URL 让你翻译、
  或提到"新的一篇"、"下一篇"、"更新 02 的文档重新生成"时使用。任何涉及向本仓库添加译文的工作都应先加载本 skill。
---

# AI 文献翻译

本仓库每篇文献一个独立目录，产出四件套：原文 md、译文 md、复刻原版排版的 index.html、以文章中文标题命名的 PDF（如 `面向长时间运行智能体的高效运行框架.pdf`，**不要叫 index.pdf**）。流程分四步：**取源 → 翻译 → 组装 → 校验**。

## 1. 取源与建目录

1. 编号：`ls` 仓库根目录，取现有 `NN-*` 目录的最大编号 +1，两位数字。
2. 目录名：`NN-中文标题`（标题去掉空格，如 `03-思维链论文翻译`）。
3. 按源类型取原文：
   - **单篇文章**（anthropic.com 等博客/研究页）：`curl -sL <url>` 拉 HTML，解析出：
     - 标题层级（`<h1>-<h4>`，注意 `data-component="Headline"`）；
     - 图片原图 URL（`www-cdn` 等直链，取原始分辨率的 PNG）、每张图在文中的位置和 figcaption 原文；
     - 正文内所有外链及锚文本；
     - 作者/致谢部分。
     下载图片到 `assets/`（文件名用描述性英文 slug），保存原文为 `<slug>.en.md`。
   - **文档站合集**（platform.claude.com 等 Mintlify 站）：先抓 `https://<host>/docs/llms.txt` 拿页面清单，
     再逐页抓 `<页面路径>.md`（Mintlify 的 .md 端点返回干净 markdown，含 frontmatter）。
     保存到 `en/`，文件名加两位编号前缀（`00-`、`01-`…）控制章节顺序。
4. 单篇文章直接 `slug.en.md`/`slug.zh.md` 平铺；合集用 `en/`、`zh/` 子目录，文件名一一对应。

## 2. 翻译

翻译规范、术语表、给子代理的完整 brief 模板见 `references/translation-style.md`——**翻译前必读**。

- 单篇短文：直接翻译。
- 长文或合集（英文总量 > 30KB）：用并行子代理分段翻译（按体量均衡分组，单代理不超过 80KB），
  把 references/translation-style.md 中的 brief 模板原样发给每个代理，只替换文件清单。
- 翻译完成后跑一致性自检（见第 4 节）。

**保真核对**：译文与原页面逐段比对，常被漏译的三类内容——正文中的小节标题、图表的 figcaption、
文末作者致谢。发现缺失先补进 md 再继续。

## 3. 组装 HTML 并渲染 PDF

两条路线，按源类型选：

- **单篇文章**：手写 `index.html` 复刻原页排版（配色、字体、栏宽、图表位置、图注样式）。
  模板与要点（Anthropic 文章风格、打印样式、图表破栏）见 `references/html-and-pdf.md`。
- **文档合集**：复制 `02-提示词工程/` 的 `build.py` + `template.html` 到新目录，
  改封面文案后运行。**不要重写组装脚本**——build.py 已内置三个踩过坑的修复
  （围栏语言标注含空格、CodeGroup 带属性、组件占位符策略），重写容易重新踩坑。详见 references/html-and-pdf.md。

渲染 PDF（屏幕样式与打印样式在同一 HTML 内，靠 `@media print` 切换）：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="目录/文章中文标题.pdf" --virtual-time-budget=20000 \
  "file://$(pwd)/目录/index.html"
```

## 4. 校验（必做，全部通过才算完成）

1. **翻译一致性**：`python3 .zcode/skills/translate-article/scripts/check_translation.py <en文件> <zh文件>`
   对每对文件比对围栏数、组件数、标题数、行数偏差、代码块逐字节一致性。
2. **HTML 无残留**：检查 index.html 中无 `<Accordion`、`<Note>`、`<CodeGroup`、`%%COMP`、`<p>```
   等残留；`<pre>` 数量与 markdown 围栏块数一致。
3. **PDF 溢出**：用 pymupdf（venv 里装，勿污染系统 Python）逐页检查文本是否越出页面边界（见 references/html-and-pdf.md 的脚本段）。
4. **视觉验收**：抽样渲染几页 PNG，交给 pdf:visual-judge 子代理判定；若子代理两次超时失败，
   以 1-3 的程序化校验为准并在交付说明中注明。
5. 更新根 `README.md` 的目录表。

## 交付

最终目录结构（合集形态）：

```
NN-中文标题/
├── assets/          # 原图（仅单篇文章通常有）
├── en/  zh/         # 合集：编号 markdown；单篇：slug.en.md / slug.zh.md
├── build.py + template.html   # 仅合集
├── index.html       # 中文，复刻原版排版
└── 文章中文标题.pdf   # 以文章标题命名，不用 index.pdf
```
