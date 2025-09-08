"""
Google Search MCP Server

A FastMCP server that provides Google Custom Search functionality.
This server exposes a tool for performing Google searches and returning formatted results.
It requires Google API Key and Custom Search Engine ID stored in environment variables.

Features:
- Streamable HTTP transport support for real-time communication
- Configurable host and port via environment variables
- Google Custom Search API integration
- Error handling and formatted result responses

Environment Variables:
- GOOGLE_API_KEY: Your Google API key (required)
- GOOGLE_CSE_ID: Your Custom Search Engine ID (required)
- HTTP_HOST: Server host (default: 127.0.0.1)
- HTTP_PORT: Server port (default: 9000)
- ENABLE_AUTH: Enable authentication (default: false)
- API_TOKEN: Bearer token for API authentication (required when ENABLE_AUTH=true)

Usage:
1. Copy .env.example to .env and configure your API keys
2. For production use, enable authentication by setting ENABLE_AUTH=true and API_TOKEN
3. Run: python main.py
4. Server will start at http://127.0.0.1:9000/mcp/
5. When authentication is enabled, clients must include Authorization header:
   Authorization: Bearer your_api_token_here
"""

import os
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

# HTTP Stream server configuration
HTTP_HOST = os.getenv('HTTP_HOST', '127.0.0.1')
HTTP_PORT = int(os.getenv('HTTP_PORT', '9000'))

# Authentication configuration
API_TOKEN = os.getenv('API_TOKEN')
ENABLE_AUTH = os.getenv('ENABLE_AUTH', 'false').lower() == 'true'

def verify_auth_token(token: Optional[str]) -> bool:
    """
    Verify the authentication token.
    
    Args:
        token (Optional[str]): The bearer token to verify
        
    Returns:
        bool: True if token is valid, False otherwise
    """
    if not ENABLE_AUTH:
        return True
    
    if not token:
        return False
        
    return token == API_TOKEN

# Initialize FastMCP with authentication
mcp = FastMCP(
    "GoogleSearch",
    auth_token=API_TOKEN if ENABLE_AUTH else None
)


@mcp.tool()
async def search_google(query: str, num_results: int = 5, auth_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform a Google search and return formatted results.
    
    This function uses Google Custom Search API to search the web based on the provided query.
    It formats the results into a consistent structure and handles potential errors.
    
    Args:
        query (str): The search query string
        num_results (int, optional): Number of search results to return. Defaults to 5.
        auth_token (Optional[str]): Authentication token for API access
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - success (bool): Whether the search was successful
            - results (list): List of dictionaries with title, link, and snippet
            - total_results (str): Total number of results found (when successful)
            - error (str): Error message (when unsuccessful)
    """
    # Verify authentication
    if not verify_auth_token(auth_token):
        return {
            "success": False,
            "error": "Authentication failed: Invalid or missing API token",
            "results": []
        }
    
    try:
        # Initialize Google Custom Search API
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        
        # Execute the search
        # pylint: disable=no-member
        result = service.cse().list(
            q=query,
            cx=GOOGLE_CSE_ID,
            num=num_results
        ).execute()
        
        # Format the search results
        formatted_results = []
        if "items" in result:
            for item in result["items"]:
                formatted_results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return {
            "success": True,
            "results": formatted_results,
            "total_results": result.get("searchInformation", {}).get("totalResults", "0")
        }
    
    except HttpError as error:
        return {
            "success": False,
            "error": f"API Error: {str(error)}",
            "results": []
        }
    except Exception as error:  # pylint: disable=broad-exception-caught
        return {
            "success": False,
            "error": str(error),
            "results": []
        }

if __name__ == "__main__":
    # 使用Streamable HTTP模式启动服务，支持环境变量配置
    print(f"Starting Google Search MCP server with Streamable HTTP transport...")
    print(f"Server will be available at: http://{HTTP_HOST}:{HTTP_PORT}/mcp/")
    
    if ENABLE_AUTH:
        print(f"Authentication: ENABLED (Bearer Token required)")
        if API_TOKEN:
            print(f"API Token: {'*' * len(API_TOKEN)}")
        else:
            print("WARNING: Authentication enabled but no API_TOKEN configured!")
    else:
        print("Authentication: DISABLED (insecure mode)")
    
    mcp.run(
        transport="streamable-http",
        host=HTTP_HOST,
        port=HTTP_PORT
    )
