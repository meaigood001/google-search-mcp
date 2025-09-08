#!/usr/bin/env python3
"""
FastMCP客户端快速启动脚本

使用方法:
1. 设置环境变量:
   set CLIENT_API_TOKEN=your_api_token_here
   set SERVER_URL=http://127.0.0.1:9000/mcp/

2. 运行脚本:
   python run_client.py

3. 运行特定模式:
   python run_client.py --test    # 仅测试连接
   python run_client.py --auth    # 仅运行认证示例
   python run_client.py --search "query"  # 执行搜索
"""

import asyncio
import os
import sys
import argparse
from client_example import (
    load_env_config,
    connect_without_auth,
    connect_with_auth,
    connect_with_custom_config,
    load_config_from_file,
    test_connection
)
from fastmcp import Client


async def quick_search(query: str, num_results: int = 5):
    """快速搜索功能"""
    print(f"=== 快速搜索: {query} ===")
    
    env_config = load_env_config()
    
    # 根据是否有API令牌选择连接方式
    if env_config["api_token"]:
        config = {
            "mcpServers": {
                "google-search": {
                    "url": env_config["server_url"],
                    "transport": "streamable-http",
                    "headers": {
                        "Authorization": f"Bearer {env_config['api_token']}",
                        "Content-Type": "application/json"
                    }
                }
            }
        }
    else:
        config = {
            "mcpServers": {
                "google-search": {
                    "url": env_config["server_url"],
                    "transport": "streamable-http"
                }
            }
        }
    
    client = Client(config)
    
    try:
        async with client:
            result = await client.call_tool(
                "search_google", 
                {
                    "query": query, 
                    "num_results": num_results,
                    "auth_token": env_config["api_token"]
                }
            )
            
            print("搜索结果:")
            if result.get("success"):
                for i, item in enumerate(result["results"], 1):
                    print(f"{i}. {item['title']}")
                    print(f"   链接: {item['link']}")
                    print(f"   摘要: {item['snippet']}")
                    print()
            else:
                print(f"搜索失败: {result.get('error')}")
                
    except Exception as e:
        print(f"搜索错误: {e}")


async def interactive_mode():
    """交互式模式"""
    print("=== 交互式搜索模式 ===")
    print("输入搜索查询，输入 'quit' 或 'exit' 退出")
    print()
    
    env_config = load_env_config()
    
    # 根据是否有API令牌选择连接方式
    if env_config["api_token"]:
        config = {
            "mcpServers": {
                "google-search": {
                    "url": env_config["server_url"],
                    "transport": "streamable-http",
                    "headers": {
                        "Authorization": f"Bearer {env_config['api_token']}",
                        "Content-Type": "application/json"
                    }
                }
            }
        }
    else:
        config = {
            "mcpServers": {
                "google-search": {
                    "url": env_config["server_url"],
                    "transport": "streamable-http"
                }
            }
        }
    
    client = Client(config)
    
    try:
        async with client:
            while True:
                query = input("搜索查询 > ").strip()
                
                if query.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                
                if not query:
                    continue
                
                try:
                    result = await client.call_tool(
                        "search_google", 
                        {
                            "query": query, 
                            "num_results": 5,
                            "auth_token": env_config["api_token"]
                        }
                    )
                    
                    print("\n搜索结果:")
                    if result.get("success"):
                        for i, item in enumerate(result["results"], 1):
                            print(f"{i}. {item['title']}")
                            print(f"   链接: {item['link']}")
                            print(f"   摘要: {item['snippet']}")
                            print()
                    else:
                        print(f"搜索失败: {result.get('error')}")
                        
                except Exception as e:
                    print(f"搜索错误: {e}")
                
                print()
                
    except KeyboardInterrupt:
        print("\n\n再见！")
    except Exception as e:
        print(f"连接错误: {e}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="FastMCP客户端快速启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run_client.py                    # 运行所有示例
  python run_client.py --test              # 仅测试连接
  python run_client.py --auth              # 仅运行认证示例
  python run_client.py --search "Python"   # 执行快速搜索
  python run_client.py --interactive       # 进入交互模式
        """
    )
    
    parser.add_argument("--test", action="store_true", help="仅测试服务器连接")
    parser.add_argument("--auth", action="store_true", help="仅运行认证连接示例")
    parser.add_argument("--no-auth", action="store_true", help="仅运行无认证连接示例")
    parser.add_argument("--config", action="store_true", help="仅运行配置文件连接示例")
    parser.add_argument("--search", type=str, help="执行快速搜索")
    parser.add_argument("--interactive", "-i", action="store_true", help="进入交互式搜索模式")
    parser.add_argument("--num-results", type=int, default=5, help="搜索结果数量 (默认: 5)")
    
    args = parser.parse_args()
    
    print("FastMCP客户端快速启动")
    print("=" * 40)
    
    # 显示当前环境配置
    env_config = load_env_config()
    print(f"服务器URL: {env_config['server_url']}")
    print(f"API令牌: {'已设置' if env_config['api_token'] else '未设置'}")
    print(f"超时时间: {env_config['timeout']}秒")
    print("-" * 40)
    
    if args.interactive:
        await interactive_mode()
        return
    
    if args.search:
        await quick_search(args.search, args.num_results)
        return
    
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
    
    # 默认运行所有示例
    print("运行所有示例...\n")
    await test_connection()
    print()
    await connect_without_auth()
    await connect_with_auth()
    await connect_with_custom_config()
    await load_config_from_file()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序错误: {e}")
        sys.exit(1)