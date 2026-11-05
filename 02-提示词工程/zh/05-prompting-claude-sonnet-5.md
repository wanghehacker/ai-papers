---
title: 为 Claude Sonnet 5 编写提示词
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
description: Claude Sonnet 5 的行为差异与提示词模式，涵盖 effort、自适应思考默认行为以及工具使用。
---

本指南介绍 Claude Sonnet 5 特有的提示词模式。关于该模型的规格，请参阅 [Claude Sonnet 5](https://platform.claude.com/docs/en/models/sonnet-5/overview)。关于适用于当前所有 Claude 模型的通用技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

Claude Sonnet 5 在编码和智能体（agent）任务方面具有特别的优势。它在既有的 Claude Sonnet 4.6 提示词上开箱即用、表现良好。本指南中的模式涵盖了最常需要调优的行为。

## 响应长度与详略程度

Claude Sonnet 5 会根据任务的复杂度来校准响应长度，而不是默认采用固定的详略程度。这通常意味着：简单的查询回答更短，开放式的分析回答更长。

如果你的产品依赖某种特定的输出风格或详略程度，你可能需要调整提示词。举个例子，想降低冗长度，可以添加：

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

如果你发现特定类型的冗长（比如过度解释），可以在提示词中加入额外的指令来防止它们。与负面示例或告诉模型不要做什么的指令相比，展示 Claude 如何以恰当的简洁程度沟通的正面示例往往更有效。

## 校准 effort 与思考深度

[effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort)允许你在 Claude 的智能与 token 花费之间进行调节，用一部分能力换取更快的速度和更低的成本。在 Claude Sonnet 5 上，effort 默认为 `high`，与 Claude Sonnet 4.6 相同。对于最难的编码和智能体任务，可将 effort 提升到 `xhigh`。也可以尝试其他 effort 级别，进一步调节 token 用量与智能：

* **`max`：** 绝对最大能力，对 token 花费没有任何约束。
* **`xhigh`：** 特高 effort 是最难编码和智能体用例的推荐设置。
* **`high`：** 默认值。该设置对大多数用例在 token 用量和智能之间取得平衡。
* **`medium`：** 适合成本敏感、需要在牺牲一定智能的同时减少 token 用量的用例。
* **`low`：** 留给范围明确的短小任务，以及对延迟敏感、但对智能不敏感的工作负载。

迁移时可参考一个粗略的跨模型对应关系：Claude Sonnet 5 在 medium 下的智能与 Claude Sonnet 4.6 在 high 下相当，Claude Sonnet 5 在 high 下与 Claude Sonnet 4.6 在 max 下相当。做基准测试时，请按观测到的思考长度对齐，而不是按 effort 名称对齐。

Claude Sonnet 5 会严格遵守 effort 级别，在低端尤其如此。在 `low` 和 `medium` 下，模型会把工作范围限定在被要求的事项之内，而不会超出请求。这对延迟和成本有利，但在以 `low` effort 运行中等复杂任务时，存在思考不足的风险。

如果你观察到模型在复杂问题上推理浅薄，请直接把 effort 提高到 `high` 或 `xhigh`，而不是围绕它写提示词。如果出于延迟原因必须把 effort 保持在 `low`，可添加有针对性的引导：

```text wrap
This task involves multistep reasoning. Think carefully through the problem before responding.
```

在 Claude Sonnet 5 上，[自适应思考（adaptive thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking)默认开启。不带 `thinking` 字段的请求会以自适应思考运行。这与 Claude Sonnet 4.6 不同，同样的请求在后者上是不带思考运行的。要完全关闭思考，请传递 `thinking: {type: "disabled"}`。由于 `max_tokens` 是总输出（思考加响应文本）的硬性上限，对那些在 Claude Sonnet 4.6 上不带思考运行的工作负载，请重新审视这个值。如果你之前在 Claude Sonnet 4.6 上关闭了思考，在 Claude Sonnet 5 上可以尝试开启思考并使用更低的 effort 级别。

自适应思考的触发行为是可以引导的。如果你发现模型输出 thinking 块的频率超出你的期望（在使用大型或复杂的系统提示词时可能出现这种情况），可添加引导来加以调节。与以往一样，请测量任何提示词改动对性能的影响。示例：

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

反过来，如果你在 `medium` 下运行困难的工作负载并发现思考不足，第一个抓手是提高 effort。如果需要更精细的控制，可以直接用提示词提出要求。

Claude Sonnet 5 不支持手动扩展思考（extended thinking）（`thinking: {type: "enabled", budget_tokens: N}`），会返回 400 错误。它在 Claude Sonnet 4.6 上已被弃用，现在已被移除。请改用自适应思考加 effort 参数。

<Note>
  如果你以 `high`、`xhigh` 或 `max` effort 运行 Claude Sonnet 5，请在 `max_tokens` 中留出余量，让模型有空间进行思考和工具调用。在长任务上，自适应思考可能占用预算的很大一部分；如果预算吃紧，你可能会看到这样一个响应：几乎全是思考，随后是被截断的回答和 `stop_reason: "max_tokens"`。调高 `max_tokens` 或降到 `medium` effort 可以解决这个问题。由于 Claude Sonnet 5 使用了新的分词器（tokenizer），同样的文本大约会产生多 30% 的 token，为 Claude Sonnet 4.6 调校的 `max_tokens` 上限可能会截断等价的输出。确切的增幅取决于内容和工作负载形态。
</Note>

## 工具使用的触发

默认情况下，Claude Sonnet 5 比 Claude Sonnet 4.6 更具智能体特质，更乐于使用工具并运行自我验证循环。关闭思考时，模型使用工具或考虑搜索的可能性会降低；如果你依赖在关闭思考的情况下进行工具调用，请在系统提示词中加入明确的推动。effort 也是影响工具使用的一个杠杆：`high` 或 `xhigh` effort 设置在智能体式搜索和编码中表现出明显更多的工具使用。在希望增加工具使用的场景中，你还可以调整提示词，明确指示模型何时以及如何正确使用其工具。例如，如果你发现模型没有使用你的网络搜索工具，请清楚地描述它为什么应该使用以及应该如何使用。

## 面向用户的进度更新

Claude Sonnet 5 会在长的智能体轨迹全程向用户提供定期且质量更高的更新。如果你曾添加脚手架来强制产生中间状态消息（"每 3 次工具调用后总结一下进度"），可以尝试将其移除。如果你发现 Claude Sonnet 5 面向用户的更新在长度或内容上与你的用例不够匹配，请在提示词中明确描述这些更新应该是什么样子，并提供示例。

## 更字面的指令遵循

Claude Sonnet 5 会以字面、明确的方式解读提示词，在较低的 effort 级别下尤其如此。它不会悄悄地把针对某一项的指令泛化到另一项，也不会推断你没有提出的请求。这种字面主义的优点是精确；对于使用精心调校的提示词、结构化提取以及需要可预测行为的流水线的 API 用例，它通常表现更好。如果你需要 Claude 广泛地应用某条指令，请明确说明范围（例如"把这个格式应用到每一个小节，而不只是第一个"）。

## 语气与写作风格

与任何新模型一样，长篇写作的文风可能会发生变化。如果你的产品依赖特定的语气风格，请对照新的基线重新评估风格提示词。

例如，如果你产品的语气更温暖、更口语化，可以添加：

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

如果你之前依靠 `temperature` 来获得风格多样性，请注意在 Claude Sonnet 5 上设置 `temperature`、`top_p` 或 `top_k` 会返回 400 错误。这一约束对 Sonnet 系模型来说是新的。迁移时请移除这些参数，改用系统提示词指令来引导语气和多样性。

## 设计与前端默认风格

在开放式的前端和设计需求上，Claude Sonnet 5 可能会落入一种一致的默认视觉风格。一套默认的固有风格对某些需求来说观感不错，但对仪表盘、开发者工具、金融科技、医疗或企业应用可能并不合适。

泛泛的指令（"别用那种颜色"、"做得干净极简一点"）往往只是让模型换到另一套固定的配色，而不是产生多样性。以下两种做法稳定有效：

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

**2. 让模型在构建之前先提出选项。** 这能打破默认风格，并把控制权交给用户。由于 Claude Sonnet 5 不接受 `temperature`，要在多次运行之间产生真正不同的设计方向，推荐采用这一做法。示例提示词：

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

为了避开用户称之为"AI 垃圾风"（AI slop）审美的套路化模式，你可以在系统提示词中加入一条简短的指令。[frontend-design 技能](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)提供了更完整的处理，但下面这段内容与前面几种多样性做法配合使用效果也很好：

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## 交互式编码产品

在只有单轮用户输入的自主、异步编码智能体，与拥有多轮用户输入的交互式、同步编码智能体之间，token 用量和行为可能有所不同。要在编码产品中同时把性能和 token 效率最大化，请使用 `xhigh` 或 `high` effort，添加诸如自动模式之类的自主功能，并减少需要你的用户参与的人工交互次数。

在限制所需用户交互次数的同时，重要的是在第一轮人类输入中预先说明任务、意图和相关约束。预先提供定义清晰、明确且准确的任务描述，有助于在把用户轮次之后的额外 token 用量降到最低的同时，最大化自主性和智能。相反，在多轮用户输入中逐步给出的模糊或欠明确的提示词，往往会相对降低 token 效率，有时还会降低性能。

## 代码审查执行框架

如果你的代码审查执行框架（harness）是为较早的模型调校的，在 Claude Sonnet 5 上你最初可能看到召回率下降。这很可能是执行框架层面的效应，而不是能力回退。当审查提示词写有"只报告高严重性问题"、"保守一点"或"不要吹毛求疵"之类的内容时，Claude Sonnet 5 对这类指令的遵循可能比早期模型更彻底：它可能同样深入地检查代码、找出缺陷，然后不报告它判定低于你所设门槛的发现。这可能表现为模型做了同样深度的调查，但把调查转化为报告发现的比例更低，尤其是在较低严重性的缺陷上。精确率通常会上升，但即使模型底层的找缺陷能力已经提高，测得的召回率仍可能下降。

一些推荐的提示词写法：

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

这段提示词在没有真正的第二步时也可以使用，但把置信度过滤从发现阶段移出去往往有帮助。如果你的执行框架有单独的验证、去重或排序阶段，请明确告诉模型它在发现阶段的职责是覆盖面而不是过滤。

如果你确实希望模型在单次通过中自行过滤，请具体说明报告的门槛，而不是使用"重要"之类的定性说法：例如"报告任何可能导致错误行为、测试失败或误导性结果的缺陷；只省略纯风格或命名偏好这类小问题"。

请在你的评测（eval）或测试用例的一个子集上迭代提示词，以验证召回率或 F1 分数的提升。

## 计算机使用（Computer use）

Claude Sonnet 5 支持较早的 `computer_20251124` 工具版本，并且在 Claude API 和 Google Cloud 上的 Claude 模型（Google 托管）上支持 `computer_toolset_20260801` 工具集。在这两个平台上，Claude Sonnet 5 还支持[浏览器使用工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)（`browser_toolset_20260801`），用于网页内的任务。[计算机使用（Computer use）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)能力可跨分辨率工作，最高支持 2576px / 3.75MP 的分辨率。内部的计算机使用测试表明，以 1080p 发送图像在性能和成本之间取得了良好的平衡。

对于特别关注成本的工作负载，720p 或 1366×768 是成本更低且性能强劲的选择。请自行测试，为你的用例找到理想的设置；尝试不同的 effort 设置也有助于调优模型的行为。
