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
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings
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

class SimpleTokenVerifier(TokenVerifier):
    """
    Simple token verifier that checks if the token matches a predefined API token.
    """
    
    def __init__(self, api_token: str):
        self.api_token = api_token
    
    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """
        Verify the token against the predefined API token.
        
        Args:
            token: The bearer token to verify
            
        Returns:
            AccessToken if valid, None otherwise
        """
        if token == self.api_token:
            return AccessToken(
                token=token,
                client_id="api-client",
                scopes=["api.access"]
            )
        return None

# Initialize FastMCP with authentication if enabled
if ENABLE_AUTH and API_TOKEN:
    # Create token verifier only when authentication is properly enabled
    token_verifier = SimpleTokenVerifier(API_TOKEN)
    
    # Create auth settings with required URLs
    # Using the server's own URL as both issuer and resource server for simplicity
    server_url = f"http://{HTTP_HOST}:{HTTP_PORT}"
    auth_settings = AuthSettings(
        issuer_url=f"{server_url}/",
        resource_server_url=f"{server_url}/mcp/"
    )
    
    mcp = FastMCP("GoogleSearch", token_verifier=token_verifier, auth=auth_settings, host=HTTP_HOST, port=HTTP_PORT)
else:
    mcp = FastMCP("GoogleSearch", host=HTTP_HOST, port=HTTP_PORT)


@mcp.tool()
async def search_google(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Perform a Google search and return formatted results.
    
    This function uses Google Custom Search API to search the web based on the provided query.
    It formats the results into a consistent structure and handles potential errors.
    
    Args:
        query (str): The search query string
        num_results (int, optional): Number of search results to return. Defaults to 5.
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - success (bool): Whether the search was successful
            - results (list): List of dictionaries with title, link, and snippet
            - total_results (str): Total number of results found (when successful)
            - error (str): Error message (when unsuccessful)
    """
    
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
    
    # 使用 FastMCP 的 run 方法启动服务器
    mcp.run(transport="streamable-http")
