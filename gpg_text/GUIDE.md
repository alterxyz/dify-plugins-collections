## 如何开发 Dify 插件的用户指南

你好，看起来你已经创建了一个插件，现在让我们开始开发吧！

### 选择你想开发的插件类型

在开始之前，你需要了解一些关于插件类型的基本知识，插件支持在 Dify 中扩展以下能力：
- **工具（Tool）**：像 Google 搜索、Stable Diffusion 等工具提供商，它可以用来执行特定的任务。
- **模型（Model）**：像 OpenAI、Anthropic 等模型提供商，你可以使用它们的模型来增强 AI 能力。
- **端点（Endpoint）**：类似于 Dify 中的 Service API 和 Kubernetes 中的 Ingress，你可以将一个 http 服务扩展为一个端点，并使用你自己的代码来控制其逻辑。

根据你想要扩展的能力，我们将插件分为三种类型：**工具（Tool）**、**模型（Model）** 和 **扩展（Extension）**。

- **工具（Tool）**：它是一个工具提供商，但不仅限于工具，你也可以在那里实现一个端点。例如，如果你正在构建一个 Discord 机器人，你需要同时具备 `发送消息` 和 `接收消息` 的能力，那么 **工具（Tool）** 和 **端点（Endpoint）** 都是必需的。
- **模型（Model）**：只是一个模型提供商，不允许扩展其他能力。
- **扩展（Extension）**：其他时候，你可能只需要一个简单的 http 服务来扩展功能，**扩展（Extension）** 是正确的选择。

我相信你在创建插件时已经选择了正确的类型，如果没有，你可以稍后通过修改 `manifest.yaml` 文件来更改它。

### 清单（Manifest）

现在你可以编辑 `manifest.yaml` 文件来描述你的插件，以下是它的基本结构：

- version(版本, 必需)：插件的版本
- type(类型, 必需)：插件的类型，目前仅支持 `plugin`，未来支持 `bundle`
- author(字符串, 必需)：作者，这是市场中的组织名称，也应等于仓库的所有者
- label(标签, 必需)：多语言名称
- created_at(RFC3339, 必需)：创建时间，市场要求创建时间必须早于当前时间
- icon(资源, 必需)：图标路径
- resource (对象)：要应用的资源
  - memory (int64)：最大内存使用量，主要与 SaaS 上 serverless 的资源申请相关，单位字节
  - permission(对象)：权限申请
    - tool(对象)：反向调用工具权限
      - enabled (bool)
    - model(对象)：反向调用模型权限
      - enabled(bool)
      - llm(bool)
      - text_embedding(bool)
      - rerank(bool)
      - tts(bool)
      - speech2text(bool)
      - moderation(bool)
    - node(对象)：反向调用节点权限
      - enabled(bool)
    - endpoint(对象)：允许注册端点权限
      - enabled(bool)
    - app(对象)：反向调用应用权限
      - enabled(bool)
    - storage(对象)：申请持久化存储权限
      - enabled(bool)
      - size(int64)：允许的最大持久化内存，单位字节
- plugins(对象, 必需)：插件扩展特定能力的 yaml 文件列表，插件包中的绝对路径。如果你需要扩展模型，你需要定义一个类似 openai.yaml 的文件，并在此处填写路径，且路径上的文件必须存在，否则打包会失败。
  - 格式
    - tools(list[string])：扩展的工具供应商，详细格式请参考 [工具指南](https://docs.dify.ai/plugins/schema-definition/tool)
    - models(list[string])：扩展的模型供应商，详细格式请参考 [模型指南](https://docs.dify.ai/plugins/schema-definition/model)
    - endpoints(list[string])：扩展的端点供应商，详细格式请参考 [端点指南](https://docs.dify.ai/plugins/schema-definition/endpoint)
  - 限制
    - 不允许同时扩展工具和模型
    - 不允许没有任何扩展
    - 不允许同时扩展模型和端点
    - 目前每种类型的扩展最多只支持一个供应商
- meta(对象)
  - version(版本, 必需)：manifest 格式版本，初始版本 0.0.1
  - arch(list[string], 必需)：支持的架构，目前仅支持 amd64 arm64
  - runner(对象, 必需)：运行时配置
    - language(string)：目前仅支持 python
    - version(string)：语言版本，目前仅支持 3.12
    - entrypoint(string)：程序入口，在 python 中应为 main

### 安装依赖

- 首先，你需要一个 Python 3.11+ 的环境，因为我们的 SDK 需要它。
- 然后，安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
- 如果你想添加更多依赖，可以将它们添加到 `requirements.txt` 文件中。一旦你在 `manifest.yaml` 文件中将 runner 设置为 python，`requirements.txt` 将被自动生成并用于打包和部署。

### 实现插件

现在你可以开始实现你的插件了，通过以下示例，你可以快速了解如何实现自己的插件：

- [OpenAI](https://github.com/langgenius/dify-plugin-sdks/tree/main/python/examples/openai)：模型提供商的最佳实践
- [Google Search](https://github.com/langgenius/dify-plugin-sdks/tree/main/python/examples/google)：工具提供商的简单示例
- [Neko](https://github.com/langgenius/dify-plugin-sdks/tree/main/python/examples/neko)：端点组的有趣示例

### 测试和调试插件

你可能已经注意到插件根目录下有一个 `.env.example` 文件，只需将其复制为 `.env` 并填写相应的值。如果你想在本地调试插件，需要设置一些环境变量。

- `INSTALL_METHOD`: 设置为 `remote`，你的插件将通过网络连接到 Dify 实例。
- `REMOTE_INSTALL_HOST`: 你的 Dify 实例的主机地址，你可以使用我们的 SaaS 实例 `https://debug.dify.ai`，或者自托管的 Dify 实例。
- `REMOTE_INSTALL_PORT`: 你的 Dify 实例的端口，默认为 5003
- `REMOTE_INSTALL_KEY`: 你应该从你使用的 Dify 实例获取调试密钥。在插件管理页面的右上角，你可以看到一个带有 `debug` 图标的按钮，点击它即可获取密钥。

运行以下命令来启动你的插件：

```bash
python -m main
```

刷新你的 Dify 实例页面，你应该能在列表中看到你的插件了，但它会被标记为 `debugging`。你可以正常使用它，但不建议用于生产环境。

### 打包插件

最后，通过运行以下命令来打包你的插件：

```bash
dify-plugin plugin package ./你的插件根目录
```

你会得到一个 `plugin.difypkg` 文件，这就是全部了。你现在可以将它提交到市场，期待你的插件被列出！


## 用户隐私政策

如果你想将插件发布到市场，请填写插件的隐私政策，更多详情请参考 [PRIVACY.md](PRIVACY.md)。