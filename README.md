# Overview 
This project serves as the basic skeleton of a chatbot.

## Prerequisites
-   [Azure OpenAI Model](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions)   
-   [Visual Code](https://code.visualstudio.com/)
-   Python version >= 3.9 

## Setup 
Follow the steps  
1.  Set up the virtual environment  
```python -m venv <your-virtual-environment-name> ```  

2.  Install the prerequisites  
```pip install -r requirements.txt```  

3.  Run the following command  
```streamlit run main.py```  

## Configuration  
Populate the following in the file .env for Azure resources.  You may get them from AI Foundry Studio.  
- AZURE_OPENAI_ENDPOINT   
- AZURE_OPENAI_API_KEY  
- AZURE_OPENAI_API_VERSION   
- AZURE_OPENAI_DEPLOYMENT_NAME   
