---
title: 为 Claude Fable 5 编写提示词
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
description: Claude Fable 5 与 Claude Mythos 5 的行为差异与提示词模式，涵盖 effort、指令遵循、长时间运行、记忆以及脚手架变更。
---

本指南介绍 Claude Fable 5 和 Claude Mythos 5 特有的提示词与脚手架模式。关于该模型的规格、定价与可用性，请参阅 [Claude Fable 5](https://platform.claude.com/docs/en/models/fable-5/overview)。关于适用于当前所有 Claude 模型的通用技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

Claude Fable 5 能够承担对以往模型来说过于复杂、运行过久或过于模糊的问题，尤其擅长完成一个人要花数小时、数天甚至数周才能做完的端到端工作。取得最佳效果的团队会把 Claude Fable 5 用在他们最棘手的未解难题上；只用较简单的工作负载去测试它，往往会低估它的能力范围。它在较为直接的任务上同样表现可靠。

Claude Fable 5 与 Claude Opus 4.8 相比存在若干行为差异，可能需要更新提示词或脚手架。这一级别的能力提升也是一个好契机，可以借此重新评估哪些指令、工具和护栏（guardrail）仍有必要。以下模式涵盖了最常需要调优的行为。

<Note>
  关于 Claude Fable 5 和 Claude Mythos 5 上思考机制的工作方式（仅支持自适应思考（adaptive thinking）、思考输出仅提供摘要形式、没有扩展思考（extended thinking）预算），请参阅[思考](https://platform.claude.com/docs/en/build-with-claude/thinking#configuring-thinking)。关于 `refusal` 停止原因与回退处理，请参阅[拒绝与回退](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)。

  Claude Fable 5 运行安全分类器，针对攻击性网络安全技术（如构建漏洞利用、恶意软件或攻击工具）、生物学与生命科学内容（如实验方法或分子机制），以及对模型思考摘要的提取。良性的网络安全工作和有益的生命科学任务也可能触发这些安全防护。若要自动改道被拒绝的请求，请配置到 Claude Opus 4.8 的[服务端或客户端回退](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)。
</Note>

## 能力提升

与 Claude Opus 4.8 相比，Claude Fable 5 在以下方面有所提升：

* **长时程（long-horizon）自主性。** Claude Fable 5 能够在更长的时间跨度上保持高效产出，完成持续多日、以目标为导向的运行，并在漫长而复杂的任务中始终保持对指令的牢固遵循。
* **复杂且定义明确问题的一次通过正确性。** 早期测试者报告称，以往需要数天迭代的系统，现在单次实现即可完成。
* **视觉能力。** Claude Fable 5 解读密集的技术图像、Web 应用和详细截图的准确度显著提高，而且通常使用更少的输出 token；它还经过训练，会使用 bash 和裁剪工具来处理翻转、模糊或带噪点的图像。
* **企业工作流。** Claude Fable 5 遵循指令、不越出范围，并在财务分析、电子表格、幻灯片和文档方面产出专业级的成果。
* **代码审查与调试。** 查找缺陷的召回率（在安全分类器所覆盖的网络安全领域之外）明显高于 Claude Opus 4.8，包括跨代码库和仓库历史的搜索。
* **驾驭模糊性。** 当面对复杂的多线程请求并被要求确定下一步行动时，Claude Fable 5 表现良好。
* **委托与协作。** Claude Fable 5 在派发和维持并行子智能体（subagent）方面明显更可靠，并能稳定管理与长时间运行的子智能体及同级智能体（agent）之间的持续通信。

除这些具体提升之外，Claude Fable 5 在几乎所有任务上都比之前的模型更能干。Claude Fable 5 不适用于攻击性网络安全或生物学与生命科学工作；这些领域的请求可能返回 [`stop_reason: "refusal"`](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)。

## 默认更长的轮次

在较高的 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 设置下，困难任务的单个请求可能运行数分钟之久，尤其是当任务需要收集上下文、构建并自我验证时；自主运行则可能延续数小时。这是团队在适应 Claude Fable 5 时遇到的最大转变之一。迁移之前，请先调整客户端超时、流式传输和面向用户的进度指示器，并考虑重构执行框架（harness），改为异步地检查运行状态（例如通过定时任务），而不是阻塞等待。为了避免 Claude Fable 5 在任务模糊时过度规划：

```text wrap
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

## 考虑所有 effort 级别

[effort](https://platform.claude.com/docs/en/build-with-claude/effort) 是 Claude Fable 5 上智能、延迟与成本之间权衡的主要控制手段。大多数任务默认使用 `high`，对能力最敏感的工作负载使用 `xhigh`，常规工作则使用 `medium` 或 `low`。Claude Fable 5 在较低的 effort 设置下依然表现出色，常常超过以往模型在 `xhigh` 下的性能。如果任务虽然完成了但耗时超出必要程度，或者你希望采用更快、更交互式的协作风格，就降低 effort。

在较高的 effort 下处理常规工作时，Claude Fable 5 收集上下文和反复斟酌的程度可能超出任务需要。与此同时，较高的 effort 往往能带来出色的验证行为、精巧的推理和最严谨的输出。为了防止在较高 effort 下出现未经要求的整理或重构：

```text wrap
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

## 更强的指令遵循

指令遵循能力的提升已经足够大，你可以用一条简短的指令来引导大多数行为，而不必逐一点名列举每种行为。例如，在未加引导时，Claude Fable 5 可能会铺陈超出任务需要的内容，尤其是在较高的 effort 设置下：罗列它并不会采纳的选项、长篇大论地解释根因、生成结构过重的 PR 描述，或者写下解说下一行代码在做什么的注释。一条简短的简洁性指令，与逐一列举各种模式同样有效：

```text wrap
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

同样的道理也适用于长时间运行工作流中的检查点行为。要让 Claude Fable 5 只在真正需要你的地方停下，不必枚举每一种情况：

```text wrap
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

## 在长时间运行中为进度断言提供依据

在长时间的自主运行中，应指示 Claude Fable 5 依据实际的工具结果来审计进度。在 Anthropic 的测试中，这样做几乎消除了编造状态报告的情况，即使任务是专门为诱导出这种行为而设计的：

```text wrap
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

## 明确边界

Claude Fable 5 偶尔会做出未被请求的操作（没人要求却起草一封邮件、创建防御性的 git 分支备份）。请为 Claude Fable 5 应做和不应做的事情定义明确的约束：

```text wrap
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

## 并行子智能体

Claude Fable 5 比以往的模型更乐于派发并行子智能体。请频繁使用子智能体，就何时适合委托给出明确指导，并优先让编排者与子智能体之间异步通信，而不是阻塞等待每个子智能体返回。跨子任务保留上下文的长寿命子智能体可以通过缓存读取节省时间和成本，并避免被最慢的子智能体拖成瓶颈。

```text wrap
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

## 构建记忆系统

当 Claude Fable 5 能够记录以往运行的经验教训并加以引用时，它的表现尤其出色。为它提供一个写笔记的地方，简单到一个 Markdown 文件即可：

```text wrap
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

若要从既有历史出发引导建立记忆系统，可让 Claude Fable 5 回顾过去的会话：

```text wrap
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

## 少数提前停止的情况

在长会话进行到深处时，Claude Fable 5 偶尔会以纯文本的意图声明（"I'll now run X"）结束一轮，却不发出相应的工具调用，或者在已有足够条件继续时停下来请求许可。此时一句"继续"或"放手把它端到端做完"就够了。要定义何时适合暂停，可将其与[更强的指令遵循](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#strong-instruction-following)中的检查点指令配合使用。对于自主运行的流水线，可添加一条系统提醒：

```text wrap
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

## 少数上下文预算相关的情况

在非常长的会话中，Claude Fable 5 偶尔会建议开启新会话、主动提出总结并交接，或者削减自己的工作。这种情况最常由执行框架向模型展示剩余 token 倒计时触发。请尽量避免向模型呈现显式的上下文预算计数。如果执行框架必须展示，一句安抚性的说明会有帮助：

```text wrap
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

## 给出理由，而不只是请求

当 prompt 中说明了请求背后的意图时，Claude Fable 5 往往表现更好：上下文能让它把任务与相关信息关联起来，而不必自行推断意图。请说明你为什么提出这个请求，尤其是对于需要动用多个工作流的长时运行智能体：

```text wrap
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

## 与用户沟通时的可读性

在长时间或智能体式的对话中（大量工具调用、庞大的工作上下文），Claude Fable 5 可能产出难以跟随的文字：密集的箭头链速记、过深的实现细节、引用用户从未见过的思考内容，或者过于技术化的措辞。附加一段沟通风格说明可以缓解这个问题：

```text wrap
Terse shorthand is fine between tool calls. Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

## 创建 send-to-user 工具

在运行长时间、异步的智能体时，要给智能体一种方式，让它在不结束当前轮次的情况下呈现用户必须原样看到的消息：一份交付物（生成的代码片段或起草的消息）、一条带具体数字的进度更新，或者对用户在循环中途所提问题的直接回复。该工具的输入就是要显示的消息；当 Claude 调用它时，直接在你的 UI 中渲染该输入，并返回一个简单的确认作为工具结果。工具输入永远不会被摘要，因此内容能够原封不动地送达。

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

只要你的 UX 依赖在任务中途原样传递内容或进行直接的用户交互，就添加这个工具。对于只叙述常规进度的智能体，模型自己的摘要通常就足够了。仅定义工具本身并不够；如果系统提示词中没有相应的指令，Claude Fable 5 很少会调用它。请将工具与如下引导性措辞配合使用：

```text wrap
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

不要把叙述或内部推理经由 `send_to_user` 传递；对非面向用户的内容过度调用它，就违背了这个工具的初衷。

## 推荐的脚手架变更

* **从你难度区间的顶端开始。** 选一个比你会分配给以往模型更难的任务，让 Claude Fable 5 去划定范围、提出澄清问题并完成它。
* **在长时间运行的提示词中明确要求自我验证。** 独立的、使用全新上下文的验证者子智能体往往优于自我批评。对于长时间运行的任务，可以这样指示：`Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.`
* **重构既有的提示词与技能。** 为以往模型开发的技能对 Claude Fable 5 而言往往过于死板，可能降低输出质量。如果默认表现更好，请检查并考虑移除旧指令。Claude Fable 5 也很擅长在工作过程中根据从当前任务中学到的东西来更新技能。
* **不要指示 Claude 在响应中复现其推理。** 那些要求模型以响应文本的形式复述、誊写或解释其内部推理的提示词、技能或执行框架指令，在 Claude Fable 5 上可能触发 [`reasoning_extraction` 拒绝类别](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response)。使用 `fallbacks: "default"` 的服务端回退不会重试因 `reasoning_extraction` 被拒绝的请求；该拒绝会直接返回给你。迁移时，请审计既有技能和系统提示词中是否存在反思类或"展示你的思考"类指令。如果你的应用需要让推理可见，请改为从[自适应思考](https://platform.claude.com/docs/en/build-with-claude/thinking)读取结构化的 `thinking` 块，并在长时间运行期间使用 [send-to-user 工具](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#create-a-send-to-user-tool)来呈现进度。你仍然可以要求对答案作简短解释或对已执行操作作总结；参见[将推理保留在 thinking 块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)。
* **创建 send-to-user 工具。** 对于长时间、异步的智能体，一个客户端工具可以在不结束当前轮次的情况下把消息原样传递给用户。参见[创建 send-to-user 工具](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5#create-a-send-to-user-tool)。
