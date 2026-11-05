---
title: 提示词工程概览
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
description: 了解何时适合使用提示词工程来解决问题，并找到 Claude 提示词技术与交互式教程。
---

## 在开始提示词工程之前

本指南假设你已经具备：

1. 对你的用例成功标准的清晰定义
2. 若干能够依据这些标准进行实证测试的方法
3. 一个你想要改进的提示词初稿

如果还不具备，请先花时间把这些建立起来。可参阅[定义成功标准并构建评测](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)获取提示与指导。

<CardGroup cols={2}>
  <Card title="提示词生成器 notebook" icon="link" href="https://colab.research.google.com/github/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb">
    还没有提示词初稿？用 Claude Cookbook 中的 metaprompt 配方生成一个。
  </Card>

  <Card title="提示词最佳实践" icon="link" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    针对 Claude 最新模型的模型级调优指引，从这里开始。
  </Card>
</CardGroup>

***

## 何时适合做提示词工程

本指南关注那些可以通过提示词工程来控制的成功标准。并非所有成功标准或失败的评测都最适合用提示词工程来解决。例如，有时候换一个模型能更轻松地改善延迟和成本。

***

## 如何做提示词工程

所有提示词技术（从清晰性与示例，到 XML 结构化、角色提示、思考与提示词链）都在[提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)中讲解。那是持续更新的参考文档；请从那里开始。

关于超越 Claude 专属技术的通用提示词工程方法论，请参阅博客文章[提示词工程的最佳实践](https://claude.com/blog/best-practices-for-prompt-engineering)。

***

## 提示词工程教程

如果你偏好交互式学习，也可以从交互式教程开始！

<CardGroup cols={2}>
  <Card title="GitHub 提示词教程" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    一个示例丰富的提示词工程基础教程。它为 Claude 3 系列模型而写，因此当两者有出入时，请以提示词最佳实践为准。
  </Card>

  <Card title="Google Sheets 提示词教程" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    提示词工程教程的轻量版，以交互式电子表格的形式呈现。
  </Card>
</CardGroup>
