---
title: Claude Opus 5 提示词指南
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
description: Claude Opus 5 的行为差异与提示词模式，涵盖回复冗长度、智能体叙述、任务范围控制、子智能体委派、自我纠正，以及禁用思考时的输出伪影。
---

本指南介绍 Claude Opus 5 特有的提示词（prompt）模式。关于该模型的规格，请参阅[Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/overview)。关于适用于当前所有 Claude 模型的技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

Claude Opus 5 为复杂的智能体（agent）编码和企业级工作而生，在长时程（long-horizon）智能体任务上尤为擅长。它在现有的 Claude Opus 4.8 提示词上开箱即用地表现良好。以下模式涵盖最常需要调优的行为。

## 能力提升

与 Claude Opus 4.8 相比，与提示词最相关的改进有：

* **智能体编码：** Claude Opus 5 最擅长高难度编码任务：多文件特性、大型重构，以及端到端的特性开发。它会完整地完成任务而不是留下桩代码或占位符，并且在预先给出完整任务规格、放手让它运行时表现最佳。它在单轮编辑等较简单任务上也表现良好，只是与先前模型的差距较小。
* **代码审查与找 bug：** Claude Opus 5 审查代码的精确率和召回率都很高：每轮扫描都能以高比率找到真实 bug，其额外发现也大多是真实问题而非误报。在较低 effort 设置下准确率依然保持，这支持评审时先快速过一遍、稍后再细致过一遍。如果你的审查提示词写了“只报告高严重性问题”或“保持保守”，模型可能会字面遵循该指令而报告得更少；请改为让它报告一切，再在单独一轮中过滤。
* **低 effort 下的效率：** `low` 和 `medium` [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 能以更高设置一小部分的 token 和延迟产出强劲的质量。从默认值（`high`）开始，再根据你的评测（eval）调整：凡质量能保持的场景，大胆把 `low` 和 `medium` 作为控制 token 成本和响应时间的主要手段；要求高的编码和智能体工作则上调到 `xhigh`。如果你沿用了先前模型的 effort 默认值，请在你自己的评测上重新做一次 effort 扫描。完整指引请参见[推荐的 effort 级别](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5)。
* **视觉：** Claude Opus 5 在图表、文档和示意图理解，以及 UI 与前端视觉还原方面都很强。请重新验证你为先前模型调过的任何 prompt 侧视觉变通方案；它们可能已不再需要。当模型拥有可迭代分析、裁剪并视觉核验其工作的工具时，视觉表现最强；工具使用（tool use）是比单纯思考更具性价比的杠杆。
* **长上下文工作：** Claude Opus 5 的[100 万 token 上下文窗口（context window）](https://platform.claude.com/docs/en/build-with-claude/context-windows)既是默认值也是最大值，其指令遵循、工具调用（tool call）和推理在整个窗口内保持一致。
* **办公与文档任务：** Claude Opus 5 能生成并处理含有复杂公式的多工作表电子表格，还能产出结构良好的幻灯片演示。请在提示词中给出它需要遵循的具体样式或模板。
* **多智能体协调：** Claude Opus 5 能很好地协调子智能体（subagent）团队，写作者-校验者模式行之有效，智能体之间互相覆盖工作的情况也很少。对于成本敏感的工作负载，请限制委派；参见[控制子智能体生成](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning)。

## 回复长度与冗长度

Claude Opus 5 默认的面向用户的回复比先前的 Opus 模型更长。[effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort)控制的是模型[思考（thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)多少，而不是说多少：降低 effort 可以减少思考量，但不能可靠地缩短可见回复。要控制回复长度，请在提示词中明确要求。

一条简短的简洁性指令就很有效。例如，对于面向用户的多轮产品：

```text wrap
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

在长系统提示词（system prompt）中，请把该指令与提示词末尾附近的简短提醒配对使用：

```text wrap
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

## 面向用户的进度更新

Claude Opus 5 在智能体工作中很乐意叙述：它倾向于宣布自己即将做什么，且智能体会话中每条消息的输出往往比先前模型更长。它会受益于关于任务期间如何与用户沟通的明确指导。想把叙述调低，就描述你想要的节奏和形态：

```text wrap
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

想把叙述调高或改变其风格，同一个杠杆朝另一个方向用力即可：明确描述更新应该是什么样子，并提供示例。展示你想要的沟通风格的正面示例，通常比告诉模型不要做什么的指令更有效。

## 书面交付物长度

与对话冗长度分开的是，Claude Opus 5 写入磁盘的文件（报告、Markdown 文档、总结）往往比在先前模型上更长。如果你的产品包含 Claude 撰写的文档，请添加明确的长度校准：

```text wrap
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

## 任务范围与过度校验

Claude Opus 5 无需吩咐就会校验自己的工作。如果你的提示词包含明确的校验指令（“为任何非平凡任务加入最终校验步骤”、“使用子智能体来校验”），请删除它们：这类指令会在 Claude Opus 5 上导致过度校验，删除它们能减少浪费的 token 且不损失质量。对添加独立校验步骤的旧运行框架（harness）脚手架，同样如此处理。

Claude Opus 5 还可能扩大任务范围，添加未被要求的步骤，或按自己的判断理解任务应该是什么。对于窄范围任务，请显式约束范围：

```text wrap
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

## 控制子智能体生成

Claude Opus 5 比先前模型更乐于委派给子智能体。对于真正独立、规模可观的工作分支，委派是值得的；但用在小事上会成倍增加成本和时间。如果你的运行框架支持子智能体，请就哪些场景值得委派给出明确指导，或者对可启动的智能体数量设置确定性上限。例如：

```text wrap
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

如果你的运行框架是 Claude Code 或 Claude Agent SDK，确定性上限就是 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 和 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 环境变量，以及 SDK 的 `max_budget_usd`（typescript: `maxBudgetUsd`）选项。旧版 Claude Code 没有这些，所以在把运行框架指向 Claude Opus 5 之前，请更新 Claude Code 和任何固定版本的 SDK。只有在 Claude Opus 5 上使用其 `claude_code` 系统提示词预设时，Claude Code 才会自动添加自己的委派指令；使用自定义或省略的系统提示词时，请自行添加本节示例那样的委派指令。参见 Agent SDK 文档中的[限制子智能体深度、并发和开销](https://code.claude.com/docs/en/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend)。

## 自我纠正

Claude Opus 5 无需提示就能很好地发现并修正自己的错误。避免指示它做已经在做的复查（“再次检查你的答案”、“回复前重新校验”）；与校验指令一样，这些会与模型自身行为叠加，只增加成本而不改善结果。

该模型也比先前模型更多地叙述对自己先前说法的纠正，这在面向用户的产品中可能并不理想。要把纠正性叙述限制在真正要紧的纠正上：

```text wrap
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

## 禁用思考运行

Claude Opus 5 默认开启[思考](https://platform.claude.com/docs/en/build-with-claude/thinking)，且只有 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 为 `high` 或更低时才能禁用思考。把 `thinking: {"type": "disabled"}` 与 `xhigh` 或 `max` effort 组合的请求会返回 400 错误。禁用思考时，模型的可见输出中偶尔会出现两种伪影（artifact）。两者的首要缓解措施都是保持思考开启、用更低的 effort 级别控制 token 成本，而不是禁用思考：对大多数任务而言，`low` effort 下开启思考的表现优于相近成本下禁用思考。

**工具调用写成文本。** 禁用思考时，模型偶尔会把工具调用写进面向用户的文本，而不是发出结构化的 `tool_use` 块。回合正常结束，该调用从未执行；而且在智能体循环中，泄漏的文本会留在对话历史里，后续回合也会受影响。这在搜索等重度使用工具的工作负载上最常见。

**输出中的内部 XML 标签。** 禁用思考时，模型可能在可见响应中发出 `<thinking>` 标签或其他内部 XML 标签。如果你的系统提示词中有一条要求模型不要思考或不要推理的规则，请删除它；这类指令会加剧标签泄漏。

对于必须保持禁用思考的集成，一条组合指令可以同时缓解两种伪影：它明确允许模型在工具调用前说话、在没有合适工具时给出替代做法（而不是强行调用），并制定禁止内部标签的一般规则：

```text wrap
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

点名 thinking 标签的指令不如一般形式有效，所以避免具体点名它们。

## 回复中的推理

要求 Claude Opus 5 逐字或按固定格式写出其思考或推理的提示词、技能和工具描述，可能会被以 `reasoning_extraction` [拒绝类别](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response)拒绝。请改为要求对答案作简短解释或总结已执行的操作；如果你确实需要推理，请保持思考开启并读取[思考摘要（summarized thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking#summarized-thinking)块（`display: "summarized"`）。参见[把推理保留在 thinking 块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)。
