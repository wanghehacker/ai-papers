---
title: 为 Claude Sonnet 5.5 编写提示词
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
description: "Claude Sonnet 5.5 特有的提示词模式：effort、主动性与范围、关闭前置思考运行、JSON 输出、进度更新、工具使用、轮中消息、编码验证、工具调用、视觉输入以及拒绝。"
---

本指南介绍 Claude Sonnet 5.5 特有的提示词模式。关于该模型的 API 变更，请参阅 [Claude Sonnet 5.5 的新变化](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)。关于适用于当前所有 Claude 模型的通用技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

既有的 Claude Sonnet 5 提示词应当无需修改即可良好运行，[为 Claude Sonnet 5 编写提示词](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)中的模式仍然是合理的起点。对于最难的长时程（long-horizon）工作，Opus 模型是更好的选择。请从与你所观察到的情况相符的小节开始：

* 不确定该运行哪个 effort 级别，或者轮次比在 Claude Sonnet 5 上更长或更短：[校准 effort](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#calibrate-effort)
* 模型在编码任务完成前就停下来确认，或者做了超出你要求的事：[引导主动性与范围](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#steer-initiative-and-scope)
* 你的集成目前是在关闭思考的情况下运行的：[关闭前置思考运行](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking)
* 对于需要几步推演的任务，JSON 答案出错或无法解析：[JSON 输出的推理任务](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#reasoning-tasks-with-json-output)
* 长的智能体轮次看起来毫无动静：[面向用户的进度更新](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates)
* 明明搜索本可发现已经变化的细节，模型却用训练知识作答：[聊天与知识工作中的工具使用](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tool-use-in-chat-and-knowledge-work)
* 用户在任务中途发送的消息被忽略或被当作注入文本：[轮中用户消息](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#mid-turn-user-messages-and-task-budgets)
* 代码改动没有运行测试或构建就被报告为已完成：[编码任务的验证](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#verification-on-coding-tasks)
* 模型以错误的大小写调用工具，或以略有不同的名称传递参数：[容错的工具调用处理](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tolerant-tool-call-handling)
* 关于密集图表或技术图纸的回答遗漏细节：[复杂视觉输入的工具](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tools-for-complex-visual-inputs)
* 请求返回 `stop_reason: "refusal"`：[安全防护拒绝](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#safeguard-refusals)

<Note>
  关于从 Claude Sonnet 5 迁移时的五项破坏性 API 变更，请参阅[迁移指南](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide#migrating-from-claude-sonnet-5)。
</Note>

## 校准 effort

[effort](https://platform.claude.com/docs/en/build-with-claude/effort) 是控制 Claude Sonnet 5.5 思考多少的主要手段，随之变化的是质量、延迟与成本。它的各级别经过了重新校准：同一级别产生的思考量与 Claude Sonnet 5 上的同名级别并不相同。请针对你自己的评测（eval）重新做一轮完整测试，而不是沿用你在 Claude Sonnet 5 上使用的设置。除非你的工作负载是智能体（agent）式的或对延迟敏感，否则从 `high`（Claude API 上的默认值）开始。对于智能体式编码和多步工具使用（tool use），定义明确的任务从 `medium` 开始，更难或更长的任务再转到 `high`。对于聊天和其他延迟敏感的工作，从 `medium` 或 `low` 开始，因为更高的 effort 意味着回复开始前要等更久。如果质量有需要，再调高 effort。

较低的 effort 也会改变模型完成智能体工作的方式。在 `low` 下，它会缩短思考，并且可能跳过对改动的验证。参见[编码任务的验证](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#verification-on-coding-tasks)。在 `low` 和 `medium` 下，对于长的智能体任务，它更可能在完成工作之前停下来与用户确认。参见[引导主动性与范围](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#steer-initiative-and-scope)。

以下三项调整会有帮助：

* 为思考和你预期的回复在 `max_tokens` 中留出空间。即使思考内容不会返回给你，思考也计入 `max_tokens`。按无思考请求的规模设定的上限可能把回复截断。对于智能体式编码，把 `max_tokens` 设为 128,000（该模型的最大值），并对响应使用[流式传输](https://platform.claude.com/docs/en/build-with-claude/streaming)。
* 把 `xhigh` 和 `max` 留给你已测量到质量提升的工作，因为在这两个级别下思考和回复会长得多。在这两个级别下不接受 `between_tools`，因此无法关闭前置思考。
* 想要更少的思考，就调低 effort 级别。从 `medium` 往上，模型几乎在每条回复前都会简短思考，连问候也不例外，这会增加首个可见 token 之前的等待时间。在系统提示词中要求它少思考，并不能可靠地减少它的思考。在 `low` 下，大多数简单请求它会跳过思考。

在请求之间更改顶层 `effort` 值会使提示词缓存（prompt cache）失效。要在对话中途更改级别，请改用[按消息更改 effort](https://platform.claude.com/docs/en/build-with-claude/effort#change-effort-mid-conversation-beta)（beta），它可以保留缓存。一次更改会对其后的每一轮生效，直到被另一次更改取代。例如，在运行于 `low` 的交互式会话中，在用户的难题之前加一条改到 `high` 的更改，在 Claude 答完之后再改回 `low`。按消息更改 effort 需要自适应思考（adaptive thinking）。在 `between_tools` 下，它们会返回 400 错误，[关闭前置思考运行](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking)一节对此有解释。

## 引导主动性与范围

Claude Sonnet 5.5 自主推进的程度取决于 effort 级别和请求本身。在较低的 effort 下，它有时会在编码任务完成前就停下来确认。在较高的 effort 下，或者面对开放式请求时，它可能做出超出你要求的事。请通过 effort 级别和系统提示词中的指令来引导它。

**把工作贯彻到底。** 在 `low` 和 `medium` effort 的智能体式编码任务上，模型有时会在工作完成前停下来确认。它可能暂停以确认计划、提出一个它自己就能回答的问题，或者在多部分任务完成其中一部分后停下来询问是否继续。先尝试更高的 effort 级别。若要在不改变 effort 的情况下让模型持续工作，可在系统提示词中加入以下内容：

```text wrap
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```

加上这段提示词后，模型在 `low` 和 `medium` effort 下会把更多工作贯彻到底，因此这两个级别下的会话运行更久、成本更高。这段提示词不能替代你自己关于风险性或不可逆操作的规则。请把这些规则保留在系统提示词中。

**编码时未经要求的增补。** 模型倾向于添加符合你仓库惯例的测试、文档和小的辅助文件，即使你并没有要求。它在每个 effort 级别都会这样做，在较高的 effort 下更多。被请求的改动本身仍然紧扣要求。大多数团队会欢迎这一点。如果你希望改动严格限于明确请求的范围，可以只加入那段提示词的第二段，即以 "When the work the user asked for is done" 开头的那一段。在 `xhigh` 和 `max` effort 下，这一段能减少这类增补，使改动整体更小。

**`xhigh` 与 `max` effort 下的彻底程度。** 在这些级别下，模型格外彻底。完成任务后，它可能自行发起一轮轮审查和验证，如果你的执行框架（harness）提供子智能体（subagent），有时还会用到它们。它还可能顺手修复过程中注意到的问题。这会消耗更多时间和 token，因此常规工作请在 `high` 或更低级别运行，那时这种情况很少见。如果你确实想要这些 effort 级别带来的额外彻底性，又希望把它引导到任务本身，可在系统提示词中加入以下内容：

```text wrap
When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
```

在 `max` effort 编码任务上的测试中，这段话阻止了模型启动审查子智能体，并让会话成本降低约三分之一，质量没有变化。它降低了主智能体自行发起审查轮次的频率，但不能完全消除。

**开放式请求。** 当请求是开放式的，比如"给我看看你能用它做出什么"，模型可能在你只想要点子的时候就开始制作演示文稿、报告或视频。如果你想先看到想法或方案，请在请求中说明，或在系统提示词中加入以下内容：

```text wrap
When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead.
```

## 关闭前置思考运行

要在不进行前置思考的情况下运行 Claude Sonnet 5.5，请发送 `thinking: {"type": "between_tools"}`。这是该模型上最低的思考设置，在 `high` effort 及以下被接受。如果你的集成目前是关闭思考运行的，请切换到 `between_tools` 并检查以下几点：

* **在 `high` effort 或以下发送 `between_tools`。** 在 `xhigh` 或 `max` effort 下，带 `between_tools` 的请求会返回 400 错误。使用 `between_tools` 时，effort 也无法在对话中途更改：与当前生效级别不同的按消息 `output_config.effort` 会返回 400 错误。要让每一轮的 effort 各不相同，请使用自适应思考。使用 `between_tools` 时，请移除任何告诉模型不要思考的指令。这类指令会增加模型在可见输出中写出内部 XML 标签的可能性。
* **按块类型读取响应。** 在自适应思考下，响应可能以一个 `thinking` 块开头，在默认的 `display: "omitted"` 下，该块的 `thinking` 字段为空。在 `between_tools` 下，响应可能以一个进度更新的 `thinking` 块开头。不要假设第一个内容块是文本。
* **原样传回 `thinking` 块。** 在 `between_tools` 下，模型在工具调用之间写下的笔记若长于一两句，仍会以 `thinking` 块的形式返回。每个块携带该笔记的摘要。请把它们与该轮助手消息的其余部分一起原样传回。你传回的块会让模型看到它写下的完整笔记，而不是摘要。
* **对无工具的推理任务使用自适应思考。** 在不带工具的请求中，`between_tools` 意味着模型不先思考就直接作答。对于需要几步推演的任务，请改用自适应思考。参见 [JSON 输出的推理任务](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#reasoning-tasks-with-json-output)。

## JSON 输出的推理任务

本节适用于你要求 Claude Sonnet 5.5 对一个需要几步推演的任务给出 JSON 答案的情况。例子包括汇总文档中的数字、套用某条规则，或对条目排序。在这类任务上，模型常常不先思考就直接作答，在 `low` 和 `medium` effort 下尤其如此。有效的做法取决于你如何请求 JSON。在可用的地方请使用[结构化输出](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（structured outputs）。此时响应文本就是符合你 schema 的 JSON，无需任何解析。

使用结构化输出时，响应文本只包含 JSON，因此模型只能在思考中推演问题。当它跳过思考时，在这类任务上就可能不够准确。以下更改有助于保持高准确率。

**要求模型先思考。** 在自适应思考下，把这一行加到系统提示词末尾：

```text wrap
Think the problem through before you answer.
```

加上这一行后，模型更常在作答前先思考。在 `high` effort 下，这一行能将准确率提升到接近模型在 `xhigh` 下的水平，而输出 token 只有小幅增加。在 `low` 和 `medium` effort 下，它能提高准确率，但达不到模型在 `high` 下的水平，且输出 token 的增幅更大。

**或者使用 `xhigh` effort。** 在自适应思考下，即使没有那一行，`xhigh` 在这类任务上也能给出最高准确率。它比 `high` 消耗更多输出 token。

**使用自适应思考而不是 `between_tools`。** 在不带工具的请求中，模型在 `between_tools` 下不会先思考再作答。那一行在此不起作用，这类任务上的准确率也更低。请对这些请求使用自适应思考，并按本节的步骤操作。在测试中，把请求拆成两个——一个请求答案、一个请求 JSON——能带来很高的答案准确率和 JSON 合规性，但成本和延迟都非常高。

在 `low` 和 `medium` effort 下使用结构化输出时，模型偶尔会一直思考到触及 `max_tokens`。在 `high` effort 及以上，这几乎不会发生。任何 `stop_reason` 为 `"max_tokens"` 的响应都应视为失败并重试，即使其文本中包含有效的 JSON。按[校准 effort](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#calibrate-effort)一节所述，把 `max_tokens` 设得足够容纳思考和 JSON，但不要超过你愿意为一次尝试付出的上限。

如果你无法使用结构化输出，就改为在提示词中要求 JSON。此时模型常常会在响应文本中推演问题，并在最后写出 JSON。JSON 中通常包含正确答案，但期望整个响应都是 JSON 的解析器会失败。以下两点有帮助：

* **解析响应中最后一个 JSON 值。** 只读取 `text` 块，并把 `stop_reason` 为 `"max_tokens"` 的响应视为失败。从每个 `{` 或 `[` 处开始，尝试解析出一个 JSON 值。当某个值解析成功后，从该值的末尾继续，这样嵌套在其中的值不会被单独计数。保留最后找到的值。不要截取从第一个 `{` 到最后一个 `}` 的全部内容。模型偶尔会在最终 JSON 之前写一份草稿，那样的范围会把两者都包括进来。如果你的答案是连续多个 JSON 值（例如每行一条记录），请保留最后一段仅由空格、逗号或换行分隔的连续值。检查结果是否包含你期望的字段，若没有则重试一次。在测试中，这样做让几乎所有响应都可用，且不改变其准确率。
* **也可以考虑在自适应思考下使用 `xhigh` effort。** 这样模型会在思考中推演问题，并且几乎总是只返回 JSON。总输出 token 与 `high` 大致相当，因为推演过程从响应文本移到了思考中。

## 面向用户的进度更新

在工具调用之间，Claude Sonnet 5.5 会写下面向用户的笔记，说明它刚刚发现了什么、接下来要做什么。长于一两句的笔记会以[进度更新 `thinking` 块](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates)的形式返回。更短的评论则保持为 `text`。在默认的 `thinking.display` 下，进度更新块的文本为空，因此只渲染 `text` 块的客户端在长的智能体轮次中可能显得毫无动静。这在聊天界面以及其他用户实时跟随模型工作的产品中影响最大。

要显示这些笔记，请设置 `display: "updates"`（beta，`thinking-display-updates-2026-08-18` 请求头）。在 `between_tools` 下，笔记会连同其摘要文本一起返回，因此不需要 `display` 字段。`between_tools` 不接受其他任何字段：随它一起发送 `display`、`budget_tokens` 或 `block_binding` 都会返回 400 错误。迁移指南中关于[工具调用之间的文本](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide#text-between-tool-calls)的小节展示了如何渲染这些笔记。有时模型需要在长轮次中途向用户展示精确的文本，例如一段代码片段或一个需要用户回答的问题。对于这种情况，给它一个向用户发送消息的简单工具，并告诉模型只对这类内容使用该工具。请在会话的第一个请求中声明该工具，这样 `tools` 列表之后就不会变化。

接下来，移除诸如"把所有发现留到最终响应"之类的旧指令。如果你想随后在可预期的节点获得更新——例如在第一次工具调用前说一句模型将要做什么，以及在结尾作简短回顾——请在系统提示词中说明。模型会遵循这类指令。在固定节点更新，对人在回路（human-in-the-loop）的工作帮助最大。

如果长的工具调用轮次仍然静默得超出你的预期，你的执行框架可以主动促发一次更新。让它统计连续多少个工具调用步骤没有向用户发送任何文本或进度更新。连续若干个（例如五个）之后，在最新的工具结果之后追加一条只生效一轮的提醒。以[轮级系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)（beta）的形式发送，文本如下：

```text wrap
The user hasn't heard from you in a while — say in a few words what you're doing, then continue.
```

如果轮次依然静默，在第二或第三次之后就别再发送提醒了。执行框架频繁在工具结果之后附加文本，可能导致模型把这些文本当作可能的提示词注入（prompt injection），[轮中用户消息](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#mid-turn-user-messages-and-task-budgets)一节对此有解释。在后续请求中，请把每条提醒留在 `messages` 里。由于提醒是追加的，而不是插入后再删除，提示词缓存和[保留思考](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking)（preserved thinking）保持完好。在 `high` effort 下，若提供了向用户发送消息的工具，这条提醒会让模型更频繁地更新用户，并缩短其最长的静默时段，任务质量没有可测量的变化。

## 聊天与知识工作中的工具使用

在聊天和知识工作任务上，当一次网络搜索本可发现已经变化的细节时，Claude Sonnet 5.5 有时会直接用训练知识作答。例如什么是被允许的、被要求的或需要收费的。

首先，检查你的提示词中是否有打消工具使用积极性的措辞，例如"只在绝对必要时才使用工具"或"尽量减少工具调用"，并将其移除。然后，如果你的产品为模型提供了搜索工具，可在系统提示词中加入以下内容：

```text wrap
Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.
```

这对研究与客服类产品影响最大，因为它们的答案依赖当下的细节。

## 轮中用户消息

Claude Sonnet 5.5 经过训练，会抵御间接提示词注入——即通过工具结果和它在任务期间读取的其他内容传入的恶意指令。有时它会把真正的用户消息也当作可能的注入。假设用户在任务中途输入的消息以[对话中途系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)的形式、紧跟在某个工具结果之后到达模型，或者被放在某个 `tool_result` 块内。模型随后可能告诉用户，工具结果中包含伪装成用户消息的文本，进而忽略该消息，或要求用户确认。

你的执行框架在每个工具结果之后添加 token 倒计时，也可能导致这种情况。允许用户在模型执行多步轮次的中途发送消息，或者执行框架在每一步的工具结果之后添加指令或上下文，同样可能如此。在每种情况下，文本都紧跟在工具结果之后到达。若有倒计时或每步指令，这种情况可能出现在每一次工具调用上。偶发的单轮提醒（例如[面向用户的进度更新](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates)中的那种）出现的频率则低得多。如果你发现自己的提醒也引发了这种反应，请降低发送提醒的频率。要避免这种误读：

* 绝不要把用户文本放进 `tool_result` 块内。模型最常误读的就是这种放置方式。
* 把轮中的用户输入作为一条用户轮次传递。把用户的话作为一个 text 块追加到承载 `tool_result` 块的那条用户消息中，放在最后一个 `tool_result` 之后。
* 把执行框架的通知（例如提醒）放在用户的话之后单独的对话中途系统消息中。绝不要把通知和用户的话放在同一个块里。
* 在用户可以在轮次中途输入的交互式会话中，不要在工具结果之后添加你自己的 token 或预算倒计时。[任务预算](https://platform.claude.com/docs/en/build-with-claude/task-budgets)（beta）会添加类似的倒计时，但尚未观察到它引发这种误读。如果在设置了任务预算的情况下出现误读，可以尝试不设置任务预算的会话。

## 编码任务的验证

在智能体式编码任务上，Claude Sonnet 5.5 通常会在把改动报告为完成之前先检查自己的工作。但在 `low` effort 下，它有时没有运行能够实际检验该改动的检查，就把改动报告为已完成。例如，它可能因为项目的依赖没有安装而跳过项目测试。

如果你看到转录记录中没有测试或构建输出、改动却被报告为已完成，请把下面这段（或类似的段落）加入系统提示词。在 `low` effort 下，它能让跳过检查或敷衍检查的情况变得罕见，任务质量没有可测量的变化，每个任务的成本只是略有上升：

```text wrap
When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count; if all that is missing is the project's declared dependencies, install them with its own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the system package manager, unless told not to. Only if no real check can run here, say which one you did not run and why instead of reporting the change as done.
```

## 容错的工具调用处理

Claude Sonnet 5.5 偶尔会以仅大小写不同的名称调用已声明的工具，例如用 `bash` 调用 `Bash`。它还可能以略有不同的名称传递已知参数。不要把这类调用当作致命错误，可让你的执行框架按以下两种方式之一处理：

* 当匹配没有歧义时接受该调用，即使大小写不对。
* 返回一个带 `is_error: true` 的 `tool_result`，其中说明确切的预期名称。模型通常会在下一轮纠正该调用。参见[用 `is_error` 处理错误](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls#handling-errors-with-is-error)。

## 复杂视觉输入的工具

对于密集的图表和技术图纸，请给 Claude Sonnet 5.5 一种对图像进行裁剪、缩放或运行代码的方式。有了这类工具，模型读取这些输入的准确度会显著提高。在图表上，这些工具在每个 effort 级别都有帮助。在技术图纸上，只有从 `high` effort 往上才有帮助，在 `xhigh` 和 `max` 下帮助最大。对于图表，添加工具比调高 effort 更有用：在测试中，`high` effort 下使用工具的模型读图表，比 `max` effort 下不使用工具更准确，而成本只是后者的一小部分。[裁剪工具配方](https://platform.claude.com/cookbook/multimodal-crop-tool)提供了一个可用的工具定义。

## 安全防护拒绝

Claude Sonnet 5.5 运行可能拒绝请求的安全分类器。拒绝以普通响应的形式到达，`stop_reason` 为 `"refusal"`，并由 `stop_details.category` 指明[拒绝类别](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response)：

* `cyber`：请求可能造成网络危害，例如恶意软件或漏洞利用的开发。在源代码中查找漏洞是允许的。高风险的两用网络安全工作则不被允许。
* `bio`：请求可能造成生物危害，例如危险的实验方法。日常健康和教育类问题不受影响。
* `frontier_llm`：请求可能有助于开发竞争性 AI 模型。
* `reasoning_extraction`：请求要求模型在响应文本中复现其内部推理。
* `general_harms`：请求属于另一项使用政策领域。良性工作也可能触发这一类别。

如果 `cyber` 分类器拦截了你组织的合法安全工作，你可以申请[网络安全验证计划](https://support.claude.com/en/articles/14604842)。如果 `bio` 分类器拦截了你组织的生命科学工作，你可以申请[生命科学验证计划](https://www.anthropic.com/news/life-sciences-verification-program)。

如果你开启[服务端回退](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback)（beta），它会把 `cyber` 和 `frontier_llm` 的拒绝放到 Claude Sonnet 5 上重试。它不会重试 `bio`、`reasoning_extraction` 或 `general_harms` 的拒绝。参见[拒绝、回退与计费](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5#refusals-fallback-and-billing)。

如果你的提示词要求模型把推理包含在响应中，请移除这些指令，因为它们会招致 `reasoning_extraction` 拒绝。在自适应思考下，请改为从[摘要思考](https://platform.claude.com/docs/en/build-with-claude/thinking#summarized-thinking)块（`display: "summarized"`）中读取推理。你仍然可以要求对答案作简短解释或对已执行操作作总结；参见[将推理保留在 thinking 块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)。
