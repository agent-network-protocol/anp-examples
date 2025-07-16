# UV Usage Guide for ANP Examples

这个项目现在使用 UV 进行 Python 包管理和虚拟环境管理。

## 基本命令

### 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 退出虚拟环境
deactivate
```

### 包管理

```bash
# 安装项目依赖（从 pyproject.toml）
uv pip install -e .

# 安装单个包
uv pip install requests

# 安装开发依赖
uv pip install pytest

# 安装指定版本的包
uv pip install "fastapi>=0.100.0"

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 列出已安装的包
uv pip list

# 生成 requirements.txt
uv pip freeze > requirements.txt

# 卸载包
uv pip uninstall package_name
```

### 运行命令

```bash
# 直接在虚拟环境中运行 Python 脚本
uv run python script.py

# 运行 uvicorn 服务器
uv run uvicorn main:app --reload

# 运行测试
uv run pytest
```

### 项目管理

```bash
# 同步依赖（安装 pyproject.toml 中的所有依赖）
uv pip sync requirements.txt

# 升级包
uv pip install --upgrade package_name

# 升级所有包
uv pip install --upgrade-all
```

## 配置文件

### pyproject.toml
项目使用标准的 `pyproject.toml` 格式，包含：
- `[project]` 部分：定义项目元数据和依赖
- `[tool.uv]` 部分：UV 特定配置
- 保留的 `[tool.poetry]` 部分：向后兼容性

### requirements.txt
生成的固定版本依赖文件，用于部署和精确复现环境。

## 常用工作流

### 开发环境设置
```bash
# 1. 克隆项目
git clone <repository>
cd anp-examples

# 2. 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate
uv pip install -e .

# 3. 安装开发依赖
uv pip install pytest
```

### 添加新依赖
```bash
# 1. 安装包
uv pip install new_package

# 2. 更新 pyproject.toml 的 dependencies 列表
# 编辑 pyproject.toml，将 new_package 添加到 dependencies 中

# 3. 更新 requirements.txt
uv pip freeze > requirements.txt
```

### 生产环境部署
```bash
# 使用 requirements.txt 确保精确的版本匹配
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## UV 的优势

1. **速度快**：比 pip 快 10-100 倍
2. **跨平台**：原生支持 Windows、macOS、Linux
3. **兼容性好**：完全兼容 pip 和 PyPI
4. **内存效率**：使用 Rust 编写，内存占用少
5. **简单易用**：与现有工具链无缝集成

## 迁移说明

项目原来使用 Poetry，现在可以同时支持 Poetry 和 UV：
- Poetry 用户可以继续使用 `poetry install` 和 `poetry run`
- UV 用户可以使用 `uv pip install -e .` 和 `uv run`
- pyproject.toml 同时包含两种配置格式以确保兼容性 