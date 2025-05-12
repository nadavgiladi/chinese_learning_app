import gradio as gr
import asyncio
from stream_gpt_mcp import stream_gpt_mcp
from introduced_vocabulary_and_tools_handling.tools_mcp import tools_sse_client

chat_history = []

async def yield_response_for_gradio(prompt, chat_history, client):
  """
  This function is used to yield the response from the stream_gpt function for Gradio.
  """

  text = ""
  stream = stream_gpt_mcp(client, prompt, chat_history)
  async for item in stream:
    text += item
    yield text

async def main():
  # initialize the mcp server and client to have access to the tools
  global client 
  client = await tools_sse_client.initialize_mcp_server_and_client()

  # create Interface
  gr.ChatInterface(
      fn=yield_response_for_gradio, 
      type="messages"
  ).launch()

if __name__ == "__main__":
  # run the main function
  asyncio.run(main())