---
title: Claude Opus 4.8 提示词指南
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
description: Claude Opus 4.8 的行为差异与提示词模式，涵盖冗长度、effort 校准、工具使用、子智能体与前端默认风格。
---

本指南介绍 Claude Opus 4.8 特有的提示词（prompt）模式。关于从 Claude Opus 4.8 迁移到 Claude Opus 5.5 涉及的 API 变更，请参阅[从 Claude Opus 4.8 迁移到 Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-4-8)。关于适用于当前所有 Claude 模型的技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

Claude Opus 4.8 在长时程（long-horizon）智能体（agent）工作、知识型工作、视觉和记忆任务上有独特优势。它在现有的 Claude Opus 4.7 提示词上开箱即用地表现良好。以下模式涵盖最常需要调优的行为。

<Note>
  关于自 Claude Opus 4.7 以来的 API 参数变更——默认 1M 上下文窗口（context window）与对话中途系统消息——请参阅[从 Claude Opus 4.7 迁移到 Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-47)，其中涵盖了通往 Claude Opus 5.5 途中的相同变更；Claude Opus 4.8 与这些行为一致。
</Note>

## 回复长度与冗长度

Claude Opus 4.8 会根据它对任务复杂度的估计来校准回复长度，而不是默认采用固定的冗长度。这通常意味着简单查询的答案更短，开放式分析的答案长得多。

如果你的产品依赖某种特定的输出风格或冗长度，你可能需要调优提示词。例如，要降低冗长度，可以添加：

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

如果你观察到某种冗长的具体例子（比如过度解释），可以在提示词中添加额外指令来防止它们。展示 Claude 如何以恰当简洁程度沟通的正面示例，通常比负面示例或告诉模型不要做什么的指令更有效。

## 校准 effort 与思考深度

[effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort)让你在 Claude 的智能水平与 token 花费之间调校，以能力换取更快的速度和更低的成本。编码和智能体场景从 `xhigh` effort 级别开始，大多数对智能敏感的场景至少使用 `high` effort。尝试其他 effort 级别以进一步调校 token 用量与智能：

* **`max`：** 最大 effort 在某些场景能带来性能提升，但 token 用量增加后收益可能递减。该设置有时也容易过度思考。对智能要求高的任务可以测试 max effort。
* **`xhigh`：** 超高 effort 是大多数编码和智能体场景的最佳设置。
* **`high`：** 该设置平衡 token 用量与智能。对大多数对智能敏感的场景，至少使用 `high` effort。
* **`medium`：** 适合需要降低 token 用量、同时牺牲一些智能的成本敏感场景。
* **`low`：** 留给短小的限定范围任务，以及对延迟敏感、对智能不敏感的工作负载。

Claude Opus 4.8 严格遵守 effort 级别，尤其在低端。在 `low` 和 `medium` 时，模型会把工作范围限定在被要求的范围内，而不是超出请求。这对延迟和成本有利，但在以 `low` effort 运行的中等复杂任务上，存在思考不足的风险。

如果你观察到复杂问题上推理浅显，请把 effort 提高到 `high` 或 `xhigh`，而不是靠提示词绕过。如果为了延迟必须保持 `low` effort，请添加有针对性的指导：

```text wrap
This task involves multistep reasoning. Think carefully through the problem before responding.
```

对这个模型而言，effort 很可能比以往任何 Opus 都更重要，升级时请积极尝试。

在 Claude Opus 4.8 上，除非你显式设置 `thinking: {type: "adaptive"}`，思考（thinking）是关闭的。[自适应思考（adaptive thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking)的触发行为是可以引导的。如果你发现模型思考得比期望更频繁（大而复杂的系统提示词可能导致这种情况），请添加引导性说明。一如既往，请测量任何提示词改动对性能的影响。示例：

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly.
```

反过来，如果你在 `medium` 下运行高难度工作负载并看到思考不足，第一个杠杆是提高 effort。如果需要更精细的控制，请直接在提示词中说明。

<Note>
  如果你以 `max` 或 `xhigh` effort 运行 Claude Opus 4.8，请设置较大的最大输出 token 预算，让模型在其子智能体（subagent）和工具调用之上有思考与行动的空间。从 64k token 起步，再行调优。
</Note>

## 工具使用触发

Claude Opus 4.8 倾向于优先推理而非工具调用。这在大多数情况下会产生更好的结果。不过，提高 effort 设置是增加工具使用（tool use）程度的有用杠杆，在知识型工作中尤其如此。`high` 或 `xhigh` effort 设置在智能体搜索和编码中表现出显著更多的工具使用。在希望更多使用工具的场景中，你还可以调整提示词，明确指示模型何时以及如何正确使用其工具。例如，如果你发现模型没有使用你的网页搜索工具，请清楚地描述它为什么以及应该如何使用。

## 面向用户的进度更新

Claude Opus 4.8 会在漫长的智能体轨迹中向用户提供更规律、更高质量的更新。如果你曾添加脚手架来强制中途状态消息（“每 3 次工具调用后总结进度”），可以试着删除它。如果你发现 Claude Opus 4.8 面向用户的更新在长度或内容上与你的场景不够匹配，请在提示词中明确描述这些更新应有的样子并提供示例。

## 更字面的指令遵循

Claude Opus 4.8 会字面、明确地解读提示词，在较低 effort 级别时尤其如此。它不会默默把一条指令从一个条目推广到另一个，也不会推断你没有提出的请求。这种字面主义的优点是精确、少反复，对于提示词经过精心调校的 API 场景、结构化提取和需要可预测行为的流水线，它通常表现更好。如果你需要 Claude 广泛应用某条指令，请显式说明范围（例如，“将此格式应用于每个章节，而不只是第一个”）。

## 语气与写作风格

与任何新模型一样，长篇写作的文风可能发生变化。Claude Opus 4.8 倾向于直接、有主见的风格，前置安抚性措辞极少，表情符号使用克制。如果你的产品依赖特定的语调，请对照新基线重新评估风格提示词。

例如，如果你的产品语调更温暖或更口语化，可以添加：

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

## 控制子智能体生成

Claude Opus 4.8 默认倾向生成更少的子智能体。不过，这一行为可以通过提示词引导；请给 Claude Opus 4.8 提供关于何时适合使用子智能体的明确指导。以下是编码场景的一个简单示例：

```text wrap
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

## 设计与前端默认风格

Claude Opus 4.8 有很强的设计直觉，并有一致的默认招牌风格：温暖的奶油色/米白色背景（\~`#F4F1EA`）、衬线展示字体（Georgia、Fraunces、Playfair）、斜体强调词，以及陶土色/琥珀色点缀色。这种风格适合编辑、酒店和作品集类需求，但不适合仪表盘、开发者工具、金融科技、医疗或企业应用。网页 UI 和幻灯片中都会出现这种默认风格。

这种默认风格很顽固。笼统的指令（“不要用奶油色”、“做得干净极简一点”）往往只是让模型换成另一套固定配色，而不是产生多样性。以下两种做法可靠有效：

**1. 指定具体的替代方案。** 模型会精确遵循明确的规格：

```text wrap
Design a desktop landing page for a supplement brand called AEFRM.

The visual direction should come from a cold monochrome atmosphere using pale silver-gray tones that gradually deepen into blue-gray and near-black, similar to a misted metallic surface.

The page should feel sharp and controlled, with a strong sense of structure and restraint.

Use this tonal system across the full page instead of introducing bright accent colors.

Use the uploaded image on the hero design in black and white.

The layout should be built with clear horizontal sections and a centered max-width container. Use 4px corner radius consistently across cards, buttons, inputs, and media frames. Margins should feel generous, with enough empty space around each section so the page breathes.

Typography should use a square, angular sans-serif with wider letter spacing than usual, especially in headings and navigation, so the text feels more engineered and less compressed. Headline text can be large and uppercase, while supporting copy remains short and sparse. The sub texts should be written with Alumni Sans SC in 4-6px like tiny little texts on corners bottom centre like that.

For the structure, start with a hero section containing a strong product statement, one short supporting paragraph, and a clean product placeholder or packshot frame. Below that, add a benefit grid with three or four blocks, then a formulation or ingredients section, and finally a cta.

Buttons should be flat and precise, with subtle hover changes using transition: all 160ms ease out where brightness and border contrast shift slightly rather than using dramatic motion.

Color palette should stay within this range:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

**2. 让模型先提出方案再动手。** 这能打破默认风格并把选择权交给用户。如果你以前靠 `temperature` 获得设计多样性，请改用这种做法；它在多次运行之间能产生明显不同的方向。示例提示词：

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

此外，为避免用户所称“AI 垃圾风”（AI slop）美学的通用套路，Claude Opus 4.8 所需的前端设计提示比之前的模型更少。对于更早的模型，Anthropic 曾推荐在 [frontend-design 技能](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)中使用一段更长的提示词片段。而 Claude Opus 4.8 只需更精简的提示指导就能生成有辨识度、有创意的前端。下面的提示词片段与前面关于多样性的提示建议配合良好：

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## 交互式编码产品

Claude Opus 4.8 的 token 用量和行为在两类编码智能体之间可能不同：只有单轮用户输入的自主异步编码智能体，以及拥有多轮用户输入的交互式同步编码智能体。具体来说，它在交互式环境中往往使用更多 token，主要因为它在用户回合后推理更多。这能改善长交互编码会话中的长时程连贯性、指令遵循和编码能力，但也伴随更多 token 用量。要在编码产品中同时最大化性能和 token 效率，请使用 `xhigh` 或 `high` effort，添加自动模式等自主特性，并减少要求用户进行的交互次数。

当然，在减少必要的用户交互时，重要的是在第一轮用户输入中预先说明任务、意图和相关约束。预先提供规格清晰、明确、准确的任务描述，有助于在最大化自主性和智能的同时，把用户回合之后的额外 token 用量降到最低。由于 Claude Opus 4.8 比之前的模型更自主，这种使用模式有助于最大化性能。相反，在多轮用户输入中渐进传达的模糊或欠明确的提示词，往往会相对降低 token 效率，有时还会降低性能。

## 代码审查运行框架

Claude Opus 4.8 找 bug 的能力明显强于此前的模型，在内部评测（eval）中的召回率和精确率都更高。但是，如果你的代码审查运行框架（harness）是针对更早模型调校的，起初可能看到召回率下降。这很可能是运行框架效应，而不是能力退化。当审查提示词写有“只报告高严重性问题”、“保持保守”或“不要吹毛求疵”之类内容时，Claude Opus 4.8 可能比更早的模型更忠实地遵循该指令：它可能同样彻底地调查代码、识别出 bug，然后不报告它判定低于你所设门槛的发现。表现出来的就是模型做了同样深度的调查，却把更少的调查转化为报告的发现，低严重性 bug 尤其如此。精确率通常会上升，但即使模型底层的找 bug 能力已经提高，测得的召回率仍可能下降。

一些推荐的提示词措辞：

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

即使没有真正的第二步，这段提示词也可以使用；但把置信度过滤移出发现步骤通常更有帮助。如果你的运行框架有独立的校验、去重或排序阶段，请明确告诉模型它在发现阶段的职责是覆盖而非过滤。

如果你确实希望模型在单轮中自行过滤，请具体说明报告阈值，而不是使用“重要”这类定性词汇：例如，“报告任何可能导致错误行为、测试失败或误导性结果的 bug；仅可省略纯风格或命名偏好这类小问题”。

请在你的评测或测试用例子集上迭代提示词，以验证召回率或 F1 分数的提升。

## 计算机使用

Claude Opus 4.8 支持早前的 `computer_20251124` 工具版本，并在 Claude API 和 Google Cloud 上的 Claude 模型（Google 托管）上支持 `computer_toolset_20260801` 工具集。在这两个平台上，Claude Opus 4.8 还支持用于网页内任务的[浏览器使用工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)（`browser_toolset_20260801`）。[计算机使用（computer use）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)能力可跨分辨率工作，最高支持 2576px / 3.75MP 的分辨率。内部计算机使用测试表明，以 1080p 发送图像能在性能与成本之间取得良好平衡。

对于特别成本敏感的工作负载，720p 或 1366×768 是性能强劲的低成本选项。请自行测试以找到适合你场景的理想设置；试验 effort 设置也有助于调校模型行为。
