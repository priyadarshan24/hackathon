from google.adk.agents import Agent, LlmAgent
from google.adk.tools import FunctionTool

def get_current_time(city: str) -> str:
    """
    Gets current time in a specified city.
    Args:
        city (str): The name of the city to get the current time for.
    Returns:
        A string with the current time in the specified city.
    """
    return f"The current time in {city} is 10:00 AM."

def get_current_weather(city: str) -> str:
    """
    Gets current weather in a specified city.
    Args:
        city (str): The name of the city to get the current weather for.
    Returns:
        A string with the current weather in the specified city.
    """
    return f"The current weather in {city} is sunny with a temperature of 25°C."


time_tool = FunctionTool(get_current_time)
weather_tool = FunctionTool(get_current_weather)

time_sub_agent = LlmAgent(
    name="time_sub_agent",
    model="gemini-2.0-flash",
    description="Sub-agent to answer questions about the time in a city.",
    instruction="You are a time expert. Use the 'get_current_time' tool to answer questions about the current time.",
    tools=[time_tool])

weather_sub_agent = LlmAgent(
    name="weather_sub_agent",
    model="gemini-2.0-flash",
    description="Sub-agent to answer questions about the weather in a city.",
    instruction="You are a weather expert. Use the 'get_current_weather' tool to answer questions about the current weather.",
    tools=[weather_tool])

root_agent = LlmAgent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about the current time and weather in a city.",
    instruction="""You are a multi-tool agent that can answer questions about the current time and weather in a specified city.""",
    sub_agents=[time_sub_agent, weather_sub_agent],
)