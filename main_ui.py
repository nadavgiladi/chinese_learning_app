import gradio as gr
from stream_gpt import stream_gpt
chat_history = []

def yield_response_for_gradio(prompt, chat_history):
  """
  This function is used to yield the response from the stream_gpt function for Gradio.
  """
  text = ""
  for item in stream_gpt(prompt, chat_history):
    text += item
    yield text

# create Interface
gr.ChatInterface(
    fn=yield_response_for_gradio, 
    type="messages"
).launch()