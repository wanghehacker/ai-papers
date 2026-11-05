# AGENTS.md

给在本仓库工作的 AI 智能体（以及人类协作者）的项目说明。动手前请先读完本文，
涉及「翻译一篇新文献」时还必须加载 `.agent/skills/translate-article/SKILL.md`。

## 这是什么

AI 文献中文翻译库：把 AI 领域的文章、论文、官方文档翻译成中文，并按原页面排版
复刻成自包含 HTML，再渲染成以文章中文标题命名的 PDF。**每篇文献一个独立目录**：

```
NN-中文标题/                     # NN 两位数字递增，如 04-面向长时间运行智能体的高效运行框架
├── assets/                      # 原文页面引用的图片/图表（原图下载，不重绘、不二次截图）
├── slug.en.md                   # 英文原文（单篇文章形态）
├── slug.zh.md                   # 中文译文
├── en/  zh/                     # 文档合集形态：编号 markdown 分章（00-、01-…）
├── build.py + template.html      # 仅合集：zh/*.md → index.html 组装脚本与模板
├── index.html                   # 中文自包含 HTML，复刻原版排版（图片走 assets/ 相对路径）
└── 文章中文标题.pdf              # Chrome headless 渲染产物，不叫 index.pdf
```

当前目录：`01` 单篇文章、`02` 十章文档合集、`03` 协议参考文档、`04` 单篇文章。
完整清单与原文链接见 `README.md` 的目录表——**新增文献后必须同步更新该表**。

## 目录导航

| 路径 | 作用 |
|---|---|
| `.agent/skills/translate-article/SKILL.md` | 标准翻译流程（取源 → 翻译 → 组装 → 校验），**翻译前必读** |
| `.agent/skills/translate-article/references/translation-style.md` | 术语表、硬性规则、并行子代理 brief 模板 |
| `.agent/skills/translate-article/references/html-and-pdf.md` | 两种 HTML 路线要点、`build.py` 踩坑记录、PDF 校验脚本 |
| `.agent/skills/translate-article/scripts/check_translation.py` | en/zh 一致性自检（CI 级必跑） |
| `README.md` | 面向读者的仓库说明、目录表、许可 |

## 环境

- Python 依赖装在仓库根的 `.venv/`（**不入库**）：`markdown`（组装 HTML）、`pymupdf`（PDF 校验）。
  一律用 `.venv/bin/python`，**不要污染系统 Python**（受 PEP 668 保护，`pip install` 会失败）。
- PDF 渲染依赖本机 Chrome：

  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 \
    --print-to-pdf="目录/文章中文标题.pdf" "file://$(pwd)/目录/index.html"
  ```

- 远程：`origin` = `https://github.com/wanghehacker/ai-papers.git`（fetch）、
  `git@github.com:wanghehacker/ai-papers.git`（push，走 SSH key，无需 token）。
  本机无 credential helper，**不要改成让 git 交互式要密码的方式 push**。

## 硬性规则

1. **英文原文不可改**：`*.en.md`、`en/*.md` 是从原站抓取的对照文本，只读。任何修正只改 `.zh.md`。
2. **代码块逐字节一致**：译文中的围栏代码块（围栏标记、语言标注、内容、注释）必须与原文完全相同。
3. **URL 不变**：只译链接文字；所有外链指向原始 URL。
4. **完整性**：不省略、不概括、不调序。易漏的三类内容——正文小节标题、图注（figcaption）、文末作者致谢。
5. **术语一致**：按 `references/translation-style.md` 的术语表（compaction→压缩、long-horizon→长时程 等）。
6. **`build.py` / `template.html` 只复制不重写**：这两个文件已内置三个修复（围栏语言标注含空格、
   `CodeGroup` 带属性、组件用占位符而非 `md_in_html`），重写极易重新踩坑。新合集直接把
   `02-提示词工程/` 的这两个文件复制过去改封面文案。
7. **PDF 许可声明不可删**：每份 PDF 末页都有一行 `CC BY-NC-SA 4.0` 授权声明（01/04 在 colophon，
   02 在 `.doc-footer`，03 在 `.article-footer`）。改模板后重新渲染要确认它还在。
8. **原始归属**：英文原文与配图著作权归 Anthropic / OpenAI 等原发布方，不在 CC 许可范围内；
   不要在 PDF 或页面上把自己标成原文作者。
9. **未经确认不要 `git push`**：本地 `git add` / `git commit` 可以自行完成，但推送到远端前必须
   先向用户说明「要推哪些 commit、改了什么」并得到明确同意。用户没点头就只停在本地，
   交付时说清楚「已提交未推送」，不要自作主张推上去。

## 改完必须校验

```bash
# 1. 译文一致性（单篇 / 合集目录）
.venv/bin/python .agent/skills/translate-article/scripts/check_translation.py <en.md> <zh.md>
.venv/bin/python .agent/skills/translate-article/scripts/check_translation.py -p 02-提示词工程/en 02-提示词工程/zh

# 2. HTML 无组件残留（应输出 0），<pre> 数应与 zh markdown 围栏块数一致
grep -c -E '<Accordion|<Note>|<CodeGroup|%%COMP|<p>```' 目录/index.html

# 3. PDF 无文字溢出（pymupdf 逐页判断越界词）
#    脚本见 references/html-and-pdf.md「PDF 渲染与校验」段
```

改完译文或模板后 **PDF 必须重新渲染**，否则仓库里的 PDF 与 markdown 不一致。
提交前 `git status` 确认没有把 `.venv/`、`.zcode/document-imports/` 带进去。

## 常见坑

- **导入 markdown**：`build.py` 需要 `.venv/bin/python` 运行，系统 `python3` 没有 `markdown` 包。
- **PDF 多出空白页**：往末页页脚追加内容时容易溢出成只剩一行的孤儿页；页脚尽量内联成一句，
  渲染后检查末页字符数（正常数百字以上）。
- **`.agent/skills/` 是自定义路径**：不在工具的默认 skill 搜索目录内，需显式读 `SKILL.md` 才能加载。
- **中文路径**：目录名含中文，`git` 输出会转义；需要看清路径时用 `git -c core.quotepath=false status`。

## 提交约定

- 一个逻辑改动一个 commit，中文说明；译文初版、PDF 渲染、模板/流程修改分开提交更易回溯。
- 提交信息写清「改了什么 + 校验结果」，例如：
  `PDF 末页加一行 CC BY-NC-SA 4.0 许可声明` + `校验：4 个 PDF 均无文字溢出，页数不变（7/86/49/6）`。
- 推送：`git push`（origin 已配好 pushurl，main 跟踪 `origin/main`）。**执行前须经用户确认**（见硬性规则第 9 条），
  确认后再推，推送后回报 commit hash 与远端状态。
