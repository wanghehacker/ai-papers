---
title: Claude Fable 5.1 提示词指南
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
description: Claude Fable 5.1 与 Claude Mythos 5.1 的行为差异与提示模式，涵盖 effort、进度更新、工具调用批量化、对话历史、写作风格、格式、任务完成度、压缩摘要、范围与测试覆盖、搜索触发、安全护栏误报、文件编辑、长输出、子智能体与视觉。
---

关于该模型的能力、API 变更、定价与可用性，请参阅 [Claude Fable 5.1 的新特性](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)。关于适用于各款 Claude 模型的通用技巧，请参阅[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)。

你现有的 Claude Fable 5 prompt 在 Claude Fable 5.1 上无需改动也应该表现良好，但有少数行为差异值得了解。请从与你观察到的现象对应的章节开始：

* 不确定该运行哪个 effort 级别，或者延迟和成本超出任务所需：[考虑所有 effort 级别](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels)
* 工具调用之间几乎没有文本：[请求面向用户的进度更新](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates)
* 智能体（agent）循环中每一轮只发起一次工具调用：[在智能体循环中批量发起相互独立的工具调用](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops)
* 请求以 `bound to a different conversation` 失败，或者你的框架在请求之间编辑了较早的轮次：[保持对话历史只追加](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)
* 行文冗长而密集：[写作密度](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density)
* 聊天回复的结构化程度低于内容所需：[聊天中的格式](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#formatting-in-chat)
* 摘要复现来源原文措辞却未标注为引用：[引用检索到的来源](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#quoting-retrieved-sources)
* 工作还没做完轮次就结束，或者模型就你已请求过的工作再次征求许可：[完成整个任务](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#finish-the-whole-task)
* 客户端压缩（compaction）摘要丢失约束、决策或精确细节：[告诉模型在压缩摘要中保留什么](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#tell-the-model-what-to-preserve-in-compaction-summaries)
* 出现未经请求的修复或扩展，或者提交的测试文件多于任务所需：[将改动和测试限定在任务要求的范围内](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-changes-and-tests-to-what-the-task-asks-for)
* 低 effort 下凭记忆作答而不搜索：[低 effort 下的搜索触发](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort)
* 良性的编码请求返回 `stop_reason: "refusal"`：[减少安全护栏误报](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#reduce-safeguard-false-positives)
* 小改动却重写整个文件：[优先使用针对性编辑而非整文件重写](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#prefer-targeted-edits-over-whole-file-rewrites)
* 在 `xhigh` 或 `max` effort 下生成长交付物耗时很久或触及 `max_tokens`：[在 xhigh 和 max effort 下为长输出留出余量](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#leave-room-for-long-outputs-at-xhigh-and-max-effort)
* 子智能体（subagent）运行期间主智能体闲置：[让主智能体在子智能体运行期间继续工作](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#let-the-lead-agent-keep-working-while-subagents-run)
* 关于图表和密集图像的回答遗漏细节：[为视觉任务提供裁剪与缩放工具](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#give-vision-work-tools-to-crop-and-zoom)

<Note>
  Claude Fable 5.1 会运行安全分类器，可能返回 `stop_reason: "refusal"`。请参阅[拒绝、回退与计费](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing)和[减少安全护栏误报](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#reduce-safeguard-false-positives)。

  要求模型写出自己的 thinking 或推理的 prompt、技能和工具描述，可能会被以 `reasoning_extraction` 类别拒绝。请改为要求一段简短的解释或对已执行操作的总结，或者从[摘要式思考](https://platform.claude.com/docs/en/build-with-claude/thinking#summarized-thinking)（summarized thinking）块（`display: "summarized"`）里读取推理内容。参见[将推理保留在 thinking 块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)。
</Note>

## 考虑所有 effort 级别

从默认 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 级别 `high` 开始，然后在你自己的评测（eval）上测试其他级别（`low`、`medium`、`xhigh` 和 `max`）。effort 是在 Claude Fable 5.1 上权衡智能水平、延迟与成本的首要控制手段。即使你在 Claude Fable 5 上已经跑过一轮，也要重新做一遍扫描：不同模型之间，同名 effort 级别对应的思考量并不相同。

Claude Fable 5.1 相对 Claude Fable 5 的能力提升体现在各个 effort 级别上，且在更高档位上幅度最大。在 `medium` 下，结果大致与 Claude Fable 5 相当而成本更低，因此在你的评测表明质量可以保持的地方，可以降到 `medium` 或 `low`。在 `low` 下，Claude Fable 5.1 的单任务成本常与 Claude Opus 和 Claude Sonnet 模型相当且得分更高，因此在你原本会让较小的模型以更高 effort 级别运行的场合，都应把它纳入比较。

两个与特定 effort 相关的行为各有单独的章节：在 `low` 下，Claude Fable 5.1 调用搜索和检索工具的频率更低（见[低 effort 下的搜索触发](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#search-triggering-at-low-effort)）；在 `xhigh` 和 `max` 下，它可能在动笔写长交付物之前思考更久（见[在 xhigh 和 max effort 下为长输出留出余量](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#leave-room-for-long-outputs-at-xhigh-and-max-effort)）。

## 请求面向用户的进度更新

在长时间的工具调用轮次中，Claude Fable 5.1 的默认行为是写出的面向用户的更新比 Claude Fable 5 更少。这一点在更高 effort 和更长的工具链中更加明显。用户会看到智能体一次安静好几分钟，或者收到的最终消息只涵盖最后一步而非整个任务。

首先，确认你的客户端到底能不能收到进度更新。模型在工具调用之间写的简短说明——它刚刚发现了什么、接下来要做什么——会以[进度更新 `thinking` 块](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates)的形式返回，而在默认 `thinking.display` 为 `"omitted"` 时，这些块是空的。设置 `display: "updates"`（beta，需 `thinking-display-updates-2026-08-18` 请求头），把每个非空的 `thinking` 块渲染成一条状态行；或者设置为 `"summarized"`，在接收摘要式推理的同时一并收到它们。如果你没有请求它们，模型的更新可能根本就没有传到你的用户那里。

其次，检查你的 prompt 里有没有抑制解说的指令。一些早期模型在工作时会频繁给出更新，这让系统提示词里出现了诸如“hold all findings for the final response”（把所有发现都留到最终回复）这样的语句。先删掉这类语句，再去添加任何新东西。

如果你仍希望有更多更新，例如在结对编程或其他人在回路的工作中，可以在系统提示词里加一句简短的话，说明你希望模型在什么时机输出面向用户的文本、每次更新应包含什么内容：

```text wrap
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

如果你的产品会折叠或隐藏工具输出，要告诉模型。否则它可能会运行命令来向用户“展示”你的 UI 从未显示过的输出。每当你发回会被你的 UI 隐藏的工具输出时，都用一条[轮次级系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)（`clear_at: "next_user_message"`，beta）附上这段提示：

```text wrap
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

## 在智能体循环中批量发起相互独立的工具调用

Claude Fable 5.1 通常会按预期并行发起工具调用：当请求里点名了多项要获取的内容时，它会并行发出这些调用。例外是编码和计算机使用循环——其中下一批相互独立的调用由任务隐含、而非被显式请求（自定义编码智能体、bash 加编辑器的框架、计算机使用）：在这些场景下，它可能改成每轮只发起一个。这不影响答案质量，但每多一个轮次就要消耗 token、一次往返和实际等待时间。在当前请求末尾加一句提醒就能解决：

```text wrap
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

每次把工具结果发回去时，都把这句话作为[轮次级系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)追加到那条用户消息之后：也就是在 `messages` 里加入一条带 `clear_at: "next_user_message"` 的 `role: "system"` 条目。一旦之后出现了新的用户消息，API 就会清除较早的副本，模型因此只会读到最新的那一条。轮次级系统消息目前处于 beta 阶段，需要 [beta 请求头](https://platform.claude.com/docs/en/api/beta-headers) `mid-conversation-system-clear-at-2026-08-21`。若不用这个 beta，可以把这句话放在同一条用户消息中、`tool_result` 块之后的文本块里。

每轮追加一个新的副本，让先前的副本逐字节原样留在原处。它们仍留在数组里，但一旦被清除，模型就看不到它们，它们也不再消耗输入 token。删除或改写它们就是对较早轮次的编辑：这会使位于其后的 thinking 块失效（见[保持对话历史只追加](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)）。

下面的循环展示了这种放置方式。每个助手轮次都完全按 API 返回的原样回传，每个用户轮次只携带工具结果，其后跟着一份新的轮次级提醒副本。

<CodeGroup exclude="shell">
  ```python Python
  import anthropic
  from anthropic.types.beta import (
      BetaMessageParam,
      BetaToolParam,
      BetaToolResultBlockParam,
  )

  client = anthropic.Anthropic()

  BATCH_NUDGE = (
      "First privately list what you need next; then request every item "
      "that doesn't depend on another's result in this one response."
  )
  # In-memory files stand in for a working directory so the sample runs anywhere.
  FILES = {
      "pyproject.toml": """\
  [project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  """,
      "README.md": """\
  # demo

  A small demo project. Run `demo --help` for usage.
  """,
  }
  tools: list[BetaToolParam] = [
      {
          "name": "read_file",
          "description": "Read a UTF-8 text file from the working directory.",
          "input_schema": {
              "type": "object",
              "properties": {"path": {"type": "string"}},
              "required": ["path"],
          },
      }
  ]
  messages: list[BetaMessageParam] = [
      {"role": "user", "content": "Summarize pyproject.toml and README.md."}
  ]

  while True:
      response = client.beta.messages.create(
          model="claude-fable-5-1",
          max_tokens=16000,
          betas=["mid-conversation-system-clear-at-2026-08-21"],
          tools=tools,
          messages=messages,
      )
      # Append the assistant turn exactly as returned, thinking blocks included.
      messages.append({"role": "assistant", "content": response.content})
      if response.stop_reason != "tool_use":
          break
      tool_results: list[BetaToolResultBlockParam] = []
      for block in response.content:
          if block.type == "tool_use":
              raw_path = block.input.get("path")
              path = raw_path if isinstance(raw_path, str) else ""
              if path in FILES:
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": FILES[path],
                      }
                  )
              else:
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": f"File not found: {path}",
                          "is_error": True,
                      }
                  )
      # Send the tool results as the user turn, then a fresh copy of the nudge as a
      # turn-scoped system message. Leave earlier copies in place: the API clears them,
      # so the model sees only the newest one.
      messages.append({"role": "user", "content": tool_results})
      messages.append(
          {"role": "system", "content": BATCH_NUDGE, "clear_at": "next_user_message"}
      )

  print(next((block.text for block in response.content if block.type == "text"), ""))
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const BATCH_NUDGE =
    "First privately list what you need next; then request every item " +
    "that doesn't depend on another's result in this one response.";
  // In-memory files stand in for a working directory so the sample runs anywhere.
  const FILES = new Map<string, string>([
    [
      "pyproject.toml",
      `[project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  `
    ],
    [
      "README.md",
      `# demo

  A small demo project. Run \`demo --help\` for usage.
  `
    ]
  ]);
  const tools: Anthropic.Beta.Messages.BetaTool[] = [
    {
      name: "read_file",
      description: "Read a UTF-8 text file from the working directory.",
      input_schema: {
        type: "object",
        properties: { path: { type: "string" } },
        required: ["path"]
      }
    }
  ];
  const messages: Anthropic.Beta.Messages.BetaMessageParam[] = [
    { role: "user", content: "Summarize pyproject.toml and README.md." }
  ];

  let response: Anthropic.Beta.Messages.BetaMessage;
  while (true) {
    response = await client.beta.messages.create({
      model: "claude-fable-5-1",
      max_tokens: 16000,
      betas: ["mid-conversation-system-clear-at-2026-08-21"],
      tools,
      messages
    });
    // Append the assistant turn exactly as returned, thinking blocks included.
    messages.push({ role: "assistant", content: response.content });
    if (response.stop_reason !== "tool_use") {
      break;
    }
    const toolResults: Anthropic.Beta.Messages.BetaToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type !== "tool_use") {
        continue;
      }
      const { input } = block;
      const path =
        typeof input === "object" &&
        input !== null &&
        "path" in input &&
        typeof input.path === "string"
          ? input.path
          : "";
      const text = FILES.get(path);
      if (text === undefined) {
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: `File not found: ${path}`,
          is_error: true
        });
        continue;
      }
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        content: text
      });
    }
    // Send the tool results as the user turn, then a fresh copy of the nudge as a
    // turn-scoped system message. Leave earlier copies in place: the API clears them,
    // so the model sees only the newest one.
    messages.push({ role: "user", content: toolResults });
    messages.push({
      role: "system",
      content: BATCH_NUDGE,
      clear_at: "next_user_message"
    });
  }

  const finalText = response.content.find((block) => block.type === "text");
  console.log(finalText?.text ?? "");
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  const string BatchNudge =
      "First privately list what you need next; then request every item "
      + "that doesn't depend on another's result in this one response.";

  // In-memory files stand in for a working directory so the sample runs anywhere.
  Dictionary<string, string> files = new()
  {
      ["pyproject.toml"] = """
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          """,
      ["README.md"] = """
          # demo

          A small demo project. Run `demo --help` for usage.
          """,
  };

  List<BetaToolUnion> tools =
  [
      new BetaTool
      {
          Name = "read_file",
          Description = "Read a UTF-8 text file from the working directory.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["path"] = JsonSerializer.SerializeToElement(new { type = "string" }),
              },
              Required = ["path"],
          },
      },
  ];

  List<BetaMessageParam> messages =
  [
      new BetaUserMessageParam { Content = "Summarize pyproject.toml and README.md." },
  ];

  BetaMessage response;
  while (true)
  {
      response = await client.Beta.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeFable5_1,
          MaxTokens = 16000,
          Betas = ["mid-conversation-system-clear-at-2026-08-21"],
          Tools = tools,
          Messages = messages,
      });
      // Append the assistant turn exactly as returned, thinking blocks included.
      messages.Add(new BetaAssistantMessageParam
      {
          Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
      });
      if (response.StopReason != BetaStopReason.ToolUse)
      {
          break;
      }
      List<BetaContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              var path = toolUse.Input.TryGetValue("path", out var pathValue)
                  && pathValue.ValueKind == JsonValueKind.String
                  ? pathValue.GetString()!
                  : "";
              if (files.TryGetValue(path, out var fileText))
              {
                  toolResults.Add(new BetaToolResultBlockParam { ToolUseID = toolUse.ID, Content = fileText });
              }
              else
              {
                  toolResults.Add(new BetaToolResultBlockParam
                  {
                      ToolUseID = toolUse.ID,
                      Content = $"File not found: {path}",
                      IsError = true,
                  });
              }
          }
      }
      // Send the tool results as the user turn, then a fresh copy of the nudge as a
      // turn-scoped system message. Leave earlier copies in place: the API clears them,
      // so the model sees only the newest one.
      messages.Add(new BetaUserMessageParam { Content = toolResults });
      messages.Add(new BetaSystemMessageParam
      {
          Content = BatchNudge,
          ClearAt = ClearAt.NextUserMessage,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
          break;
      }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  )

  const batchNudge = "First privately list what you need next; then request every item " +
  	"that doesn't depend on another's result in this one response."

  // In-memory files stand in for a working directory so the sample runs anywhere.
  var files = map[string]string{
  	"pyproject.toml": `[project]
  name = "demo"
  version = "0.1.0"
  description = "Demo project for the batching example"
  `,
  	"README.md": `# demo

  A small demo project. Run "demo --help" for usage.
  `,
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.BetaToolUnionParam{
  		{OfTool: &anthropic.BetaToolParam{
  			Name:        "read_file",
  			Description: anthropic.String("Read a UTF-8 text file from the working directory."),
  			InputSchema: anthropic.BetaToolInputSchemaParam{
  				Properties: map[string]any{
  					"path": map[string]any{"type": "string"},
  				},
  				Required: []string{"path"},
  			},
  		}},
  	}
  	messages := []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize pyproject.toml and README.md.")),
  	}

  	var response *anthropic.BetaMessage
  	for {
  		var err error
  		response, err = client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeFable5_1,
  			MaxTokens: 16000,
  			Betas:     []anthropic.AnthropicBeta{"mid-conversation-system-clear-at-2026-08-21"},
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		// Append the assistant turn exactly as returned, thinking blocks included.
  		messages = append(messages, response.ToParam())
  		if response.StopReason != anthropic.BetaStopReasonToolUse {
  			break
  		}
  		var toolResults []anthropic.BetaContentBlockParamUnion
  		for _, block := range response.Content {
  			toolUse, ok := block.AsAny().(anthropic.BetaToolUseBlock)
  			if !ok {
  				continue
  			}
  			var input struct {
  				Path string `json:"path"`
  			}
  			// A missing or non-string path leaves input.Path empty, which takes the error-result branch.
  			if err := json.Unmarshal([]byte(toolUse.JSON.Input.Raw()), &input); err != nil {
  				input.Path = ""
  			}
  			text, found := files[input.Path]
  			if !found {
  				text = "File not found: " + input.Path
  			}
  			toolResults = append(toolResults, anthropic.NewBetaToolResultBlock(toolUse.ID, text, !found))
  		}
  		// Send the tool results as the user turn, then a fresh copy of the nudge as a
  		// turn-scoped system message. Leave earlier copies in place: the API clears them,
  		// so the model sees only the newest one.
  		messages = append(messages, anthropic.NewBetaUserMessage(toolResults...))
  		messages = append(messages, anthropic.BetaMessageParam{OfSystem: &anthropic.BetaSystemMessageParam{
  			Content: []anthropic.BetaSystemMessageParamContentUnion{{OfText: &anthropic.BetaTextBlockParam{Text: batchNudge}}},
  			ClearAt: anthropic.BetaSystemMessageParamClearAtNextUserMessage,
  		}})
  	}

  	for _, block := range response.Content {
  		if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  			fmt.Println(textBlock.Text)
  			break
  		}
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.BetaContentBlockParam;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.BetaSystemMessageParam;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.BetaTool.InputSchema;
  import com.anthropic.models.beta.messages.BetaToolResultBlockParam;
  import com.anthropic.models.beta.messages.BetaToolUseBlock;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  static final String BATCH_NUDGE =
      "First privately list what you need next; then request every item "
          + "that doesn't depend on another's result in this one response.";

  // In-memory files stand in for a working directory so the sample runs anywhere.
  static final Map<String, String> FILES = Map.of(
      "pyproject.toml", """
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          """,
      "README.md", """
          # demo

          A small demo project. Run `demo --help` for usage.
          """);

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaTool readFileTool = BetaTool.builder()
          .name("read_file")
          .description("Read a UTF-8 text file from the working directory.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of("path", Map.of("type", "string"))))
              .required(List.of("path"))
              .build())
          .build();
      List<BetaMessageParam> messages = new ArrayList<>();
      messages.add(BetaMessageParam.ofUser("Summarize pyproject.toml and README.md."));

      BetaMessage response;
      while (true) {
          response = client.beta().messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_FABLE_5_1)
              .maxTokens(16000)
              .addBeta("mid-conversation-system-clear-at-2026-08-21")
              .addTool(readFileTool)
              .messages(messages)
              .build());
          // Append the assistant turn exactly as returned, thinking blocks included.
          messages.add(response.toParam());
          boolean requestedTools = response.stopReason()
              .map(BetaStopReason.TOOL_USE::equals)
              .orElse(false);
          if (!requestedTools) {
              break;
          }
          List<BetaToolUseBlock> toolUses = response.content().stream()
              .flatMap(block -> block.toolUse().stream())
              .toList();
          List<BetaContentBlockParam> toolResults = new ArrayList<>();
          for (BetaToolUseBlock toolUse : toolUses) {
              Map<String, JsonValue> input =
                  (Map<String, JsonValue>) toolUse._input().asObject().orElseThrow();
              JsonValue pathValue = input.get("path");
              String path = pathValue != null && pathValue.asString().isPresent()
                  ? pathValue.asStringOrThrow()
                  : "";
              String fileText = FILES.get(path);
              BetaToolResultBlockParam.Builder result = BetaToolResultBlockParam.builder()
                  .toolUseId(toolUse.id());
              if (fileText != null) {
                  result.content(fileText);
              } else {
                  result.content("File not found: " + path).isError(true);
              }
              toolResults.add(BetaContentBlockParam.ofToolResult(result.build()));
          }
          // Send the tool results as the user turn, then a fresh copy of the nudge as a
          // turn-scoped system message. Leave earlier copies in place: the API clears them,
          // so the model sees only the newest one.
          messages.add(BetaMessageParam.ofUserOfContentBlockParams(toolResults));
          messages.add(BetaMessageParam.ofSystem(BetaSystemMessageParam.builder()
              .content(BATCH_NUDGE)
              .clearAt(BetaSystemMessageParam.ClearAt.NEXT_USER_MESSAGE)
              .build()));
      }

      String finalText = response.content().stream()
          .flatMap(block -> block.text().stream())
          .map(textBlock -> textBlock.text())
          .findFirst()
          .orElse("");
      IO.println(finalText);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Messages\BetaStopReason;
  use Anthropic\Client;

  $client = new Client();

  const BATCH_NUDGE = 'First privately list what you need next; then request every item '
      . "that doesn't depend on another's result in this one response.";
  // In-memory files stand in for a working directory so the sample runs anywhere.
  const FILES = [
      'pyproject.toml' => <<<'TOML'
          [project]
          name = "demo"
          version = "0.1.0"
          description = "Demo project for the batching example"
          TOML,
      'README.md' => <<<'MD'
          # demo

          A small demo project. Run `demo --help` for usage.
          MD,
  ];
  $tools = [
      [
          'name' => 'read_file',
          'description' => 'Read a UTF-8 text file from the working directory.',
          'input_schema' => [
              'type' => 'object',
              'properties' => ['path' => ['type' => 'string']],
              'required' => ['path'],
          ],
      ],
  ];
  $messages = [
      ['role' => 'user', 'content' => 'Summarize pyproject.toml and README.md.'],
  ];

  while (true) {
      $response = $client->beta->messages->create(
          model: 'claude-fable-5-1',
          maxTokens: 16000,
          betas: ['mid-conversation-system-clear-at-2026-08-21'],
          tools: $tools,
          messages: $messages,
      );
      // Append the assistant turn exactly as returned, thinking blocks included.
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      if ($response->stopReason !== BetaStopReason::TOOL_USE->value) {
          break;
      }
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $path = is_string($block->input['path'] ?? null) ? $block->input['path'] : '';
              if (array_key_exists($path, FILES)) {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => FILES[$path],
                  ];
              } else {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => "File not found: {$path}",
                      'is_error' => true,
                  ];
              }
          }
      }
      // Send the tool results as the user turn, then a fresh copy of the nudge as a
      // turn-scoped system message. Leave earlier copies in place: the API clears them,
      // so the model sees only the newest one.
      $messages[] = ['role' => 'user', 'content' => $toolResults];
      $messages[] = [
          'role' => 'system',
          'content' => BATCH_NUDGE,
          'clear_at' => 'next_user_message',
      ];
  }

  $textBlock = array_find($response->content, fn ($block) => $block->type === 'text');
  echo $textBlock?->text ?? '', PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  BATCH_NUDGE =
    "First privately list what you need next; then request every item " \
    "that doesn't depend on another's result in this one response."
  # In-memory files stand in for a working directory so the sample runs anywhere.
  FILES = {
    "pyproject.toml" => <<~TOML,
      [project]
      name = "demo"
      version = "0.1.0"
      description = "Demo project for the batching example"
    TOML
    "README.md" => <<~MD
      # demo

      A small demo project. Run `demo --help` for usage.
    MD
  }
  tools = [
    {
      name: "read_file",
      description: "Read a UTF-8 text file from the working directory.",
      input_schema: {
        type: "object",
        properties: {path: {type: "string"}},
        required: ["path"]
      }
    }
  ]
  messages = [{role: "user", content: "Summarize pyproject.toml and README.md."}]

  response = nil
  loop do
    response = client.beta.messages.create(
      model: Anthropic::Model::CLAUDE_FABLE_5_1,
      max_tokens: 16000,
      betas: ["mid-conversation-system-clear-at-2026-08-21"],
      tools: tools,
      messages: messages
    )
    # Append the assistant turn exactly as returned, thinking blocks included.
    messages << {role: "assistant", content: response.content}
    break unless response.stop_reason == :tool_use

    tool_results = response.content.filter_map do |block|
      next unless block.type == :tool_use

      path = block.input[:path]
      if FILES.key?(path)
        {type: "tool_result", tool_use_id: block.id, content: FILES[path]}
      else
        {
          type: "tool_result",
          tool_use_id: block.id,
          content: "File not found: #{path}",
          is_error: true
        }
      end
    end
    # Send the tool results as the user turn, then a fresh copy of the nudge as a
    # turn-scoped system message. Leave earlier copies in place: the API clears them,
    # so the model sees only the newest one.
    messages << {role: "user", content: tool_results}
    messages << {role: "system", content: BATCH_NUDGE, clear_at: "next_user_message"}
  end

  puts response.content.find { it.type == :text }&.text
  ```
</CodeGroup>

## 保持对话历史只追加

把每个助手轮次完全按 API 返回的原样追加到历史里，包括 thinking 块，并且不要在请求之间编辑较早的轮次。一个 thinking 块[只有在其之前的所有内容都保持不变时才有效](https://platform.claude.com/docs/en/build-with-claude/thinking#preserved-in-conversation)：系统提示词、工具列表，以及之前的每一条消息。要决定未通过前缀检查的块如何处理，可设置 `thinking.block_binding.prefix_mismatch_behavior`，它需要 `thinking-binding-controls-2026-08-01` beta 请求头。设为 `"error"` 时，API 以 400 错误拒绝该请求；设为 `"drop_block"` 时，API 丢弃无效的块。至于不设置该参数的请求会怎样，见[未设置 `prefix_mismatch_behavior` 时](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#enforcement)。

大多数会触发前缀检查的历史编辑也会重启[提示词缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（prompt cache）：比如逐轮注入又移除提醒、就地摘要较早的轮次，或在会话中途更改系统提示词。逐轮提醒请改用[轮次级系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)发送；更改指令或工具请使用[会话中途系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)，而不是改写 `system` 或 `tools`；一切裁剪都交给服务端[压缩](https://platform.claude.com/docs/en/build-with-claude/compaction)或[上下文编辑](https://platform.claude.com/docs/en/build-with-claude/context-editing)去做。如果你在客户端压缩，最简单的形态是用一条摘要消息加上新的用户轮次替换整个历史，其他内容一概不重放。没有 thinking 块被带过去，所以不会有任何块失效，模型会在压缩后的对话上重新思考（见[在客户端压缩](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#custom-compaction-on-the-client)）。Claude Fable 5.1 的缓存读取价格为每百万 token 0.25 美元，即输入价格的 2.5%（见[定价](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#pricing)）。为了省钱而过早压缩，在成本与智能水平之间可能是一笔错误的买卖，因此请试验更晚的压缩时机。

要找出你的框架做了哪些编辑，可以按[检查你的代码是否编辑了前缀](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted)里的做法，以 `prefix_mismatch_behavior: "drop_block"` 跑一个会话并记录 `input_transformations`。你也可以捕获它在几个正常轮次里发出的确切请求，确认相邻请求在新增轮次之前的部分逐字节一致。

## 写作密度

Claude Fable 5.1 的写作里套话很少，几乎也没有不加解释的行话。但在某些情况下，它的行文比 Claude Fable 5 更密集：句子更长，分段更少。定义这种反模式——“矫饰文风”（mannered prose）——的指令会有帮助。把它加到用户消息里（首选）或系统提示词里：

```text wrap
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

简短版本通常也有效：

```text wrap
Please remove all mannered prose.
```

## 聊天中的格式

早期模型在聊天中过度使用列表和加粗，很多 prompt 里因此带着为减少这类问题而写的反格式化规则。Claude Fable 5.1 的倾向恰恰相反：它更少用加粗，也更少去用标题、列表或引号。如果你的 prompt 里有反格式化的语句，请删掉它，或者换成一条说明什么时候适合用特定格式的规则，比如下面这条：

```text wrap
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

## 引用检索到的来源

在总结文档时，Claude Fable 5.1 比 Claude Fable 5 更容易复现来源文本的段落而不把它们标注为引用。要解决这个问题，可以在系统提示词里加入一个完整的正确回复示例：用户的请求、回复，以及一句解释这个回复为什么正确的说明。

```text wrap
<example>
<user>look up how the Riverton Ledger and the Coast Dispatch each covered the Harbor Bridge closure and compare their reporting</user>
<response>
[web_search: Harbor Bridge closure Riverton Ledger]
[web_search: Harbor Bridge closure Coast Dispatch]
Both outlets agree on the basics: the bridge closed on March 3 after inspectors found cracked welds, and the state expects repairs to take about eight months. Where they differ is emphasis. The Ledger treats it as a local-economy story. The Dispatch frames it as a funding failure; its editorial calls the closure "entirely foreseeable." Read together, the Ledger explains who is affected now and the Dispatch explains how it came to this — neither account alone gives the whole picture.
</response>
<rationale>CORRECT: The response is organized around where the two outlets agree and differ, not as a walk through either article. Each outlet's reporting is conveyed in one or two sentences of the assistant's own indirect speech. One short marked phrase from one source; every other claim is reworded. The response is still specific and complete.</rationale>
</example>
```

请把那两行 `[web_search: ...]` 替换成你自己工具的名称，这样模型会把它们读作模板化的工具输出，而不是要逐字照搬的文字。

## 完成整个任务

Claude Fable 5.1 在方法论指导不多的情况下也能执行很长的任务，尤其是在目标明确的时候。但在复杂的异步工作负载上，要提醒它不要在工作完成之前结束轮次。没有这句提醒，模型有时会描述自己接下来要做什么，而不是直接去做（“Next, I'll …”），或者停下来为原始请求已经覆盖的步骤征求许可（“Shall I apply this?”）。用户只能回复“继续”或“开始吧”，这适合结对编程和其他人在回路的工作，却没有发挥模型完整的长时程（long-horizon）能力。

在系统提示词里加两段内容可以共同缓解这个问题。请两段都用。如果你需要控制 prompt 长度，就只用第一段，它保留了大部分效果。第一段告诉模型不要就已请求过的工作发问，并把它已经说出的后续步骤直接执行掉：

```text wrap
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

开头那句告诉模型用户没有在实时观看的话，承载了大部分效果，请按原样保留。如果你的产品需要模型为特定的确认事项停下来，可以在那句话后面加一句，把它们列出来。这一段也可能让模型更不愿意就含糊的请求发问，请在你自己的任务上核对这笔权衡。

第二段把用户的请求定义为交付物的范围：

```text wrap
# Delivering work
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

## 告诉模型在压缩摘要中保留什么

当一段长对话被压缩时，明确告诉 Claude Fable 5.1 它的摘要必须保留哪些内容，效果很好。服务端[压缩](https://platform.claude.com/docs/en/build-with-claude/compaction)已经这么做了。如果你在客户端压缩，请使用下面这条摘要指令：

```text wrap
Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped.
```

## 将改动和测试限定在任务要求的范围内

当被要求实现一个开放式的功能时，Claude Fable 5.1 会交付所要求的东西，有时还给得更多：它可能修复附近的代码、扩展任务没有提到的行为，或者提交多于这次改动所需要的测试文件。它对“哪些不要做”的明确指令反应良好。加上下面这条指令后，未经请求的追加内容和提交的测试代码会大幅减少，而任务成功率没有可测量的变化：

```text wrap
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

## 低 effort 下的搜索触发

在 `low` effort 下，Claude Fable 5.1 不像 Claude Fable 5 那样常调用搜索或检索工具，而更倾向于凭记忆回答。某些情况下，最简单的修复是只对受影响的轮次提高 effort，而不是提高整个对话的。参见[在会话中途更改 effort](https://platform.claude.com/docs/en/build-with-claude/effort#changing-effort-mid-conversation)。

另一些情况下，在 prompt 里朝验证方向推一把会有帮助。在系统提示词里说明：认出一个名字不等于知道它当前的状态，这类名字应该按用户的原样写法去搜索：

```text wrap
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

## 减少安全护栏误报

Claude Fable 5.1 的安全分类器产生的误报（false positive）比 Claude Fable 5 发布时更少，而且允许在源代码中查找漏洞。误报仍会出现，被拦截的请求会返回 `stop_reason: "refusal"`（见[拒绝、回退与计费](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1#refusals-fallback-and-billing)）。有三种情况会加大误报的可能：

* **编译检查式措辞：** 不要问“这个程序能否无错误地编译？”，而要问“这个程序里有没有 bug？”
* **小众编程语言：** 给模型提供关于这门语言是什么、如何运作的背景信息，例如让它能访问这门语言的文档。
* **工具输出里的 base64：** 向模型上下文返回 base64 编码数据的工具可能触发误报，因此建议的修复是移除这些数据。

## 优先使用针对性编辑而非整文件重写

如果 Claude Fable 5.1 为小改动重写整个文件，可以把下面的指令附加到系统提示词或第一条用户消息。Claude Fable 5.1 比 Claude Fable 5 更倾向于重写整个文本文件，而不是做一处针对性的编辑。最终文件通常是一样的，但除非文件很短或大部分内容都在变动，重写要花掉更多输出 token 和时间。加上这条指令后，Claude Fable 5.1 在中小改动上的行为就和 Claude Fable 5 一致了。

```text wrap
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

## 在 xhigh 和 max effort 下为长输出留出余量

在 `xhigh`、尤其是 `max` effort 下，Claude Fable 5.1 可能会在开始写回复之前思考更久。当单个请求要一份长交付物（比如完整重写一份长文档）时，它可能在思考里起草这份交付物的大部分，然后又作为回复再写一遍，这意味着更长的等待和更多的输出 token。最简单的做法是把这类请求放在 `high`（推荐的起点）跑，只在你测得过质量提升的地方再升到 `xhigh` 或 `max`（见[考虑所有 effort 级别](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#consider-all-effort-levels)）。如果你确实要在 `xhigh` 或 `max` 下跑它们：

* 把 `max_tokens` 设置得给思考和回复都留出空间，而不只是你预期的回复长度。
* 把下面这段提示附加到用户消息末尾。它能让文本和代码类请求的思考大幅变短。请把 `[max_tokens]` 替换成该请求实际的 `max_tokens` 值，例如 64,000。

```text wrap
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

## 让主智能体在子智能体运行期间继续工作

如果你的编码智能体允许 Claude Fable 5.1 把工作委托给子智能体，不要强迫主智能体停下来逐个等待。在编码任务上，让主智能体在子智能体运行的同时继续干活，能在质量、token 用量和成本相近的前提下降低平均完成时间。可以这样搭建：

* 让启动子智能体的工具立即返回。
* 每个子智能体的结果就绪后，在稍后的一条 `user` 消息里传回给主智能体。
* 给主智能体一个单独的工具，供它调用来等待结果。

模型仍常常会等待。省下的时间来自那些它继续干其他活的运行。

## 为视觉任务提供裁剪与缩放工具

Claude Fable 5.1 开箱即用就有更好的视觉能力，面对密集图表这类复杂视觉输入，当它能够迭代地分析、裁剪并目视核验自己看到的内容时，表现最好。要拿到全部收益，请把模型当作智能体来运行，让它能访问一个容器——里面放着原始图像或视频，并预装了基本的图像处理库（如 PIL 和 OpenCV）。如果跑一个容器开销太大，单是一个图像裁剪工具就能带来大部分提升：这种工具返回图像中选定的一块区域（已裁剪并放大），让模型能把具体细节看得更深，并以图像 token 来扩展测试时计算。[裁剪工具配方](https://platform.claude.com/cookbook/multimodal-crop-tool)里有一个可用的定义。
