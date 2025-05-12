# ANP 网络探索工具 (ANP Network Explorer)

ANP 网络探索工具是一个基于 React 和 Ant Design 的聊天界面应用，旨在成为智能体互联网时代的 HTTP。

## 功能特点

- 聊天界面：支持用户与 AI 助手进行对话
- 酒店查询：可以通过聊天查询酒店信息，并以卡片形式展示
- 响应式设计：适配不同屏幕尺寸
- 骨架屏：优化加载体验

## 安装

### 前置要求

本项目使用 Node.js，建议使用 nvm（Node Version Manager）来管理 Node.js 版本。

- Windows: 下载并安装 [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)
- macOS/Linux: 使用以下命令安装
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
  ```

安装 nvm 后，使用以下命令安装并使用指定版本的 Node.js：

```bash
nvm install 18  # 安装 Node.js 18 版本
nvm use 18      # 使用 Node.js 18 版本
```

### 项目安装

1. 创建并配置 .env 文件：

在项目根目录创建一个 .env 文件，并添加以下内容：

```
AI_API_KEY=your_api_key_here
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=gpt-3.5-turbo
```

请确保将 `your_api_key_here` 替换为您的实际 API 密钥。

2. 安装依赖：

```bash
npm install
```

## 运行

启动开发服务器：

```bash
npm run dev
```

访问 `http://localhost:5173` 查看应用。

## 使用说明

1. 在聊天界面输入消息与 AI 助手交互
2. 输入 "查找酒店" 来获取酒店信息
3. 查看酒店卡片，了解酒店详情
4. 点击 "立即预订" 按钮进行预订操作

## 技术栈

- React
- TypeScript
- Ant Design
- Vite
