from connection import config
from agents import Agent,Runner,FunctionTool,function_tool
from search_engines import google_search
import requests





# Tool Calling
# Function as Tool
# @function_tool
def search_engine(search_prompt):
    url = google_search.get_search_url(search_prompt)
    # print(url)
    resp = requests.get(url)
    # print(resp)
    html = resp.text
    # print(resp.text)
    results = google_search.extract_search_results(html,page_url=url)
    return html

print(search_engine("Iran Israel war"))

# # 
# agent = Agent(
#     name="Assistant",
#     instructions=
#     """You are an assistant who help user for every prompt.If you have not answer call `search_engine` and give results from that
#         If ypu face any error while accessing tool also explain that error
#     """,
#     tools=[search_engine]

# )


# result = Runner.run_sync(
#     agent,
#     input="what is latest news about Iran-Israel conflict?",
#     run_config= config
# )

# print(result.final_output)