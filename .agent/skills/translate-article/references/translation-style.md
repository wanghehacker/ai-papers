# 翻译规范与术语表

## 术语表（保持全仓库一致）

首次出现时中英对照，之后只用中文；右列为固定译法：

| 英文 | 译法 |
|---|---|
| prompt engineering | 提示词工程 |
| system prompt | 系统提示词 |
| few-shot prompting | 少样本提示（few-shot prompting） |
| chain of thought | 思维链（chain of thought） |
| extended thinking | 扩展思考（extended thinking） |
| adaptive thinking | 自适应思考（adaptive thinking） |
| thinking block | thinking 块 |
| agent / subagent | 智能体（agent）/ 子智能体（subagent） |
| context window | 上下文窗口 |
| compaction | 压缩（compaction） |
| long-horizon | 长时程（long-horizon） |
| eval | 评测（eval） |
| hallucination | 幻觉 |
| guardrail | 护栏（guardrail） |
| jailbreak / prompt injection | 越狱 / 提示词注入（prompt injection） |
| prefill | 预填充（prefill） |
| prompt chaining | 提示词链（prompt chaining） |
| tool use / tool call | 工具使用 / 工具调用 |
| effort level | effort 级别（effort level） |

**保留英文不译**：prompt、token、LLM、XML、JSON、API、MCP、Claude、模型名（Claude Opus 5.5 等）、
工具名（Bash/Python）、代码与提示词示例（引号内作为示例的英文 prompt 原样保留）。

## 硬性规则

1. 完整性：逐段翻译，不省略、不概括、不调序。frontmatter 的 title/description 译为中文，url 原样保留。
2. 代码块（含围栏标记、语言标注、内容、注释）逐字节原样复制，禁止任何改动。
3. 文档站的 JSX 组件标签（`<Accordion>`、`<CardGroup>`、`<Card>`、`<Note>`、`<Tip>`、`<Info>`、`<CodeGroup>`）
   结构与 href 等属性原样保留，只翻译 title 属性值和标签内非代码正文。
4. URL 一律不变，仅译链接文字。
5. Markdown 结构（标题层级、列表、表格、加粗斜体）与原文一一对应，表格单元格全部翻译。
6. 中文标点（，。：“”），技术文档语气，“你”称呼读者。

## 大文档并行翻译（子代理 brief 模板）

英文总量 > 30KB 时按体量均衡分组（单代理 ≤ 80KB），每个代理用下面模板，替换源/目标文件清单即可：

```
你是 AI 文献翻译工程的翻译代理。任务：把 N 篇文档从英文完整翻译为中文，写入指定文件。

源文件与目标文件（一一对应）：
1. <绝对路径 en> → <绝对路径 zh>
（按上面"硬性规则"与"术语表"逐条列出，术语表全文粘贴）

写入方式：单篇可用一次 Write；超过 ~30KB 的分块写入：第一块用 Write，后续块用 Bash 追加：
  cat >> 目标文件 <<'ZHMD_APPEND_EOF'
  （本块内容）
  ZHMD_APPEND_EOF
每块 250–350 行。切勿一次 Write 硬塞全文导致截断。

完成后自检（对每对源/目标文件，不一致必须修复）：
- grep -c '^```' 相等；grep -c '<Accordion'、'<Note>'、'<Tip>'、'<Card '、'<CodeGroup' 相等
- grep -cE '^#{1,4} ' 相等；行数偏差 ≤ ±15%
- 抽取代码块内容用 cmp/diff 逐字节比对（推荐用 sed 从源文件抽取代码块直接复制进译文）
最后报告：目标文件路径、代码块数、标题数、自检结果。
```

要点：分块写入防截断；让代理直接从源文件复制代码块（而非重打），保证逐字节一致；
自检指标全部量化，代理能自行闭环修复。
