# UV 依赖管理指南

本文档介绍如何使用 UV 来管理 Google Search MCP 项目的依赖。

## 📋 文件说明

### pyproject.toml
项目的主要配置文件，包含：
- 项目元数据（名称、版本、描述等）
- 核心依赖
- 可选依赖（开发、客户端等）
- 工具配置（black、isort、mypy、pytest等）

### uv.lock
UV 的锁定文件，包含：
- 确切的依赖版本
- 依赖关系图
- 哈希值验证

### requirements.txt
传统 pip 兼容的依赖文件，作为备选方案。

## 🚀 快速开始

### 1. 安装 UV

```bash
# 在 Windows 上
powershell -c "irm https://astral.sh/uv/install.sh | iex"

# 在 Linux/Mac 上
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装核心依赖
uv pip install -e .

# 安装开发依赖
uv pip install -e ".[dev]"

# 安装所有依赖（包括客户端工具）
uv pip install -e ".[all]"
```

## 📦 依赖组说明

### 核心依赖
```bash
uv pip install -e .
```
包含：
- `mcp` - MCP 框架
- `fastmcp` - FastMCP 客户端
- `google-api-python-client` - Google API 客户端
- `python-dotenv` - 环境变量管理

### 开发依赖
```bash
uv pip install -e ".[dev]"
```
包含核心依赖 +：
- `pytest` - 测试框架
- `pytest-asyncio` - 异步测试支持
- `black` - 代码格式化
- `isort` - 导入排序
- `flake8` - 代码检查
- `mypy` - 类型检查

### 客户端依赖
```bash
uv pip install -e ".[client]"
```
包含核心依赖 +：
- `aiohttp` - 异步 HTTP 客户端

### 所有依赖
```bash
uv pip install -e ".[all]"
```
包含所有上述依赖。

## 🛠️ 常用命令

### 依赖管理
```bash
# 添加新依赖
uv add <package-name>

# 添加开发依赖
uv add --group dev <package-name>

# 移除依赖
uv remove <package-name>

# 更新依赖
uv sync

# 更新特定包
uv sync --upgrade <package-name>
```

### 虚拟环境管理
```bash
# 创建虚拟环境
uv venv

# 删除虚拟环境
uv venv --remove

# 显示虚拟环境信息
uv venv --show-path
```

### 运行脚本
```bash
# 运行主程序
uv run python main.py

# 运行客户端示例
uv run python client_example.py

# 运行快速启动脚本
uv run python run_client.py

# 运行测试
uv run pytest

# 代码格式化
uv run black .

# 导入排序
uv run isort .

# 类型检查
uv run mypy .

# 代码检查
uv run flake8 .
```

## 🔄 从 requirements.txt 迁移

如果你有现有的 requirements.txt 文件，可以将其转换为 UV 格式：

```bash
# 从 requirements.txt 安装依赖
uv pip install -r requirements.txt

# 生成 pyproject.toml
uv init
```

## 📊 依赖分析

```bash
# 显示依赖树
uv pip tree

# 检查过时的包
uv pip outdated

# 检查安全漏洞
uv pip audit

# 显示依赖信息
uv pip show <package-name>
```

## 🎯 开发工作流

### 1. 设置开发环境
```bash
# 克隆项目
git clone <repository-url>
cd google-search-mcp

# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 安装所有依赖
uv pip install -e ".[all]"
```

### 2. 日常开发
```bash
# 运行服务器
uv run python main.py

# 运行客户端测试
uv run python run_client.py --test

# 运行测试
uv run pytest

# 代码格式化
uv run black .
uv run isort .

# 类型检查
uv run mypy .

# 代码检查
uv run flake8 .
```

### 3. 添加新依赖
```bash
# 添加核心依赖
uv add <package-name>

# 添加开发依赖
uv add --group dev <package-name>

# 更新锁定文件
uv sync
```

## 🐛 故障排除

### 常见问题

#### 1. UV 未找到命令
```bash
# 确保 UV 已正确安装
uv --version

# 如果未安装，重新安装
# Windows
powershell -c "irm https://astral.sh/uv/install.sh | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. 虚拟环境激活失败
```bash
# 重新创建虚拟环境
uv venv --force

# 手动激活
# Windows
.venv\Scripts\activate.ps1

# Linux/Mac
source .venv/bin/activate
```

#### 3. 依赖安装失败
```bash
# 清理缓存
uv cache clean

# 重新安装
uv sync --reinstall

# 检查 Python 版本
python --version
uv python list
```

#### 4. 锁定文件冲突
```bash
# 重新生成锁定文件
uv lock

# 强制同步
uv sync --force
```

### 调试命令
```bash
# 显示详细输出
uv sync --verbose

# 显示调试信息
uv sync --debug

# 检查环境
uv pip list
uv pip freeze
```

## 📚 相关资源

- [UV 官方文档](https://docs.astral.sh/uv/)
- [UV GitHub 仓库](https://github.com/astral-sh/uv)
- [Python 打包指南](https://packaging.python.org/)
- [pyproject.toml 规范](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)

## 🤝 贡献

如果你发现任何问题或有改进建议，请提交 Issue 或 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。