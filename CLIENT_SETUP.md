# FastMCP客户端配置指南

本文档详细介绍如何配置客户端连接到Google Search MCP服务器，包括认证设置和不同环境下的配置方法。

## 目录

1. [快速开始](#快速开始)
2. [认证配置](#认证配置)
3. [配置方法](#配置方法)
4. [使用示例](#使用示例)
5. [故障排除](#故障排除)

## 快速开始

### 基本连接（无认证）

适用于开发环境，服务器未启用认证时：

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
            {"query": "test", "num_results": 3}
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 运行示例

```bash
# 运行客户端示例
python client_example.py
```

## 认证配置

### Bearer Token认证

当服务器启用认证时（`ENABLE_AUTH=true`），客户端需要提供Bearer Token：

#### 方法1：环境变量
```bash
export CLIENT_API_TOKEN="your_api_token_here"
python client_example.py
```

#### 方法2：配置文件
在`client_config.json`中配置：

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

#### 方法3：代码中直接设置
```python
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
```

### 高级认证配置

使用自定义传输层配置：

```python
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(
    url="http://127.0.0.1:9000/mcp/",
    headers={
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "User-Agent": "MyClient/1.0"
    },
    timeout=30.0
)

client = Client({"mcpServers": {"google-search": {}}})
```

## 配置方法

### 1. Python代码配置

#### 基本配置
```python
from fastmcp import Client

config = {
    "mcpServers": {
        "server_name": {
            "url": "http://host:port/mcp/",
            "transport": "streamable-http"
        }
    }
}

client = Client(config)
```

#### 带认证的配置
```python
config = {
    "mcpServers": {
        "server_name": {
            "url": "http://host:port/mcp/",
            "transport": "streamable-http",
            "headers": {
                "Authorization": "Bearer your_token"
            }
        }
    }
}
```

### 2. JSON配置文件

创建`client_config.json`文件：

```json
{
  "mcpServers": {
    "google-search": {
      "url": "http://127.0.0.1:9000/mcp/",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

然后在Python中加载：

```python
import json
from fastmcp import Client

with open('client_config.json', 'r') as f:
    config = json.load(f)

client = Client(config)
```

### 3. 环境变量配置

```bash
# 服务器URL
export SERVER_URL="http://127.0.0.1:9000/mcp/"

# API令牌
export CLIENT_API_TOKEN="your_api_token_here"

# 其他配置
export TIMEOUT="30"
export USER_AGENT="MyClient/1.0"
```

Python代码中读取环境变量：

```python
import os
from fastmcp import Client

server_url = os.getenv('SERVER_URL', 'http://127.0.0.1:9000/mcp/')
api_token = os.getenv('CLIENT_API_TOKEN')

config = {
    "mcpServers": {
        "google-search": {
            "url": server_url,
            "transport": "streamable-http",
            "headers": {
                "Authorization": f"Bearer {api_token}"
            } if api_token else {}
        }
    }
}

client = Client(config)
```

## 使用示例

### 调用Google搜索工具

```python
async with client:
    # 基本搜索
    result = await client.call_tool(
        "search_google", 
        {
            "query": "Python programming",
            "num_results": 5
        }
    )
    
    # 带认证的搜索
    result = await client.call_tool(
        "search_google", 
        {
            "query": "machine learning",
            "num_results": 3,
            "auth_token": api_token  # 传递认证令牌
        }
    )
    
    # 处理结果
    if result.get("success"):
        for item in result["results"]:
            print(f"标题: {item['title']}")
            print(f"链接: {item['link']}")            print(f"摘要: {item['snippet']}")
            print("-" * 50)
    else:
        print(f"搜索失败: {result.get('error')}")
```

### 错误处理

```python
try:
    async with client:
        result = await client.call_tool(
            "search_google", 
            {"query": "test", "num_results": 3}
        )
        
        if result.get("success"):
            print("搜索成功")
        else:
            print(f"搜索失败: {result.get('error')}")
            
except Exception as e:
    print(f"连接错误: {e}")
```

## 故障排除

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

### 配置检查清单

- [ ] 服务器地址和端口正确
- [ ] 传输协议设置为`streamable-http`
- [ ] API令牌正确配置（如需要认证）
- [ ] 请求头格式正确
- [ ] 网络连接正常
- [ ] 服务器正在运行
- [ ] 防火墙设置允许连接

## 最佳实践

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

### 监控和日志
1. **记录请求和响应**
2. **监控错误率**
3. **设置告警机制**
4. **定期检查服务器状态**