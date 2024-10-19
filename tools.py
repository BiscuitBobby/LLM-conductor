from langchain_core.tools import tool

@tool(return_direct=True)
def FindUser(query):
  """
  Retrieve customer related information
  args: x -> str
  """
  output = '''
  'metadata': {'user_id': 'USR009',
   'name': 'James Clark',
   'email': 'james.clark@example.com'},
  'distance': 0.5500432}
  '''
  return output

@tool(return_direct=True)
def Retrieve(query):
  """
  Retrieve customer related information
  args: x -> str
  """
  output = "20$"
  return output

@tool(return_direct=True)
def Message(query):
  """
  Message a user
  args: {username: message_body} -> str
  """
  output = "message has been sent successfully"
  return output

arsenal = [FindUser, Retrieve, Message]
