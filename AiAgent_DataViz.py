#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pyautogen')


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import Image
import os
import autogen


# In[4]:


config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-0125", "gpt-3.5-turbo", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-instruct"],
    },
)


# In[5]:


llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="NEVER",
)

coder = autogen.AssistantAgent(
    name="Coder",  # the default assistant agent is capable of solving problems with code
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER VISUALIZATION BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
- bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
- Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field first converted to a date object etc?
- Goal compliance (compliance): how well the code meets the specified visualization goals?
- Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be more effective in conveying insights? If a different visualization type is more appropriate, the score MUST BE LESS THAN 5.
- Data encoding (encoding): Is the data encoded appropriately for the visualization type?
- aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

YOU MUST PROVIDE A SCORE for each of the above dimensions.
{bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
Do not suggest code.
Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


# In[6]:


user_proxy.reset()
coder.reset()
critic.reset()
groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(
    manager,
    message="download data from https://raw.githubusercontent.com/MainakRepositor/Datasets/master/Cryptocurrency/bitcoin-sv.csv and create an insightful graph that can show the predicted stock data trend. Save the plot to a file. Print the fields in a dataset before visualizing it. Take the feedback from the critic to improve the code.",
)


# In[10]:


import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Implementing error handling for download
url = "https://raw.githubusercontent.com/MainakRepositor/Datasets/master/Cryptocurrency/bitcoin-sv.csv"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Error downloading the dataset:", e)

# Save the dataset with the correct filename
file_name = "bitcoin-sv.csv"
with open(file_name, "wb") as file:
    file.write(response.content)

# Load the data into a DataFrame
data = pd.read_csv(file_name)

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Handle missing values if needed
# Example: data.dropna(inplace=True)

# Visualize the data using a time series plot
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], color='blue', linestyle='-', marker='o')
plt.title('Bitcoin SV Stock Data Trend')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig('bitcoin_sv_stock_trend.png')
plt.show()


# In[ ]:



