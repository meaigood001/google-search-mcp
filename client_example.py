"""
FastMCP客户端连接Google Search MCP服务器的示例

本文件展示了四种连接方式：
1. 无认证连接（开发环境）
2. 带Bearer Token认证连接（生产环境）
3. 自定义认证配置连接
4. 从配置文件加载连接

使用方法：
1. 设置环境变量（可选）:
   export CLIENT_API_TOKEN="your_api_token_here"
   export SERVER_URL="http://127.0.0.1:9000/mcp/"

2. 运行示例:
   python client_example.py

3. 运行特定示例:
   python client_example.py --auth
   python client_example.py --config
"""

import asyncio
import os
import json
import argparse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


def load_env_config():
    """从环境变量加载配置"""
    return {
        "api_token": os.getenv("CLIENT_API_TOKEN"),
        "server_url": os.getenv("SERVER_URL", "http://127.0.0.1:9000/mcp/"),
        "timeout": float(os.getenv("TIMEOUT", "30")),
        "user_agent": os.getenv("USER_AGENT", "FastMCP-Client/1.0")
    }


async def connect_without_auth():
    """
    无认证连接示例（仅用于开发环境）
    """
    print("=== 无认证连接示例 ===")
    
    env_config = load_env_config()
    
    # 服务器配置（无认证）
    config = {
        "mcpServers": {
            "google-search": {
                "url": env_config["server_url"],
                "transport": "streamable-http"
            }
        }
    }
    
    try:
        # 初始化客户端
        client = Client(config)
        
        async with client:
            # 调用Google搜索工具
            result = await client.call_tool(
                "search_google", 
                {
                    "query": "FastMCP tutorial",
                    "num_results": 3
                }
            )
            
            print("搜索结果:")
            if result.get("success"):
                for item in result["results"]:
                    print(f"标题: {item['title']}")
                    print(f"链接: {item['link']}")
                    print(f"摘要: {item['snippet']}")
                    print("-" * 50)
            else:
                print(f"搜索失败: {result.get('error')}")
            
    except Exception as e:
        print(f"连接失败: {e}")


async def connect_with_auth():
    """
    带Bearer Token认证的连接示例（推荐用于生产环境）
    """
    print("\n=== 带Bearer Token认证连接示例 ===")
    
    env_config = load_env_config()
    api_token = env_config["api_token"]
    
    if not api_token:
        print("警告: 请设置CLIENT_API_TOKEN环境变量")
        print("示例: export CLIENT_API_TOKEN='your_api_token_here'")
        return
    
    # 服务器配置（带认证）
    config = {
        "mcpServers": {
            "google-search": {
                "url": env_config["server_url"],
                "transport": "streamable-http",
                "headers": {
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json",
                    "User-Agent": env_config["user_agent"]
                }
            }
        }
    }
    
    try:
        # 初始化客户端
        client = Client(config)
        
        async with client:
            # 调用Google搜索工具（包含认证令牌）
            result = await client.call_tool(
                "search_google", 
                {
                    "query": "Python programming",
                    "num_results": 2,
                    "auth_token": api_token  # 传递认证令牌给工具
                }
            )
            
            print("搜索结果:")
            if result.get("success"):
                for item in result["results"]:
                    print(f"标题: {item['title']}")
                    print(f"链接: {item['link']}")
                    print(f"摘要: {item['snippet']}")
                    print("-" * 50)
            else:
                print(f"搜索失败: {result.get('error')}")
            
    except Exception as e:
        print(f"连接失败: {e}")


async def connect_with_custom_config():
    """
    自定义认证配置连接示例
    """
    print("\n=== 自定义认证配置连接示例 ===")
    
    env_config = load_env_config()
    api_token = env_config["api_token"]
    
    if not api_token:
        print("警告: 请设置CLIENT_API_TOKEN环境变量")
        return
    
    try:
        # 使用自定义认证头
        from fastmcp.client.transports import StreamableHttpTransport
        
        # 使用自定义传输层配置
        transport = StreamableHttpTransport(
            url=env_config["server_url"],
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
                "User-Agent": env_config["user_agent"],
                "X-Client-ID": "example-client",
                "X-Request-ID": "req-12345"
            },
            timeout=env_config["timeout"]
        )
        
        config = {
            "mcpServers": {
                "google-search": {
                    "url": env_config["server_url"],
                    "transport": "streamable-http"
                }
            }
        }
        
        # 初始化客户端
        client = Client(config)
        
        async with client:
            # 调用Google搜索工具
            result = await client.call_tool(
                "search_google", 
                {
                    "query": "artificial intelligence",
                    "num_results": 3,
                    "auth_token": api_token
                }
            )
            
            print("搜索结果:")
            if result.get("success"):
                for item in result["results"]:
                    print(f"标题: {item['title']}")
                    print(f"链接: {item['link']}")
                    print(f"摘要: {item['snippet']}")
                    print("-" * 50)
            else:
                print(f"搜索失败: {result.get('error')}")
            
    except Exception as e:
        print(f"连接失败: {e}")


async def load_config_from_file():
    """从JSON配置文件加载配置"""
    print("\n=== 从配置文件加载连接示例 ===")
    
    config_file = "client_config.json"
    
    if not os.path.exists(config_file):
        print(f"配置文件 {config_file} 不存在")
        print("请确保client_config.json文件存在并包含正确的配置")
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 替换环境变量占位符
        for server_name, server_config in config.get("mcpServers", {}).items():
            if "headers" in server_config:
                for key, value in server_config["headers"].items():
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]
                        env_value = os.getenv(env_var)
                        if env_value:
                            server_config["headers"][key] = env_value
                        else:
                            print(f"警告: 环境变量 {env_var} 未设置，使用默认值")
        
        print(f"加载配置: {config}")
        client = Client(config)
        
        async with client:
            # 调用Google搜索工具
            result = await client.call_tool(
                "search_google", 
                {"query": "data science", "num_results": 3}
            )
            
            print("搜索结果:")
            if result.get("success"):
                for item in result["results"]:
                    print(f"标题: {item['title']}")
                    print(f"链接: {item['link']}")
                    print(f"摘要: {item['snippet']}")
                    print("-" * 50)
            else:
                print(f"搜索失败: {result.get('error')}")
                
    except json.JSONDecodeError as e:
        print(f"配置文件JSON格式错误: {e}")
    except Exception as e:
        print(f"配置文件错误: {e}")


async def test_connection():
    """测试连接到服务器"""
    print("\n=== 测试服务器连接 ===")
    
    env_config = load_env_config()
    
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(env_config["server_url"]) as response:
                if response.status == 200:
                    print(f"✓ 服务器连接成功: {env_config['server_url']}")
                else:
                    print(f"✗ 服务器连接失败: HTTP {response.status}")
    except ImportError:
        print("警告: 需要安装aiohttp来测试连接")
    except Exception as e:
        print(f"✗ 连接测试失败: {e}")


async def main():
    """主函数 - 运行连接示例"""
    parser = argparse.ArgumentParser(description="FastMCP客户端连接示例")
    parser.add_argument("--auth", action="store_true", help="仅运行认证连接示例")
    parser.add_argument("--config", action="store_true", help="仅运行配置文件连接示例")
    parser.add_argument("--test", action="store_true", help="仅测试服务器连接")
    parser.add_argument("--no-auth", action="store_true", help="仅运行无认证连接示例")
    
    args = parser.parse_args()
    
    print("FastMCP客户端连接Google Search MCP服务器示例")
    print("=" * 60)
    
    # 显示当前环境配置
    env_config = load_env_config()
    print(f"服务器URL: {env_config['server_url']}")
    print(f"API令牌: {'已设置' if env_config['api_token'] else '未设置'}")
    print(f"超时时间: {env_config['timeout']}秒")
    print("-" * 60)
    
    if args.test:
        await test_connection()
        return
    
    if args.no_auth:
        await connect_without_auth()
        return
    
    if args.auth:
        await connect_with_auth()
        return
    
    if args.config:
        await load_config_from_file()
        return
    
    # 运行所有示例
    await test_connection()
    await connect_without_auth()
    await connect_with_auth()
    await connect_with_custom_config()
    await load_config_from_file()


if __name__ == "__main__":
    asyncio.run(main())