# ANP网络探索工具 / ANP Network Explorer

### 项目介绍

ANP网络探索工具是一个基于Agent Network Protocol (ANP)的应用程序，允许用户使用自然语言与智能体网络进行交互。用户可以提供智能体描述URL，通过简单的问题与智能体进行对话，并实时查看网络爬取的过程。
![查询天气案例](images/anp-examples-mainpage.png)

### 项目结构

本项目包含以下主要组件：

- **web_app/**：Web应用程序，包含前端和后端实现
  - **frontend/**：基于HTML/JavaScript的用户界面
  - **backend/**：基于FastAPI的后端服务器
  - **static/**：静态资源文件

- **anp_examples/**：ANP核心功能实现
  - **simple_example.py**：简化的ANP爬取逻辑实现
  - **anp_tool.py**：ANP工具类，用于与智能体网络交互
  - **utils/**：工具类和辅助函数

- **use_did_test_public/**：DID认证相关文件
  - **did.json**：DID文档
  - **key-1_private.pem**：私钥文件
  - **private_keys.json**：密钥配置

- **examples_code/**：示例代码
  - **client.py**：客户端示例
  - **server.py**：服务器示例
  - **did_auth_middleware.py**：DID认证中间件
  - **jwt_config.py**：JWT配置

### 如何运行（面向体验用户）

#### 环境设置

在运行项目之前，你需要设置必要的环境变量。项目中提供了一个 `.env.example` 文件作为模板：

1.  复制 `.env.example` 文件并重命名为 `.env`：
    ```bash
    cp .env.example .env
    ```
2.  编辑 `.env` 文件，填入你的 API-KEY 和 Endpoint 等实际配置信息。


**配置示例：**

```env
# 选择 AI 服务提供商 (必填)
MODEL_PROVIDER=openai  # 可选值: dashscope / openai

# DashScope (阿里云通义千问) 配置
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL_NAME=qwen2.5-14b-instruct

# OpenAI 兼容 API 配置  
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.360.cn/v1
OPENAI_MODEL=gpt-4o
```

**使用说明：**
- 选择 `dashscope` 时，只需配置 DASHSCOPE 相关参数
- 选择 `openai` 时，只需配置 OPENAI 相关参数
- 获取 API Key：[阿里云控制台](https://dashscope.console.aliyun.com/) 或您选择的 AI 服务商


#### 使用Web应用程序

##### 方法一：通过浏览器直接运行
通过访问我们部署在WEB端的应用程序，你可以直接体验ANP网络探索工具的功能。
[访问网址:Https://service.agent-network-protocol.com/anp-demo/](https://service.agent-network-protocol.com/anp-demo/)
![查询天气案例](images/anp-examples-web-search-result.png)

##### 方法二：使用脚本运行
通过以下步骤，你可以在本地运行Web应用程序。

1. 安装依赖：
   ```bash
   # 使用Poetry
   poetry install
   
   # 或使用pip
   pip install -r web_app/backend/requirements.txt
   ```

2. 启动Web应用程序：
   
   ```bash

    # 启动Python虚拟环境
    poetry shell

    # 或手动启动
    source venv/bin/activate  # Linux/Mac
    # 或 venv\Scripts\activate  # Windows

   python web_app/backend/anp_examples_backend.py
   ```

3. 打开浏览器访问：`http://localhost:5005`

4. 在输入框中输入您的问题，并提供智能体URL（可选，默认为`https://agent-search.ai/ad.json`）

5. 点击"提交问题"按钮
![查询天气案例](images/anp-examples-search-agent.png)

1. 查看结果和网络爬取过程
![查询天气案例](images/anp-examples-search-result.png)

##### 方法三: 使用 Docker 运行
> 通过`docker compose`命令运行Docker容器，确保你已经安装了Docker和Docker Compose。
```bash
docker compose up -d
```
然后打开浏览器访问：`http://localhost:5005`

### 如何开发（面向开发者）

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/anp-examples.git
   cd anp-examples
   ```
2. 安装开发依赖：
   ```bash
   poetry install
   
   # 或使用pip
   pip install -r web_app/backend/requirements.txt
   ```

3. 运行测试：
   ```bash
   python web_app/backend/anp_examples_backend.py
   ```

4. 观察日志：
[完整的运行日志](anp-examples.log.md)
