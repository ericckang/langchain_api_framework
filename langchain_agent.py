from langchain.agents import Tool, LLMSingleActionAgent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from apis.stockdata_api import StockAPI
from apis.fred_api import FREDAPI
from core.api_factory import APIFactory
from core.custom_prompt_template import CustomPromptTemplate
from core.custom_output_parser import CustomOutputParser
from config import OPENAI_API_KEY
import json

# Define tools
def get_stock_quotes_tool(ticker_symbols):
    print("Fetching stock quotes...")
    stock_api_class = APIFactory.get_api('stock')
    stock_api = stock_api_class()
    quotes = stock_api.fetch_data(ticker_symbols)
    return json.dumps(quotes, indent=4)

def get_financial_news_tool(ticker_symbols):
    print("Fetching financial news...")
    stock_api_class = APIFactory.get_api('stock')
    stock_api = stock_api_class()
    news = stock_api.fetch_news(ticker_symbols)
    return json.dumps(news, indent=4)

def get_fred_search(search_text):
    print("FRED SEARCH")
    fred_api_class = APIFactory.get_api('fred')
    fred_api = fred_api_class()
    result = fred_api.fetch_data(search_text)
    parsed_response = fred_api.parse_response(result, num_results=2)
    result_json = json.dumps(parsed_response, indent=4)
    return result_json

def get_champion_rotations_tool():
    print("Fetching League of Legends champion rotations...")
    league_api_class = APIFactory.get_api('league')
    league_api = league_api_class()
    rotations = league_api.fetch_data() 
    parsed_rotations = league_api.parse_response(rotations)
    rotations_json = json.dumps(parsed_rotations, indent=4)
    return rotations_json

def get_brawlstars_event_rotation_tool():
    print("Fetching Brawlstars event rotations...")
    brawlstars_api_class = APIFactory.get_api('brawlstars')
    brawlstars_api = brwalstars_api_class()
    rotations = brawlstars_api.fetch_data()
    parsed_rotations = brawlstars_api.parse_response(rotations)
    rotations_json = json.dumps(parsed_rotations, indent=4)
    return rotations_json

def get_recipe_tool(meal_name: str):
    print(f"Fetching recipe for {meal_name}...")
    meal_db_api_class = APIFactory.get_api('meal')
    meal_db_api = meal_db_api_class()
    recipe = meal_db_api.fetch_data(meal_name)
    parsed_recipe = meal_db_api.parse_response(recipe)
    return json.dumps(parsed_recipe, indent=4)

tools = [
    Tool(
        name="get_stock_quotes",
        func=lambda input: get_stock_quotes_tool(input),
        description="Get the latest stock quotes for given ticker symbols. The input should be a comma-separated list of ticker symbols."
    ),
    Tool(
        name="get_financial_news",
        func=lambda input: get_financial_news_tool(input),
        description="Get the latest financial news. The input should be a comma-separated list of ticker symbols."
    ),
    Tool(
        name="search_in_Federal_Reserve_Bank_of_St_Louis",
        func=lambda input: get_fred_search(input),
        description="Search for economic data series from the Federal Reserve Economic Data (FRED) API. The input should be a string containing the search text."
    ),
    Tool(
        name="get_champion_rotations",
        func=lambda input: get_champion_rotations_tool(),
        description="Fetches the current champion rotations for League of Legends."
    ),
    Tool(
        name="get_recipe",
        func=lambda input: get_recipe_tool(input),
        description="Fetches the recipe for the specified meal from TheMealDB. The input should be the name of the meal."
    )
]

# Load the model
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

# Define a custom prompt template
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    input_variables=["input", "intermediate_steps"]
)

output_parser = CustomOutputParser()
llm_chain = LLMChain(llm=llm, prompt=prompt)

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=[tool.name for tool in tools]
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

def ask_agent(question):
    print(f"Asking agent: {question}")
    response = agent_executor.run(question)
    print(json.dumps(response, indent=4))
    return response

if __name__ == "__main__":
    print("Ask about stock quotes...")
    response = ask_agent("What are the latest stock quotes for AAPL and TSLA?")

    #print("Ask about financial news...")
    #response = ask_agent("What's the latest financial news for TSLA and MSFT?")

    #print("Ask about FRED")
    #response = ask_agent("Search for economic data series related to monetary service index in the Federal Reserve Bank of St. Louis database")

    #print("Get champion rotations...")
    #response = ask_agent("Get champion rotations in league of legends")

    #print("Get recipe...")
    #response = ask_agent("What is the recipe for Arrabiata?")

    
