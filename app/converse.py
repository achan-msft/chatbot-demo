import streamlit
from openai import AzureOpenAI 
import json, os, uuid, jsonref  
from app.util.utility_datetime import DateTimeUtility 

class Converse():
    def __init__(self, *args, **kwds):
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.AZURE_OPENAI_DEPLOYMENT_NAME =  os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") # "gpt-4o" # os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') # "gpt-4o" #os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") # "2024-08-01-preview" # os.getenv("AZURE_OPENAI_API_VERSION") # os.environ["AZURE_OPENAI_API_VERSION"]
        
        self.TOOLS_FILE_NAME = "tools.json"
        self.tools = self.get_tools_content() # function calling   

    def get_init_system_message(self):
        system_content ="you are a helpful assistant. answer the user's query in a concise manner. if you don't understand, ask for clarification."
        system_message = { "role": "system", "content": system_content }
        
        assistant_content = "Hello! I am an AI assistant. How can I help you today?"
        assistant_message = { "role": "assistant", "content": assistant_content }

        init_messages = [system_message, assistant_message]
        return init_messages 
    
    def start(self, message_list, is_stream):
        client = AzureOpenAI(
            azure_endpoint = self.AZURE_OPENAI_ENDPOINT, 
            api_key = self.AZURE_OPENAI_API_KEY,  
            api_version = self.AZURE_OPENAI_API_VERSION
        )

        # First API call: Ask the model to use the function
        response = client.chat.completions.create(
            model=self.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=message_list,
            tools=self.tools,
            tool_choice="auto",
            stream=is_stream,
        )

        response_message = response.choices[0].message        
        message_list.append(response_message)

        if response_message.tool_calls: # self.need_extra_call(messages):
            for tool_call in response_message.tool_calls:
                message_response = self.process_message(tool_call, message_list)
                message_list.append(message_response)

            # Second API call: Get the final response from the model
            final_response = client.chat.completions.create(
                model=self.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=message_list,
            )
            final_message = final_response.choices[0].message.content
        
        else:
            final_message = message_list[-1].content

        return final_message 
    
    def process_message(self, tool_call, messages: list) -> dict:
        if tool_call.function.name == "get_current_time":
            function_args = json.loads(tool_call.function.arguments)
            time_response = DateTimeUtility.get_current_time(
                location=function_args.get("location")
            )
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": time_response,
            }

        elif tool_call.function.name == "function_calling_test":
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": "you just invoked a test function",
            }
        
    def get_tools_content(self):
        try: 
            with open(self.TOOLS_FILE_NAME, 'r') as f:
                content = f.read()
                tools = jsonref.loads(content)
                return tools 

        except Exception as e:
            print(e)
