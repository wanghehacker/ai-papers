---
title: 提示词最佳实践
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
description: 面向 Claude 最新模型的提示词工程技巧综合指南，涵盖清晰表达、示例、XML 结构化、思考与智能体系统。
---

这是当前 Claude 模型（包括 Claude Fable 5.1、Claude Mythos 5.1、Claude Fable 5、Claude Mythos 5、Claude Opus 5.5、Claude Opus 5、Claude Opus 4.8、Claude Opus 4.7、Claude Opus 4.6、Claude Sonnet 5.5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Haiku 5.5 和 Claude Haiku 4.5）提示词工程的参考文档。本页分为三个部分：

* **[各模型专属指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#model-specific-guidance)**在前：介绍单个模型行为有何不同，以及 prompt 中需要相应修改什么。
* 随后是**适用于所有当前模型的技巧**：通用原则、输出与格式、工具使用、思考，以及智能体（agent）系统。
* 最后是**迁移注意事项**，面向从早期几代模型迁移而来的 prompt。

<Tip>
  要概览模型能力，请参阅[模型概览](https://platform.claude.com/docs/en/models/overview)。要了解 Claude Fable 5.1 的能力与 API 变更，请参阅 [Claude Fable 5.1 的新特性](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)。要获取迁移指引，请参阅[迁移指南](https://platform.claude.com/docs/en/about-claude/models/migration-guide)。关于 Claude Opus 5.5，请参阅 [Claude Opus 5.5 的新特性](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)。关于 Claude Sonnet 5.5，请参阅 [Claude Sonnet 5.5 的新特性](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)。关于 Claude Haiku 5.5，请参阅 [Claude Haiku 5.5 的新特性](https://platform.claude.com/docs/en/models/haiku-5-5/whats-new-haiku-5-5)。
</Tip>

## 各模型专属指南

这些模型各有自己的提示词页面。请先阅读你所用模型对应的页面，再阅读后面介绍的技巧。

| 模型                                  | 指南                                                                                                                               | 差异点                                                                                                                                                                                                                                                                                                        |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5.1 与 Claude Mythos 5.1 | [Claude Fable 5.1 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)   | 与 Claude Fable 5 的差异：effort 级别、长任务收尾、面向用户的进度更新、原样传回 thinking 块、智能体循环中的工具调用批处理、低 effort 时的搜索触发、格式与写作密度。                                                                        |
| Claude Fable 5 与 Claude Mythos 5     | [Claude Fable 5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)       | 与 Claude Opus 4.8 的差异：effort 级别、指令遵循、长时间运行时的进度声明、记忆系统，以及 `reasoning_extraction` 拒绝类别。                                                                                                                                                      |
| Claude Sonnet 5.5                      | [Claude Sonnet 5.5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) | 与 Claude Sonnet 5 的差异：effort 校准、主动性与任务范围、无前置思考运行、推理任务的 JSON 输出、面向用户的进度更新、聊天中的工具使用、回合中用户消息、编码任务的验证、工具调用处理、复杂视觉输入和安全保障拒绝。 |
| Claude Sonnet 5                        | [Claude Sonnet 5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)     | 与 Claude Sonnet 4.6 的差异：回复长度、effort 与思考深度校准、工具使用触发、字面化指令遵循，以及设计与前端默认取向。                                                                                                                                       |
| Claude Opus 5.5                        | [Claude Opus 5.5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)     | 与 Claude Opus 5 的差异：effort 校准、为禁用思考而编写的 prompt、面向用户的进度更新、安全保障拒绝，以及用于复杂视觉输入的工具。                                                                                                                                       |
| Claude Opus 5                          | [Claude Opus 5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)         | 与早期 Opus 模型的差异：回复长度与冗余度、面向用户的进度更新、书面交付物长度、任务范围与过度验证、子智能体控制和自我修正。                                                                                                                   |
| Claude Opus 4.8                        | [Claude Opus 4.8 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)     | 回复长度、effort 与思考深度校准、工具使用触发、字面化指令遵循、子智能体控制，以及设计与前端默认取向。                                                                                                                                                         |
| Claude Haiku 5.5                       | [Claude Haiku 5.5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)   | 与 Claude Haiku 4.5 的差异：effort 级别、搜索、用你自己的工具输出 JSON、长智能体 prompt 中的提前停止、编码任务的验证、回合中用户消息、聊天机器人的系统提示词遵循和安全保障拒绝。                                                                     |

## 通用原则

本节及后续各节的技巧适用于当前的 Claude 模型，包括 Claude Fable 5.1、Claude Mythos 5.1、Claude Fable 5 和 Claude Mythos 5。当某项技巧点名了特定模型时，应将其视为在该模型上测得的结果；在应用到其他模型之前，请先用你自己的评测（eval）重新验证。

### 清晰、直接

Claude 对清晰、明确的指令反应良好。具体说明你想要的输出有助于提升效果。如果你希望 Claude 做的事情超出任务本身的最低要求，请明确提出，而不要指望模型从含糊的 prompt 中自行推断。

可以把 Claude 想象成一位才华横溢、但不了解你的规范和工作流程的新员工。你把需求解释得越精确，结果就越好。

**关键测试：** 把你的 prompt 拿给一位对该任务几乎不了解的同事看，请他照着执行。如果他会感到困惑，Claude 也会。

* 具体说明你想要的输出格式和约束条件。
* 当步骤的顺序或完整性很重要时，用编号列表或项目符号列表把指令组织成分步形式。

<Accordion title="示例：创建分析仪表盘" defaultOpen>
  **效果一般：**

  ```text wrap
  Create an analytics dashboard
  ```

  **效果更好：**

  ```text wrap
  Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
  ```
</Accordion>

### 补充上下文以提升表现

在指令之外提供背景或动机（例如向 Claude 解释为什么这种行为很重要），能让 Claude 更了解你的目标，从而给出更有针对性的回复。

<Accordion title="示例：格式偏好" defaultOpen>
  **效果一般：**

  ```text wrap
  NEVER use ellipses
  ```

  **效果更好：**

  ```text wrap
  Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
  ```
</Accordion>

Claude 能够据此举一反三。

### 有效使用示例

示例是引导 Claude 输出格式、语气和结构最可靠的手段之一。几个精心设计的示例（即少样本提示（few-shot prompting）或多样本提示（multishot prompting））能提升准确性和一致性。

添加示例时，应让它们做到：

* **相关：** 紧密贴合你的实际使用场景。
* **多样：** 覆盖边界情况，并保持足够的变化，以免 Claude 学到非预期的模式。
* **结构化：** 用 `<example>` 标签包裹示例（多个示例放在 `<examples>` 标签中），让 Claude 能将它们与指令区分开。

<Tip>
  为获得最佳效果，建议提供 3–5 个示例。你还可以让 Claude 评估你的示例是否相关、多样，或让它基于你的初始示例生成更多示例。
</Tip>

### 用 XML 标签组织 prompt

XML 标签能帮助 Claude 无歧义地解析复杂 prompt，尤其是当你的 prompt 混合了指令、上下文、示例和变量输入时。把每类内容分别放进各自的标签（例如 `<instructions>`、`<context>`、`<input>`），可以减少误解。

最佳实践：

* 在所有 prompt 中使用一致且有描述性的标签名。
* 当内容存在天然的层级结构时嵌套标签（`<documents>` 内放多个文档，每个放在 `<document index="n">` 中）。

### 给 Claude 分配角色

在系统提示词中设定角色，可以让 Claude 的行为和语气聚焦到你的使用场景上。哪怕只有一句话也会有用：

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "system": "You are a helpful coding assistant specializing in Python.",
      "messages": [
        {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --system "You are a helpful coding assistant specializing in Python." \
    --message '{role: user, content: "How do I sort a list of dictionaries by key?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      system="You are a helpful coding assistant specializing in Python.",
      messages=[
          {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
      ],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    system: "You are a helpful coding assistant specializing in Python.",
    messages: [{ role: "user", content: "How do I sort a list of dictionaries by key?" }]
  });

  console.log(message.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      System = "You are a helpful coding assistant specializing in Python.",
      Messages = [new UserMessageParam { Content = "How do I sort a list of dictionaries by key?" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a helpful coding assistant specializing in Python."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I sort a list of dictionaries by key?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024)
      .system("You are a helpful coding assistant specializing in Python.")
      .addUserMessage("How do I sort a list of dictionaries by key?")
      .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'How do I sort a list of dictionaries by key?']
      ],
      model: Model::CLAUDE_OPUS_5_5,
      system: 'You are a helpful coding assistant specializing in Python.',
  );

  echo json_encode($message->content, JSON_PRETTY_PRINT), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    system: "You are a helpful coding assistant specializing in Python.",
    messages: [
      { role: "user", content: "How do I sort a list of dictionaries by key?" }
    ]
  )

  puts message.content
  ```
</CodeGroup>

### 长上下文提示

处理大型文档或数据密集型输入（20k+ token）时，请仔细组织 prompt 结构，以获得最佳效果：

* **把长篇数据放在开头：** 把长文档和输入放在 prompt 靠近顶部的位置，位于你的查询、指令和示例之前。这在所有模型上都能提升表现。

  <Note>
    测试显示，把查询放在末尾最多可将回复质量提升 30%，对复杂的多文档输入尤其如此。
  </Note>

* **用 XML 标签组织文档内容与元数据：** 使用多个文档时，把每个文档包在 `<document>` 标签里，并用 `<document_content>` 和 `<source>`（以及其他元数据）子标签，以求清晰。

  <Accordion title="示例：多文档结构">
    ```xml
    <documents>
      <document index="1">
        <source>annual_report_2023.pdf</source>
        <document_content>
          {{ANNUAL_REPORT}}
        </document_content>
      </document>
      <document index="2">
        <source>competitor_analysis_q2.xlsx</source>
        <document_content>
          {{COMPETITOR_ANALYSIS}}
        </document_content>
      </document>
    </documents>

    Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.
    ```
  </Accordion>

* **让回复以引文为依据：** 对长文档任务，先让 Claude 引用文档中与任务相关的部分，再执行任务。这能帮助 Claude 聚焦相关内容、忽略文档的其余部分。

  <Accordion title="示例：引文提取">
    ```xml
    You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.

    <documents>
      <document index="1">
        <source>patient_symptoms.txt</source>
        <document_content>
          {{PATIENT_SYMPTOMS}}
        </document_content>
      </document>
      <document index="2">
        <source>patient_records.txt</source>
        <document_content>
          {{PATIENT_RECORDS}}
        </document_content>
      </document>
      <document index="3">
        <source>patient01_appt_history.txt</source>
        <document_content>
          {{PATIENT01_APPOINTMENT_HISTORY}}
        </document_content>
      </document>
    </documents>

    Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in <quotes> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in <info> tags.
    ```
  </Accordion>

### 模型自我认知

如果你希望 Claude 在你的应用中正确表明身份，或使用特定的 API 字符串：

```text Sample prompt for model identity wrap
The assistant is Claude, created by Anthropic. The current model is Claude Opus 5.5.
```

对于需要指定模型字符串的 LLM 应用：

```text Sample prompt for model string wrap
When an LLM is needed, please default to Claude Opus 5.5 unless the user requests
otherwise. The exact model string for Claude Opus 5.5 is claude-opus-5-5.
```

## 输出与格式

### 沟通风格与详略程度

与之前的模型相比，Claude 的最新模型沟通风格更简洁、更自然：

* **更直接、更有依据：** 给出基于事实的进度报告，而不是自我表功式的更新
* **更口语化：** 略更流利、更贴近对话，机器感更弱
* **更简略：** 除非另有提示，可能为了效率省略详细的总结

这意味着 Claude 在工具调用之后可能会跳过口头总结，直接进行下一个动作。如果你希望更清楚地看到它的工作过程：

```text Sample prompt wrap
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

Claude Opus 5 在详略程度上是个例外：它面向用户的默认回复比之前的模型更长，而且调高或调低 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 并不能可靠地改变可见的回复长度。请改为在 prompt 中明确要求简洁，示例指令见 [Claude Opus 5 提示词指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity)。Claude Fable 5.1 在智能体工作中的倾向则相反：它在工具调用之间写的面向用户的更新更少。请明确要求输出进度文本，并删除任何要求它保持该文本简短的指令。参见[请求面向用户的进度更新](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates)。

### 控制回复的格式

有几种引导输出格式特别有效的方法：

1. **告诉 Claude 该做什么，而不是不该做什么**

   * 与其说：“不要在回复中使用 markdown”
   * 不如说：“你的回复应当由流畅连贯的散文段落组成。”

2. **使用 XML 格式指示**

   * 不妨说：“把你回复中的散文部分写在 \<smoothly\_flowing\_prose\_paragraphs> 标签里。”

3. **让 prompt 风格与想要的输出保持一致**

   prompt 中使用的格式风格可能会影响 Claude 的回复风格。如果你在输出格式的可控性上仍然遇到问题，可以尝试让 prompt 的风格尽可能贴近你想要的输出风格。例如，去掉 prompt 中的 markdown 可以减少输出中 markdown 的量。

4. **针对特定格式偏好使用详细的 prompt**

   要更精细地控制 markdown 和格式的使用，请提供明确的指引：

````text Sample prompt to minimize markdown wrap
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form
content, write in clear, flowing prose using complete paragraphs and sentences. Use
standard paragraph breaks for organization and reserve markdown primarily for `inline
code`, code blocks (```...```), and simple headings (## and ###). Avoid using **bold**
and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless: a) you're presenting
truly discrete items where a list format is the best option, or b) the user explicitly
requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into
sentences. This guidance applies especially to technical writing. Using prose instead of
excessive formatting will improve user satisfaction. NEVER output a series of overly
short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas
rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
````

Claude Fable 5.1 本身的格式化就比早期模型少，因此在该模型上，这样一段提示可能会压制内容需要的结构。请删掉它，或替换为[聊天中的格式化](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#formatting-in-chat)中更简短的规则。

### LaTeX 输出

Claude 的最新模型默认使用 LaTeX 呈现数学表达式、公式和技术性说明。如果你更喜欢纯文本，请在 prompt 中加入以下指令：

```text Sample prompt wrap
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup
notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text
characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

### 文档创建

Claude 的最新模型在创建演示文稿、动画和可视化文档时具有很强的指令遵循能力，通常第一次尝试就能产出可用的结果。

要想在文档创建中获得最佳效果：

```text Sample prompt wrap
Create a professional presentation on [topic]. Include thoughtful design elements,
visual hierarchy, and engaging animations where appropriate.
```

### 从预填充回复迁移

从 Claude 4.6 系列模型和 [Claude Mythos Preview](https://anthropic.com/glasswing) 开始，最后一个 assistant 回合上的预填充（prefill）回复（即为 Claude 提供一条让它接着写下去的部分 assistant 消息）不再受支持。向这些模型发送带预填充 assistant 消息的请求会返回 400 错误。模型的智能水平和指令遵循能力已经进步到大多数 prefill 用例不再需要它。较早的模型仍支持 prefill，在对话的其他位置添加 assistant 消息也不受影响。

以下是常见的 prefill 场景及其迁移方式：

<Accordion title="控制输出格式">
  预填充（prefill）一直被用来强制特定输出格式，例如 JSON/YAML、分类任务等，即利用 prefill 把 Claude 约束到某个特定结构。

  **迁移方案：** [结构化输出（structured outputs）](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)功能正是为了把 Claude 的回复约束为遵循给定 schema 而设计的。可以先尝试直接要求模型遵循你的输出结构——新模型在被要求时能够可靠地匹配复杂 schema，尤其是配合重试机制使用时。对于分类任务，可以使用带枚举字段（包含你的有效标签）的工具，或使用结构化输出。
</Accordion>

<Accordion title="消除开场白">
  像 `Here is the requested summary:\n` 这样的预填充曾被用来跳过开场文本。

  **迁移方案：** 在系统提示词中使用直接指令：“直接作答，不加开场白。不要以‘Here is...’、‘Based on...’之类的短语开头。” 或者，引导模型在 XML 标签内输出、使用结构化输出，或使用工具调用。如果偶尔仍有开场白漏出来，可以在后处理中去掉。
</Accordion>

<Accordion title="避免不当拒绝">
  预填充曾被用来绕过不必要的拒绝。

  **迁移方案：** 如今 Claude 对何时应当拒绝的把握已大为改善。在 `user` 消息内进行清晰的提示（不使用 prefill）就足够了。
</Accordion>

<Accordion title="续写">
  预填充曾被用来继续未完成的生成、恢复被中断的回复，或从上一次生成结束的地方接着扩展。

  **迁移方案：** 把续写请求移到 user 消息中，并附上被中断回复的最后一段文本：“你之前的回复被中断，结尾是 \`\[previous\_response]\`。请从你停下的地方继续。” 如果这属于错误处理或不完整回复处理流程的一部分、且没有 UX 上的代价，可以直接重试请求。
</Accordion>

<Accordion title="上下文补充与角色一致性">
  预填充曾被用来定期确保上下文被刷新或注入。

  **迁移方案：** 对于很长的对话，把以前通过 prefill 注入的 assistant 提醒放进 user 回合。如果上下文补充是更复杂的智能体系统的一部分，可以考虑通过工具来补充（暴露或鼓励使用包含上下文的工具，依据轮数之类的启发式规则），或在[上下文压缩（compaction）](https://platform.claude.com/docs/en/build-with-claude/compaction)期间进行。
</Accordion>

## 工具使用

### 工具的使用

Claude 的最新模型为精确的指令遵循而训练，受益于明确指示其使用特定工具。如果你说“你能建议一些修改吗”，Claude 有时只会给出建议而不动手修改，尽管你的本意可能正是让它修改。要了解如何定义工具以及排查工具触发问题，请参阅 [Claude 的工具使用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。

要让 Claude 采取行动，请说得更明确：

<Accordion title="示例：明确指令" defaultOpen>
  **效果一般（Claude 只会给建议）：**

  ```text wrap
  Can you suggest some changes to improve this function?
  ```

  **效果更好（Claude 会直接修改）：**

  ```text wrap
  Change this function to improve its performance.
  ```

  或者：

  ```text wrap
  Make these edits to the authentication flow.
  ```
</Accordion>

要让 Claude 默认更主动地采取行动，可以把下面这段加进系统提示词：

```text Sample prompt for proactive action wrap
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is
unclear, infer the most useful likely action and proceed, using tools to discover any
missing details instead of guessing. Try to infer the user's intent about whether a tool
call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

反过来，如果你希望模型默认更谨慎、不急于立刻开始实现、只在被要求时才采取行动，可以用类似下面的 prompt 来引导这种行为：

```text Sample prompt for conservative action wrap
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make
changes. When the user's intent is ambiguous, default to providing information, doing
research, and providing recommendations rather than taking action. Only proceed with
edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

Claude Opus 4.5 和 Claude Opus 4.6 对系统提示词的响应也比之前的模型更强。如果你的 prompt 是为了缓解工具或技能触发不足而设计的，这些模型现在可能触发过度。解决办法是放缓激进措辞。以前你可能写“CRITICAL: You MUST use this tool when...”，现在可以改用更平常的提示，例如“Use this tool when...”。

### 优化并行工具调用

Claude 的最新模型会并行执行相互独立的工具调用。这些模型会：

* 研究时并行执行多个探索性搜索
* 一次读取多个文件，更快建立上下文
* 并行运行 bash 命令（甚至可能把系统性能拖成瓶颈）

这种行为是可以引导的。虽然不加提示时模型并行调用工具的成功率已经很高，你仍可以把它提升到约 100%，或调整激进程度：

```text Sample prompt for maximum parallel efficiency wrap
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool
calls, make all of the independent tool calls in parallel. Prioritize calling tools
simultaneously whenever the actions can be done in parallel rather than sequentially.
For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into
context at the same time. Maximize use of parallel tool calls where possible to increase
speed and efficiency. However, if some tool calls depend on previous calls to inform
dependent values like the parameters, do NOT call these tools in parallel and instead
call them sequentially. Never use placeholders or guess missing parameters in tool
calls.
</use_parallel_tool_calls>
```

```text Sample prompt to reduce parallel execution wrap
Execute operations sequentially with brief pauses between each step to ensure stability.
```

在 Claude Fable 5.1 的长智能体循环中，请在每轮工具结果之后，以回合级（turn-scoped）系统消息的形式发送并行调用指令。参见[在智能体循环中批量执行独立工具调用](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops)。

## 思考与推理

### 过度思考与过度求全

Claude Opus 4.6 比之前的模型做更多的前期探索，尤其是在较高的 [`effort`](https://platform.claude.com/docs/en/build-with-claude/effort) 设置下。这些初期工作通常有助于优化最终结果，但模型可能会在没有提示的情况下收集大量上下文或推进多条研究线。如果你以前的 prompt 鼓励模型更加周全，就应该针对 Claude Opus 4.6 调整这些指引：

* **用更有针对性的指令取代一刀切的默认规则。** 不要写“默认使用 \[tool]”，而是加上诸如“当 \[tool] 有助于加深你对问题的理解时使用它”的指引。
* **去掉过度提示。** 之前触发不足的工具现在大概率会恰当触发。“拿不准就用 \[tool]”这类指令会导致触发过度。
* **把 effort 当作兜底手段。** 如果 Claude 仍然过于激进，就给 `effort` 设一个更低的级别。

在某些情况下，Claude Opus 4.6 可能会思考得非常久，导致 thinking token 膨胀、回复变慢。如果不希望出现这种行为，可以添加明确指令约束其推理，或调低 `effort` 设置以减少总体思考和 token 消耗。

```text Sample prompt wrap
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

如果你需要给思考成本设一个硬上限：带 `budget_tokens` 上限的扩展思考（extended thinking）在 Opus 4.6 和 Sonnet 4.6 上仍可使用，但已被弃用。在 Claude 4.7 及之后的模型上，设置 `budget_tokens` 会返回 400 错误。请改用更低的 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 设置，或配合[自适应思考（adaptive thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking)用 `max_tokens` 作为硬性上限。

### 善用思考与交错思考能力

Claude 的最新模型提供思考能力，对涉及工具使用后的反思或复杂多步推理的任务尤其有帮助。你可以引导它的初始思考或交错思考（interleaved thinking），以获得更好的结果。

Claude 4.6 及之后的模型和 Claude Mythos Preview 使用[自适应思考（adaptive thinking）](https://platform.claude.com/docs/en/build-with-claude/thinking)（`thinking: {type: "adaptive"}`），由 Claude 动态决定何时思考、思考多少。在 Claude Fable 5.1、Claude Mythos 5.1、Claude Fable 5、Claude Mythos 5 和 Claude Opus 5.5 上，思考始终开启，自适应思考是唯一模式。Claude 根据两个因素校准思考：`effort` 参数和查询复杂度。更高的 effort 会带来更多思考，更复杂的查询同样如此。对不需要思考的简单查询，模型直接作答。在内部评测中，自适应思考稳定地带来比扩展思考更好的表现。请考虑迁移到自适应思考。

对需要智能体行为的工作负载（如多步工具使用、复杂编码任务和长时程（long-horizon）智能体循环），请使用自适应思考。较老的模型使用带 `budget_tokens` 的手动[扩展思考（extended thinking）](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)；每种模型接受哪种配置，请参见[各模型配置表](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models)。

你可以引导 Claude 的思考行为：

```text Example prompt wrap
After receiving tool results, carefully reflect on their quality and determine optimal
next steps before proceeding. Use your thinking to plan and iterate based on this new
information, and then take the best next action.
```

自适应思考的触发行为是可以通过 prompt 引导的。如果发现模型思考得比期望更频繁（在大型或复杂系统 prompt 下可能出现这种情况），可以添加指引：

```text Sample prompt wrap
Thinking adds latency and should only be used when it will meaningfully improve
answer quality - typically for problems that require multistep reasoning. When in
doubt, respond directly.
```

如果你正从带 `budget_tokens` 的[扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)迁移过来，请替换你的思考配置，把预算控制移到 `effort` 上。下面的示例展示同一请求迁移前后的写法（可用级别和各模型的可用情况见 [effort](https://platform.claude.com/docs/en/build-with-claude/effort)）：

<CodeGroup>
  ```bash cURL
  # Before: extended thinking with a manual budget (older models)
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 16000,
      "thinking": {"type": "enabled", "budget_tokens": 10000},
      "messages": [
        {"role": "user", "content": "..."}
      ]
    }'

  # After: adaptive thinking with effort
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 16000,
      "thinking": {"type": "adaptive"},
      "output_config": {"effort": "high"},
      "messages": [
        {"role": "user", "content": "..."}
      ]
    }'
  ```

  ```bash CLI
  # Before: extended thinking with a manual budget (older models)
  ant messages create <<'YAML'
  model: claude-sonnet-4-5-20250929
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  messages:
    - role: user
      content: "..."
  YAML

  # After: adaptive thinking with effort
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 16000
  thinking:
    type: adaptive
  output_config:
    effort: high
  messages:
    - role: user
      content: "..."
  YAML
  ```

  ```python Python
  # Before: extended thinking with a manual budget (older models)
  client.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      messages=[{"role": "user", "content": "..."}],
  )

  # After: adaptive thinking with effort
  client.messages.create(
      model="claude-opus-5-5",
      max_tokens=16000,
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  // Before: extended thinking with a manual budget (older models)
  await client.messages.create({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 16000,
    thinking: { type: "enabled", budget_tokens: 10000 },
    messages: [{ role: "user", content: "..." }]
  });

  // After: adaptive thinking with effort
  await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: "high" },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  // Before: extended thinking with a manual budget (older models)
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_5_20250929,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages = [new UserMessageParam { Content = "..." }]
  });

  // After: adaptive thinking with effort
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive(),
      OutputConfig = new OutputConfig { Effort = Effort.High },
      Messages = [new UserMessageParam { Content = "..." }]
  });
  ```

  ```go Go
  // Before: extended thinking with a manual budget (older models)
  client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_5_20250929,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfEnabled: &anthropic.ThinkingConfigEnabledParam{BudgetTokens: 10000},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })

  // After: adaptive thinking with effort
  client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortHigh,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  // Before: extended thinking with a manual budget (older models)
  client.messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_4_5_20250929)
      .maxTokens(16000L)
      .thinking(ThinkingConfigEnabled.builder()
          .budgetTokens(10000L)
          .build())
      .addUserMessage("...")
      .build());

  // After: adaptive thinking with effort
  client.messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(16000L)
      .thinking(ThinkingConfigAdaptive.builder().build())
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.HIGH)
          .build())
      .addUserMessage("...")
      .build());
  ```

  ```php PHP
  // Before: extended thinking with a manual budget (older models)
  $client->messages->create(
      model: 'claude-sonnet-4-5-20250929',
      maxTokens: 16000,
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
      messages: [['role' => 'user', 'content' => '...']],
  );

  // After: adaptive thinking with effort
  $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 16000,
      thinking: ['type' => 'adaptive'],
      outputConfig: ['effort' => 'high'],
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  # Before: extended thinking with a manual budget (older models)
  client.messages.create(
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 16000,
    thinking: { type: "enabled", budget_tokens: 10000 },
    messages: [{ role: "user", content: "..." }]
  )

  # After: adaptive thinking with effort
  client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: "high" },
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

如果你不使用扩展思考，就不需要添加 `thinking` 参数。在 Claude Opus 4.6 到 Claude Opus 4.8 以及 Claude Sonnet 4.6 上，省略 `thinking` 参数时思考是关闭的。在 Claude Opus 5、Claude Sonnet 5.5、Claude Sonnet 5 和 Claude Haiku 5.5 上，省略 `thinking` 参数时思考默认开启，因此回复可能以 `thinking` 块开头。请按 `type` 而不是按位置来挑选内容块，并在 `max_tokens` 中为思考留出空间。在 Claude Opus 5 和 Claude Haiku 5.5 上，只有 effort 为 `high` 或更低时才能关闭思考。在 Claude Sonnet 5.5 上，最低的思考设置是 `between_tools`，在 effort 为 `high` 或更低时被接受。在 Claude Fable 5.1、Claude Mythos 5.1、Claude Fable 5、Claude Mythos 5 和 Claude Opus 5.5 上，思考始终开启，无论你是否设置 `thinking` 参数。

* **偏好一般性指令而非规定性步骤。** 像“think thoroughly”（认真思考）这样的 prompt 往往比手写的分步计划产生更好的推理。Claude 的推理常常超出人工规定的水平。
* **多样本示例与思考配合有效。** prompt 中的完整示例会影响 Claude 在自己的 thinking 块中处理类似问题的方式。每个示例按“问题 + 要采用的方法 + 预期答案”的形式呈现。
* **手动思维链（chain of thought，CoT）提示作为兜底。** 关闭思考时，你仍然可以鼓励逐步推理：让 Claude 在回答前先把问题想清楚，并把最终答案放在 `<answer>` 标签里以便你提取。在 Claude Fable 5.1、Claude Fable 5、Claude Opus 5.5、Claude Opus 5 和 Claude Sonnet 5.5 上，请改用 thinking；如果成本或延迟重要，就用更低的 [effort](https://platform.claude.com/docs/en/build-with-claude/effort) 级别：要求模型写出推理过程的 prompt（例如写在 `<thinking>` 标签里）可能会被拒绝。参见[把推理保留在 thinking 块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)。
* **让 Claude 自查。** 附上类似“完成之前，请对照 \[test criteria] 验证你的答案”的要求。这能可靠地捕获错误，对编码和数学任务尤其如此。Claude Opus 5 是例外：它无需明确指令就能把自己的工作验证得很好，从为早期模型调优的 prompt 沿袭下来的验证指令反而会导致过度验证，增加 token 和延迟。在 Claude Opus 5 上，请直接删除这些指令，而不是改写。参见[任务范围与过度验证](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification)。

<Note>
  当扩展思考被禁用时，Claude Opus 4.5 对“think”一词及其变体尤其敏感。这些情况下，可考虑改用“consider”“evaluate”或“reason through”等替代说法。
</Note>

<Info>
  有关思考能力的更多信息，请参阅[思考](https://platform.claude.com/docs/en/build-with-claude/thinking)与[引导思考](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)。
</Info>

## 智能体系统

### 长时程推理与状态跟踪

Claude 的最新模型能够以很强的状态跟踪能力处理长时程推理任务。Claude 通过专注于渐进式进展，在长时间会话中保持方向感：一次稳步推进少数几件事，而不是试图一口气做完所有事。这种能力尤其体现在跨越多个上下文窗口或任务迭代的场景中：Claude 可以处理一项复杂任务、保存状态，然后带着全新的上下文窗口继续。

#### 上下文感知与多窗口工作流

Claude Sonnet 5、Claude Sonnet 4.6、Claude Sonnet 4.5（已弃用）和 Claude Haiku 4.5 具备[上下文感知（context awareness）](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-awareness)能力，让模型能够在整个对话中跟踪剩余的上下文窗口（也就是它的“token 预算”）。这使 Claude 可以根据自己还有多少可用空间，更有效地执行任务和管理上下文。

**管理上下文上限：**

如果你在会压缩上下文或允许把上下文保存到外部文件的智能体框架（如 Claude Code）中使用 Claude，可以考虑把这些信息写进 prompt，让 Claude 据此行动。否则，随着接近上下文上限，Claude 有时可能会自然而然地尝试提前收尾工作。下面是一个示例 prompt：

```text Sample prompt wrap
Your context window will be automatically compacted as it approaches its limit, allowing
you to continue working indefinitely from where you left off. Therefore, do not stop
tasks early due to token budget concerns. As you approach your token budget limit, save
your current progress and state to memory before the context window refreshes. Always be
as persistent and autonomous as possible and complete tasks fully, even if the end of
your budget is approaching. Never artificially stop any task early regardless of the
context remaining.
```

[记忆工具（memory tool）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)与上下文感知配合得很好，可用于管理上下文过渡。

#### 跨多个上下文窗口的工作流

对于跨越多个上下文窗口的任务：

1. **为第一个上下文窗口使用不同的 prompt：** 用第一个上下文窗口搭建框架（写测试、创建初始化脚本），再用后续的上下文窗口迭代待办清单。

2. **让模型以结构化格式写测试：** 让 Claude 在开始工作前创建测试，并用结构化格式（例如 `tests.json`）跟踪它们。这有利于长期的迭代能力。提醒 Claude 测试的重要性：“删除或修改测试是不可接受的，否则可能导致功能缺失或引入 bug。”

3. **设置便利工具：** 鼓励 Claude 创建初始化脚本（例如 `init.sh`），优雅地启动服务器并运行测试套件和 linter。这样从全新上下文窗口继续时就不会重复劳动。

4. **在全新开始与压缩之间做选择：** 清空上下文窗口时，可以考虑使用全新的上下文窗口，而不是压缩（compaction）。Claude 的最新模型非常擅长从本地文件系统中发现状态，某些情况下你可以利用这一点来取代压缩。要明确规定它应如何开始：

   * “运行 pwd；你只能读写该目录下的文件。”
   * “查看 progress.txt、tests.json 和 git 日志。”
   * “在着手实现新功能之前，先手动完整跑通一个基本的集成测试。”

5. **提供验证工具：** 随着自主任务时长增长，Claude 需要在没有持续人工反馈的情况下验证正确性。能让 Claude 验证 UI 工作的工具很有帮助，例如[计算机使用工具（computer use tool）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[浏览器使用工具（browser use tool）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)或浏览器自动化 MCP 服务器。

6. **鼓励充分利用上下文：** 提示 Claude 高效完成各个组件后再继续：

```text Sample prompt wrap
This is a very long task, so it may be beneficial to plan out your work clearly. It's
encouraged to spend your entire output context working on the task - just make sure you
don't run out of context with significant uncommitted work. Continue working
systematically until you have completed this task.
```

#### 状态管理最佳实践

* **用结构化格式保存状态数据：** 跟踪结构化信息（如测试结果或任务状态）时，使用 JSON 或其他结构化格式，把 schema 要求对 Claude 说明白。
* **用非结构化文本写进度笔记：** 自由格式的进度笔记适合跟踪总体进展和上下文。
* **用 git 跟踪状态：** Git 提供已完成工作的日志和可恢复的检查点。Claude 的最新模型尤其擅长用 git 跨多个会话跟踪状态。
* **强调渐进式进展：** 明确要求 Claude 记录自己的进度，专注于渐进式工作。

<Accordion title="示例：状态跟踪">
  ```json tests.json
  {
    "tests": [
      { "id": 1, "name": "authentication_flow", "status": "passing" },
      { "id": 2, "name": "user_management", "status": "failing" },
      { "id": 3, "name": "api_endpoints", "status": "not_started" }
    ],
    "total": 200,
    "passing": 150,
    "failing": 25,
    "not_started": 25
  }
  ```

  ```text wrap
  // Progress notes (progress.txt)
  Session 3 progress:
  - Fixed authentication token validation
  - Updated user model to handle edge cases
  - Next: investigate user_management test failures (test #2)
  - Note: Do not remove tests as this could lead to missing functionality
  ```
</Accordion>

### 平衡自主性与安全性

在没有指引的情况下，Claude Opus 4.6 可能会采取难以撤销或影响共享系统的操作，例如删除文件、force-push 或向外部服务发布内容。如果你希望 Claude Opus 4.6 在采取有潜在风险的操作前先确认，请在 prompt 中加入指引：

```text Sample prompt wrap
Consider the reversibility and potential impact of your actions. You are encouraged to
take local, reversible actions like editing files or running tests, but for actions that
are hard to reverse, affect shared systems, or could be destructive, ask the user before
proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending
messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example,
don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be
in-progress work.
```

### 研究与信息收集

Claude 的最新模型能够有效地从多个来源查找并综合信息。要获得最佳研究效果：

1. **提供明确的成功标准：** 定义对你的研究问题而言，什么样的回答算成功。

2. **鼓励来源验证：** 让 Claude 在多个来源之间交叉验证信息。

3. **对复杂研究任务使用结构化方法：**

```text Sample prompt for complex research wrap
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track your confidence levels in your progress notes to improve
calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or
research notes file to persist information and provide transparency. Break down this
complex research task systematically.
```

这种结构化方法能帮助 Claude 有条不紊地处理大型语料库，并反复审视自己的发现。

### 子智能体编排

Claude 的最新模型原生支持编排子智能体（subagent）。这些模型能够识别哪些任务适合委派给专门的子智能体，并主动这样做，无需明确指令。

要利用这种行为：

1. **确保子智能体工具定义完善：** 提供子智能体工具，并在工具定义中描述清楚。
2. **让 Claude 自然编排：** Claude 无需明确指令就能恰当地委派。
3. **警惕过度使用：** Claude Opus 4.6 有很强的使用子智能体的倾向，在更简单的直接方法就足够的场合也可能生成子智能体。例如，直接调用 grep 更快也够用时，模型可能还是为代码探索生成子智能体。Claude Opus 5 也比之前的模型更愿意委派给子智能体；指引和抑制用的示例 prompt 见[控制子智能体的生成](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning)。

如果你发现子智能体被过度使用，请添加关于何时适合、何时不适合使用子智能体的明确指引：

```text Sample prompt for subagent usage wrap
Use subagents when tasks can run in parallel, require isolated context, or involve
independent workstreams that don't need to share state. For simple tasks, sequential
operations, single-file edits, or tasks where you need to maintain context across steps,
work directly rather than delegating.
```

### 复杂 prompt 的链式执行

有了自适应思考和子智能体编排，Claude 能在内部处理大多数多步推理。当你需要检查中间输出或强制执行特定的流水线结构时，显式的提示词链（prompt chaining，把任务拆分为顺序的 API 调用）仍然有用。

最常见的链式模式是**自我修正（self-correction）**：生成草稿 → 让 Claude 对照标准评审 → 让 Claude 根据评审修改。每一步都是单独的 API 调用，因此你可以在任何环节记录日志、评测或分支。

### 减少智能体编码中的文件创建

Claude 的最新模型有时会出于测试和迭代的目的创建新文件，在处理代码时尤其如此。这让 Claude 可以把文件（尤其是 Python 脚本）当作保存最终输出前的“临时草稿本”。使用临时文件可以改善结果，对智能体编码场景尤其明显。

如果你希望尽量少留下新文件，可以指示 Claude 自己收尾清理：

```text Sample prompt wrap
If you create any temporary new files, scripts, or helper files for iteration, clean up
these files by removing them at the end of the task.
```

### 过度积极

Claude Opus 4.5 和 Claude Opus 4.6 有过度工程化的倾向：创建多余文件、添加不必要的抽象，或者构建没人要求的灵活性。如果你发现这种不希望出现的行为，请添加具体指引，让方案保持精简。

例如：

```text Sample prompt to minimize overengineering wrap
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was
asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need
extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't
change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios
that can't happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time
operations. Don't design for hypothetical future requirements. The right amount of
complexity is the minimum needed for the current task.
```

### 避免专注于让测试通过与硬编码

Claude 有时会把过多注意力放在让测试通过上，而牺牲更通用的解法；或者使用变通手段（例如用辅助脚本完成复杂重构），而不直接使用标准工具。要防止这种行为、获得可泛化的解法：

```text Sample prompt wrap
Please write a high-quality, general-purpose solution using the standard tools
available. Do not create helper scripts or workarounds to accomplish the task more
efficiently. Implement a solution that works correctly for all valid inputs, not just
the test cases. Do not hard-code values or create solutions that only work for specific
test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm.
Tests are there to verify correctness, not to define the solution. Provide a principled
implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please
inform me rather than working around them. The solution should be robust, maintainable,
and extendable.
```

### 减少智能体编码中的幻觉

Claude 的最新模型更不容易产生幻觉（hallucination），能基于代码给出更准确、更有依据、更聪明的回答。要进一步鼓励这种行为、把幻觉降到最低：

```text Sample prompt wrap
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Make sure to investigate and read relevant
files BEFORE answering questions about the codebase. Never make any claims about code
before investigating unless you are certain of the correct answer - give grounded and
hallucination-free answers.
</investigate_before_answering>
```

## 特定能力技巧

### 改进的视觉能力

与之前的 Claude 模型相比，Claude Opus 4.5 和 Claude Opus 4.6 的视觉能力更强。它们在图像处理和数据提取任务上表现更好，尤其是上下文中存在多张图像时。这些改进也延伸到计算机使用（computer use）场景，模型能更可靠地解读截图和 UI 元素。你还可以把视频拆成帧，用这些模型进行分析。

一种被证明能进一步提升表现的有效技巧，是给 Claude 一个裁剪工具（crop tool）或[智能体技能（agent skill）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。测试显示，当 Claude 能够“放大”查看图像的相关区域时，图像评测成绩持续提升。Anthropic 为裁剪工具提供了一个[配方（recipe）](https://platform.claude.com/cookbook/multimodal-crop-tool)。

### 前端设计

Claude Opus 4.5 和 Claude Opus 4.6 能构建出具有出色前端设计的复杂真实世界 Web 应用。但如果没有指引，模型可能默认套用千篇一律的模式，落入用户所说的“AI slop”（AI 垃圾风）审美。要创建令人惊喜、愉悦的独特创意前端：

<Tip>
  关于改进前端设计的详细指南，请阅读博文[通过技能改进前端设计](https://www.claude.com/blog/improving-frontend-design-through-skills)。
</Tip>

对于 API 之外的前端设计工作，[Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) 提供了画布和设计工具，Claude 可以在其中交互式地生成并迭代设计。

下面是一段可用于鼓励更好前端设计的系统提示词片段：

```text Sample prompt for frontend aesthetics wrap
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this
creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive
frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic
fonts like Arial and Inter; opt instead for distinctive choices that elevate the
frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency.
Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw
from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only
solutions for HTML. Use Motion library for React when available. Focus on high-impact
moments: one well-orchestrated page load with staggered reveals (animation-delay)
creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer
CSS gradients, use geometric patterns, or add contextual effects that match the overall
aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the
context. Vary between light and dark themes, different fonts, different aesthetics. You
still tend to converge on common choices (Space Grotesk, for example) across
generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

你也可以参考[完整的技能定义](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)。

### 药物剂量

如果用户可能向你的应用询问药物剂量，请把下面与你应用所调用模型对应的代码块原样加入你的系统提示词，一字不改。该代码块让 Claude 从产品标签而非记忆中给出儿童的非处方药剂量。有网页搜索时（例如[网页搜索工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)），Claude 会在回答前核对标签，这会增加延迟和搜索成本。没有网页搜索时，Claude 会引导用户查看标签上的剂量表、咨询药师或儿童医生，而不是直接给出剂量。

```text Medication dosing block for Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, and Claude Sonnet 5 wrap
<medical_guidance>
This applies only when the person explicitly says the medicine is for a child, and isn't a healthcare professional asking for work.
Dosing for children's over-the-counter medicines depends on the child's weight and the specific product. For infants and toddlers, a small error can cause real harm. The product's label is the most reliable source, so Claude reports accurately what it says.
If neither the child's age or weight is given, Claude asks for both. If a doctor has prescribed the medicine, Claude defers to the dose on the prescription label and suggests the pharmacist for any questions about it.
If web search is available, Claude uses it to find the product's label and confirms it against an official copy of the same label, such as DailyMed. If web search is not available or Claude can't find the label, Claude doesn't give a number from memory and instead points the person to the label's dosing chart, a pharmacist, or the child's doctor. Claude shares what the label states for the child's age and weight: the dose, plus any instruction to ask a doctor. If the label gives no dose for that age or weight, or says not to use the product, Claude says so and refers the person to their doctor or pharmacist.
</medical_guidance>
```

```text Medication dosing block for Claude Haiku 5.5 wrap
<medical_guidance>
This applies only when the person explicitly says the medicine is for a child, and isn't a healthcare professional asking for work.
Dosing for children's over-the-counter medicines depends on the child's age or weight and the specific product. For infants and toddlers, a small error can cause real harm. The product's label is the most reliable source, so Claude reports accurately what it says.
If neither the child's age or weight is given, Claude asks for both. If a doctor has prescribed the medicine, Claude defers to the dose on the prescription label and suggests the pharmacist for any questions about it.
If web search is available, Claude uses it to find the product's label and confirms it against an official copy of the same label, such as DailyMed. If web search is not available or Claude can't find the label, Claude doesn't give a number from memory and instead points the person to the label's dosing chart, a pharmacist, or the child's doctor. Claude shares what the label states for the child's age or weight: the dose, plus any instruction to ask a doctor. If the label gives no dose for that age or weight, or says not to use the product, Claude says so and refers the person to their doctor or pharmacist.
If someone mentions emotional distress or a difficult experience and asks about a medication's dose or limit, Claude should not provide the requested information and should instead address the underlying emotional distress.
</medical_guidance>
```

```text Medication dosing block for Claude Sonnet 4.6 wrap
<medical_guidance>
If web search is available, Claude uses it to find the children's medicine label and confirms it against an official copy of the same label, such as DailyMed. Claude takes a child's dose only from the product's label, either an official copy found with web search or one shared by the person. Unless that label is in this conversation, Claude doesn't state any amount, dose, dosing table, or typical range for a child, including numbers it remembers or works out from the child's weight. Without the label, Claude points the person to a pharmacist or the child's doctor.
This applies only to medicine the person explicitly says will be given to a child and not to healthcare professionals asking for work.
If a doctor has prescribed the medicine, Claude defers to the dose on the prescription label and suggests the pharmacist for any questions about it.
If neither the child's age nor weight is given, Claude asks for both.
Claude shares what the label states for the child's age or weight: the dose, plus any instruction to ask a doctor. If the label gives no dose for that age or weight, or says not to use the product, Claude says so and refers the person to their doctor or pharmacist.
</medical_guidance>
```

```text Medication dosing block for Claude Haiku 4.5 wrap
<medical_guidance>
When someone asks about a medicine for a child and web search is available, Claude uses it to find that medicine's label and confirms it against an official copy, such as DailyMed.
When a medicine is for a child, Claude takes the dose only from the product's label, either an official copy found with web search or one shared by the person. Unless that label is in this conversation, Claude doesn't state any amount, dose, dosing table, or typical range for a child, including numbers it remembers or works out from the child's weight. Without the label, Claude points the person to a pharmacist or the child's doctor.
Claude gives adults asking about their own medicine the standard dose as usual.
If no child is mentioned, Claude answers as it would for an adult.
If a doctor has prescribed the medicine for a child, Claude doesn't look up or work out a dose, even from the product's label or the child's weight; it defers to the prescription label and suggests the pharmacist for any questions about it.
If neither the child's age nor weight is given, Claude asks for both.
Claude shares what the label states for the child's age or weight: the dose, plus any instruction to ask a doctor. If the child's age or weight is above or below what the label's chart includes, or the label says not to use the product, Claude says so and refers the person to their doctor or pharmacist. Claude doesn't give doses from charts other than the product's label.
</medical_guidance>
```

## 迁移注意事项

从早期几代模型迁移到当前的 Claude 模型时：

1. **具体说明你想要的行为：** 考虑精确描述你希望在输出中看到什么。

2. **用修饰语框定指令：** 添加鼓励 Claude 提升输出质量和细节的修饰语，有助于更好地塑造 Claude 的表现。例如，不要用“创建一个分析仪表盘”，而用“创建一个分析仪表盘。尽可能多地纳入相关功能和交互。超越基础，做出功能完备的实现。”

3. **明确请求特定功能：** 想要动画和交互元素时，明确提出来。

4. **更新思考配置：** Claude 4.6 及之后的模型使用[自适应思考](https://platform.claude.com/docs/en/build-with-claude/thinking)（`thinking: {type: "adaptive"}`）取代带 `budget_tokens` 的手动思考。在 Claude 4.7 及之后的模型上，设置 `budget_tokens` 会返回 400 错误。请使用 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort)来控制思考深度。

5. **从预填充回复迁移：** 从 Claude 4.6 系列模型和 Claude Mythos Preview 开始，最后一个 assistant 回合上的预填充回复不再受支持。替代方案的详细指引见[从预填充回复迁移](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#migrating-away-from-prefilled-responses)。

6. **调整防偷懒提示：** 如果你以前的 prompt 鼓励模型更周全或更激进地使用工具，请减少这类指引。Claude 4.6 系列模型更主动，早期模型所需的指令在它们身上可能导致触发过度。

7. **原样传回 thinking 块并保持历史只追加：** 每个 assistant 回合都按 API 返回的原样追加，包括 thinking 块。在 Claude 5.1 及之后的模型上，在请求之间编辑较早的消息、重建 `system` 或 `tools`、或就地总结较早的回合，会[使之后的所有 thinking 块失效](https://platform.claude.com/docs/en/build-with-claude/thinking#preserved-in-conversation)。请把这些改动移到对话中段的系统消息和服务端上下文管理中。参见[保持对话历史只追加](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#keep-the-conversation-history-append-only)。

详细的迁移步骤，请参阅[迁移指南](https://platform.claude.com/docs/en/about-claude/models/migration-guide)。

### 迁移到 Claude Sonnet 5.5

请参阅 [Claude Sonnet 5.5 迁移指南](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)。它涵盖面向 Claude Sonnet 5 编写的代码的破坏性变更，以及从 Claude Sonnet 4.6 和更早版本迁移的步骤，包括移除手动扩展思考（`budget_tokens`）。

## 后续步骤

<CardGroup cols={2}>
  <Card title="Claude Fable 5.1 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1">
    Claude Fable 5.1 的行为差异与提示词模式，涵盖 effort、任务收尾、进度更新、thinking 块、工具调用批处理和写作风格。
  </Card>

  <Card title="Claude Fable 5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5">
    Claude Fable 5 和 Claude Mythos 5 的行为差异与提示词模式，涵盖 effort、指令遵循、长时间运行、记忆和脚手架变更。
  </Card>

  <Card title="Claude Sonnet 5.5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5">
    Claude Sonnet 5.5 的行为差异与提示词模式，涵盖 effort 校准、主动性与任务范围、无前置思考运行、推理任务的 JSON 输出、进度更新、工具使用、回合中用户消息、编码验证、工具调用处理、视觉输入和安全保障拒绝。
  </Card>

  <Card title="Claude Sonnet 5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5">
    Claude Sonnet 5 的行为差异与提示词模式，涵盖 effort、自适应思考默认值和工具使用。
  </Card>

  <Card title="Claude Opus 5.5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5">
    Claude Opus 5.5 的行为差异与提示词模式，涵盖 effort 校准、思考始终开启、进度更新、安全保障拒绝和视觉输入。
  </Card>

  <Card title="Claude Opus 5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5">
    Claude Opus 5 的行为差异与提示词模式，涵盖回复详略、智能体叙事、任务范围界定、子智能体委派和自我修正。
  </Card>

  <Card title="Claude Haiku 5.5 提示词指南" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5">
    Claude Haiku 5.5 的行为差异与提示词模式，涵盖 effort、搜索、用你自己的工具输出 JSON、提前停止、编码验证、回合中用户消息、聊天机器人的系统提示词遵循和安全保障拒绝。
  </Card>

  <Card title="提示词工程概览" icon="edit" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview">
    何时使用提示词工程，以及在调优 prompt 之前如何规划你的方法。
  </Card>
</CardGroup>
