import asyncio
import aiohttp
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from introduced_vocabulary_and_tools_handling.tools_mcp import tools_server

async def initialize_mcp_server_and_client():
  """
  This function initializes the MCP server and client.
  It runs the server in a background task and creates a client instance to connect to the server.
  """

  # create a client instance
  url = "http://127.0.0.1:8050/mcp/"

  # run the server in the background
  server_task = asyncio.create_task(tools_server.run_mcp_server())

  # explicit transport type for the client
  transport_type = StreamableHttpTransport(url=url)
  client = Client(transport_type)
  
  await asyncio.sleep(2)  # wait for the server to start
  
  return client
  
async def list_tools(client):
    """
    This function lists the tools available in the MCP server. in the format expected by OpenAI.
    """

    async with client:
        tools_result = await client.list_tools()

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                },
            }
            for tool in tools_result
        ]
    
async def use_tool(client, tool_name, parameters={}):
    """
    This function uses a specific tool from the MCP server. It sends a request to the server and returns the result of the tool."""
    async with client:
        tool_result = await client.call_tool(tool_name, parameters)

        return tool_result


