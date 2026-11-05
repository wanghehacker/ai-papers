# AI 文献翻译库

翻译各种 AI 相关的文献（文章、论文、博客等）。每篇文献一个独立目录，目录名格式：

> 翻译新文献时使用工程内 skill：`.zcode/skills/translate-article/`（含完整流程、术语表、
> 组装脚本踩坑记录和 en/zh 一致性自检脚本 `check_translation.py`）。

```
NN-中文标题/            # 编号两位数字 + 文章中文标题，如 01-面向AI智能体的有效上下文工程
├── assets/             # 原文页面引用的图片、图表（从原站下载，原样保留）
├── slug.en.md          # 英文原文（Markdown）
├── slug.zh.md          # 中文译文（Markdown）
├── index.html          # 复刻原页面排版的中文 HTML（自包含，图片走相对路径 assets/）
└── 文章标题.pdf         # 由 index.html 渲染的 PDF（以文章中文标题命名，如 01 目录为「面向AI智能体的有效上下文工程.pdf」）
```

## 翻译规范

- 译文结构与原文页面保持一致：标题层级（h2/h3/h4）、段落顺序、图表位置均按原页面还原，不遗漏原文的小节标题、图注、作者致谢等内容。
- 图表从原站下载原图放入 `assets/`，HTML/PDF 中原样嵌入（不重绘、不二次截图）。
- `index.html` 复刻原页面的视觉风格（配色、衬线正文、居中阅读栏、mono 图注），文内超链接全部保留并指向原始 URL。
- HTML 通过 headless Chrome 渲染为 PDF：

  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="目录/文章标题.pdf" "file://$(pwd)/目录/index.html"
  ```

## 目录

| 编号 | 标题 | 原文 |
|---|---|---|
| 01 | 面向 AI 智能体的有效上下文工程 | [Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) |
| 02 | 提示词工程（10 章合集） | [Prompt engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) |
| 03 | Codex 应用服务器（协议参考文档） | [Codex App Server](https://learn.chatgpt.com/docs/app-server) |
| 04 | 面向长时间运行智能体的高效运行框架 | [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) |

## 许可

本仓库的中文译文、译文排版与翻译流程文档以 [CC BY-NC-SA 4.0](LICENSE) 授权
（署名—非商业性使用—相同方式共享 4.0 国际）。转载或改编请注明来源与作者，
保留相同协议，且不得用于商业用途。

英文原文与原文配图的著作权归原作者/原发布方所有，不在本许可范围内，仅作翻译对照与学习研究之用。

## 合集结构

多页文档合集的变体结构（见 `02-提示词工程/`）：`en/`、`zh/` 子目录存放编号的逐页 markdown，`build.py` + `template.html` 把 `zh/*.md` 组装成单页 docs 风格 `index.html`（屏幕端左侧栏导航，打印时自动切换为封面 + 目录 + 分章），再渲染以文章中文标题命名的 PDF（如 `提示词工程.pdf`）。文内互相引用的原文链接会被改写为章节内锚点。
