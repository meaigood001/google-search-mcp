# Google Search MCP Server

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/google-search-mcp)

一个基于FastMCP框架的Google搜索服务器，提供Google自定义搜索功能。支持Streamable HTTP传输协议，具备企业级安全认证机制。

## ✨ 主要特性

- 🔍 **Google搜索集成**: 使用Google Custom Search API提供强大的搜索功能
- 🚀 **Streamable HTTP**: 支持实时通信的高性能HTTP传输协议
- 🔐 **企业级安全**: 内置Bearer Token认证机制，支持生产环境安全部署
- ⚙️ **灵活配置**: 通过环境变量轻松配置服务器参数
- 📦 **现代化依赖管理**: 支持UV和pip两种依赖管理方式
- 🛠️ **开发友好**: 完整的开发工具链，包括测试、格式化、类型检查
- 📚 **完整文档**: 详细的服务器和客户端配置指南

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Google API Key
- Google Custom Search Engine ID

### 安装

#### 使用UV（推荐）

```bash
# 安装UV
powershell -c "irm https://astral.sh/uv/install.sh | iex"

# 克隆项目
git clone https://github.com/yourusername/google-search-mcp.git
cd google-search-mcp

# 创建虚拟环境
uv venv
.venv\Scripts\activate

# 安装依赖
uv pip install -e .
```

#### 使用pip

```bash
# 克隆项目
git clone https://github.com/yourusername/google-search-mcp.git
cd google-search-mcp

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 配置

1. 复制环境变量模板文件：

```bash
copy .env.example .env
```

2. 编辑`.env`文件，配置必要的环境变量：

```env
# Google API配置
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_custom_search_engine_id_here

# 服务器配置
HTTP_HOST=127.0.0.1
HTTP_PORT=9000

# 认证配置（生产环境建议启用）
ENABLE_AUTH=true
API_TOKEN=your_secure_api_token_here
```

### 运行服务器

```bash
# 启动服务器
python main.py
```

服务器将在 `http://127.0.0.1:9000/mcp/` 启动。

## 🔧 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `GOOGLE_API_KEY` | Google API密钥 | - | ✅ |
| `GOOGLE_CSE_ID` | Google自定义搜索引擎ID | - | ✅ |
| `HTTP_HOST` | 服务器主机地址 | `127.0.0.1` | ❌ |
| `HTTP_PORT` | 服务器端口 | `9000` | ❌ |
| `ENABLE_AUTH` | 是否启用认证 | `false` | ❌ |
| `API_TOKEN` | API认证令牌 | - | 认证启用时必需 |

### 认证配置

#### 开发环境（无认证）

```env
ENABLE_AUTH=false
```

#### 生产环境（启用认证）

```env
ENABLE_AUTH=true
API_TOKEN=your_secure_api_token_here
```

## 📖 使用方法

### 服务器API

服务器提供一个搜索工具：

#### `search_google`

执行Google搜索并返回格式化结果。

**参数：**
- `query` (str): 搜索查询字符串
- `num_results` (int, 可选): 返回结果数量，默认为5
- `auth_token` (str, 可选): 认证令牌（启用认证时必需）

**返回值：**
```json
{
  "success": true,
  "results": [
    {
      "title": "结果标题",
      "link": "结果链接",
      "snippet": "结果摘要"
    }
  ],
  "total_results": "1000000"
}
```

### 客户端连接

#### 基本连接（无认证）

```python
import asyncio
from fastmcp import Client

async def main():
    config = {
        "mcpServers": {
            "google-search": {
                "url": "http://127.0.0.1:9000/mcp/",
                "transport": "streamable-http"
            }
        }
    }
    
    client = Client(config)
    
    async with client:
        result = await client.call_tool(
            "search_google", 
            {"query": "Python编程", "num_results": 3}
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### 带认证的连接

```python
import asyncio
from fastmcp import Client

async def main():
    config = {
        "mcpServers": {
            "google-search": {
                "url": "http://127.0.0.1:9000/mcp/",
                "transport": "streamable-http",
                "headers": {
                    "Authorization": "Bearer your_api_token_here"
                }
            }
        }
    }
    
    client = Client(config)
    
    async with client:
        result = await client.call_tool(
            "search_google", 
            {"query": "人工智能", "num_results": 5}
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 运行示例

项目提供了完整的客户端示例：

```bash
# 运行客户端示例
python client_example.py

# 使用命令行工具
python run_client.py --help
```

## 🛠️ 开发

### 安装开发依赖

```bash
# 使用UV
uv pip install -e ".[dev]"

# 使用pip
pip install -e ".[dev]"
```

### 代码格式化

```bash
# 格式化代码
uv run black .
uv run isort .
```

### 类型检查

```bash
# 运行类型检查
uv run mypy .
```

### 测试

```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=google_search_mcp
```

### 代码检查

```bash
# 运行代码检查
uv run flake8 .
```

## 📁 项目结构

```
google-search-mcp/
├── main.py                 # 主服务器文件
├── client_example.py      # 客户端示例
├── run_client.py         # 命令行客户端工具
├── client_config.json    # 客户端配置文件
├── pyproject.toml        # 项目配置文件
├── requirements.txt      # pip依赖文件
├── uv.lock              # UV锁定文件
├── .env.example         # 环境变量模板
├── .env                 # 环境变量文件（git忽略）
├── README.md           # 项目说明文档
├── README_CLIENT.md    # 客户端配置指南
├── CLIENT_SETUP.md     # 客户端设置详细文档
└── UV_USAGE.md         # UV使用指南
```

## 🔍 详细文档

- [客户端配置指南](README_CLIENT.md) - 详细的客户端连接和配置说明
- [客户端设置文档](CLIENT_SETUP.md) - 完整的客户端配置方法和最佳实践
- [UV使用指南](UV_USAGE.md) - UV依赖管理工具的使用说明

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastMCP](https://github.com/modelcontextprotocol/fastmcp) - 提供MCP服务器框架
- [Google Custom Search API](https://developers.google.com/custom-search) - 提供搜索功能
- [UV](https://github.com/astral-sh/uv) - 现代化的Python包管理器

## 📞 支持

如果您遇到问题或有建议，请：

- 创建 [Issue](https://github.com/yourusername/google-search-mcp/issues)
- 查看 [文档](https://github.com/yourusername/google-search-mcp#readme)
- 联系维护者

---

**注意**: 使用本服务器需要有效的Google API密钥和Custom Search Engine ID。请确保遵守Google API的使用条款和服务限制。