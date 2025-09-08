# Google Search MCP 客户端配置指南

本指南详细介绍如何配置客户端连接到Google Search MCP服务器，包括认证设置和不同环境下的配置方法。

## 📁 文件结构

```
google-search-mcp/
├── main.py                    # MCP服务器主程序
├── client_example.py          # 客户端连接示例
├── run_client.py              # 客户端快速启动脚本
├── client_config.json         # JSON配置文件示例
├── .env.example              # 环境变量配置示例
├── CLIENT_SETUP.md           # 详细客户端配置文档
└── README_CLIENT.md          # 本文件
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 复制环境变量配置文件
copy .env.example .env

# 编辑.env文件，设置必要的环境变量
# 至少需要设置GOOGLE_API_KEY和GOOGLE_CSE_ID
```

### 2. 启动服务器

```bash
# 启动MCP服务器
python main.py
```

服务器将启动在 `http://127.0.0.1:9000/mcp/`

### 3. 配置客户端

#### 方法一：使用环境变量（推荐）

```bash
# Windows
set CLIENT_API_TOKEN=your_api_token_here
set SERVER_URL=http://127.0.0.1:9000/mcp/

# Linux/Mac
export CLIENT_API_TOKEN="your_api_token_here"
export SERVER_URL="http://127.0.0.1:9000/mcp/"
```

#### 方法二：使用JSON配置文件

编辑 `client_config.json`：

```json
{
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
```

### 4. 运行客户端

```bash
# 运行快速启动脚本（推荐）
python run_client.py

# 或运行完整示例
python client_example.py

# 执行快速搜索
python run_client.py --search "Python programming"

# 进入交互模式
python run_client.py --interactive
```

## 🔐 认证配置

### 启用服务器认证

在服务器的 `.env` 文件中设置：

```env
ENABLE_AUTH=true
API_TOKEN=your_secure_api_token_here
```

### 客户端认证配置

#### Bearer Token认证

```python
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
```

#### 环境变量认证

```python
import os

api_token = os.getenv("CLIENT_API_TOKEN")

config = {
    "mcpServers": {
        "google-search": {
            "url": "http://127.0.0.1:9000/mcp/",
            "transport": "streamable-http",
            "headers": {
                "Authorization": f"Bearer {api_token}"
            } if api_token else {}
        }
    }
}
```

## 📋 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `CLIENT_API_TOKEN` | 客户端API令牌 | - | 认证时必需 |
| `SERVER_URL` | 服务器URL | `http://127.0.0.1:9000/mcp/` | 可选 |
| `TIMEOUT` | 请求超时时间（秒） | `30` | 可选 |
| `USER_AGENT` | 用户代理字符串 | `FastMCP-Client/1.0` | 可选 |

### JSON配置文件

```json
{
  "mcpServers": {
    "server_name": {
      "url": "http://host:port/mcp/",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer token",
        "Content-Type": "application/json",
        "User-Agent": "Custom-Client/1.0"
      },
      "timeout": 30
    }
  }
}
```

## 🛠️ 使用示例

### 基本搜索

```python
import asyncio
from fastmcp import Client

async def search_example():
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
            {"query": "Python programming", "num_results": 5}
        )
        
        if result.get("success"):
            for item in result["results"]:
                print(f"标题: {item['title']}")
                print(f"链接: {item['link']}")
                print(f"摘要: {item['snippet']}")
        else:
            print(f"搜索失败: {result.get('error')}")

asyncio.run(search_example())
```

### 带认证的搜索

```python
async def authenticated_search():
    api_token = "your_api_token_here"
    
    config = {
        "mcpServers": {
            "google-search": {
                "url": "http://127.0.0.1:9000/mcp/",
                "transport": "streamable-http",
                "headers": {
                    "Authorization": f"Bearer {api_token}"
                }
            }
        }
    }
    
    client = Client(config)
    
    async with client:
        result = await client.call_tool(
            "search_google", 
            {
                "query": "machine learning", 
                "num_results": 3,
                "auth_token": api_token
            }
        )
        
        # 处理结果...
```

### 自定义传输层配置

```python
from fastmcp.client.transports import StreamableHttpTransport

async def custom_transport_example():
    transport = StreamableHttpTransport(
        url="http://127.0.0.1:9000/mcp/",
        headers={
            "Authorization": "Bearer your_token",
            "Content-Type": "application/json",
            "User-Agent": "MyClient/1.0"
        },
        timeout=30.0
    )
    
    config = {
        "mcpServers": {
            "google-search": {
                "url": "http://127.0.0.1:9000/mcp/",
                "transport": "streamable-http"
            }
        }
    }
    
    client = Client(config)
    # 使用客户端...
```

## 📝 命令行工具

### run_client.py 使用方法

```bash
# 测试服务器连接
python run_client.py --test

# 仅运行无认证示例
python run_client.py --no-auth

# 仅运行认证示例
python run_client.py --auth

# 仅运行配置文件示例
python run_client.py --config

# 执行快速搜索
python run_client.py --search "Python programming"

# 指定搜索结果数量
python run_client.py --search "AI" --num-results 10

# 进入交互模式
python run_client.py --interactive
# 或
python run_client.py -i
```

### client_example.py 使用方法

```bash
# 运行所有示例
python client_example.py

# 仅运行认证示例
python client_example.py --auth

# 仅运行配置文件示例
python client_example.py --config

# 仅运行无认证示例
python client_example.py --no-auth

# 仅测试连接
python client_example.py --test
```

## 🔧 故障排除

### 常见错误

#### 1. 认证失败
```
错误: Authentication failed: Invalid or missing API token
```

**解决方案：**
- 确保服务器已启用认证（`ENABLE_AUTH=true`）
- 检查API令牌是否正确
- 确保在请求头中正确设置了`Authorization: Bearer token`

#### 2. 连接被拒绝
```
错误: Connection refused
```

**解决方案：**
- 确保服务器正在运行
- 检查URL和端口是否正确
- 确认网络连接正常

#### 3. 超时错误
```
错误: Request timeout
```

**解决方案：**
- 增加超时时间设置
- 检查网络延迟
- 优化服务器响应时间

### 调试技巧

#### 1. 启用详细日志
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 2. 检查服务器状态
```bash
# 检查服务器是否运行
curl http://127.0.0.1:9000/mcp/
```

#### 3. 测试认证
```bash
# 测试带认证的请求
curl -H "Authorization: Bearer your_token" \
     http://127.0.0.1:9000/mcp/
```

## 🏆 最佳实践

### 安全性
1. **生产环境务必启用认证**
2. **使用HTTPS协议**
3. **定期轮换API令牌**
4. **不要在代码中硬编码敏感信息**
5. **使用环境变量或配置文件管理密钥**

### 性能优化
1. **设置合理的超时时间**
2. **重用客户端连接**
3. **批量处理请求**
4. **缓存常用查询结果**

### 开发建议
1. **开发环境使用无认证连接**
2. **生产环境使用认证连接**
3. **使用配置文件管理不同环境的配置**
4. **实现适当的错误处理和重试机制**

## 📚 相关文档

- [详细客户端配置文档](CLIENT_SETUP.md)
- [服务器配置文档](.env.example)
- [FastMCP官方文档](https://fastmcp.dev/)

## 🤝 贡献

如果您发现任何问题或有改进建议，请提交Issue或Pull Request。

## 📄 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。