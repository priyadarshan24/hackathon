from google.adk.agents import Agent, LlmAgent
from google.adk.tools import FunctionTool
from db_run import SessionLocal
from models import Contact, Chassis

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
    Args:https://github.com/priyadarshan24/hackathon.git
        city (str): The name of the city to get the current weather for.
    Returns:
        A string with the current weather in the specified city.
    """
    return f"The current weather in {city} is sunny with a temperature of 25°C."

def update_new_number_for_chassis(chassis: str, new_mobile: str) -> str:
    """
    Gets chassis number and the required mobile number to be updated and against it
    Args:https://github.com/priyadarshan24/hackathon.git
        chassis (str): the chassis number of the user
        new_mobile (str): the mobile number which the user wants to update
    Returns:
        A string with the current weather in the specified city.
    """
    try:
        db = SessionLocal()
        chassis = db.query(Chassis).filter_by(chassis_number=chassis).first()

        if not chassis:
            return f"No chassis found with number {chassis}."

        contact = chassis.contact
        if not contact:
            return f"No contact linked to chassis {chassis}."

        old_phone = contact.phone

        if old_phone == new_mobile:
            return f"The mobile number {new_mobile} is already associated with chassis {chassis}."
        contact.phone = new_mobile
        db.commit()

        return (
            f"Phone number for chassis {chassis} updated successfully.\n"
            f"Old Number: {old_phone}\n"
            f"New Number: {new_mobile}"
        )
    except Exception as e:
        db.rollback()
        return f"Error updating phone number for chassis {chassis}: {str(e)}"
    finally:
        db.close()

# TODO
def fetch_number_against_chassis(mobile: str) -> str:
    """
    Gets chassis number against the given mobile number
    Args:https://github.com/priyadarshan24/hackathon.git
        mobile (str): the chassis number of the user
    Returns:
        A string with the deatils.
    """

    try:
        db = SessionLocal()
        chassis = db.query(Chassis).filter_by(chassis_number=chassis).first()

        if chassis:
            mobile = {chassis.contact.phone}
            if mobile:
                return f"The chassis {mobile} has the following mobile number {mobile}."
            else:
                return f"No mobile number found for chassis {chassis}."
    except Exception as e:
        return f"Error fetching number for chassis {chassis}: {str(e)}"
    finally:
        db.close()

def fetch_chassis_against_number(chassis: str) -> str:
    """
    Gets mobile number against the given chassis number
    Args:https://github.com/priyadarshan24/hackathon.git
        chassis (str): the chassis number of the user
    Returns:
        A string with the deatils.
    """

    try:
        db = SessionLocal()
        chassis = db.query(Chassis).filter_by(chassis_number=chassis).first()

        if chassis:
            mobile = {chassis.contact.phone}
            if mobile:
                return f"The chassis {mobile} has the following mobile number {mobile}."
            else:
                return f"No mobile number found for chassis {chassis}."
    except Exception as e:
        return f"Error fetching number for chassis {chassis}: {str(e)}"
    finally:
        db.close()

# Agent Wrappers
time_tool = FunctionTool(get_current_time)
weather_tool = FunctionTool(get_current_weather)
mob_number_update_tool = FunctionTool(update_new_number_for_chassis)
get_chassis_mobile = FunctionTool(fetch_number_against_chassis)
get_chassis_number = FunctionTool(fetch_chassis_against_number)

mob_number_update_agent = LlmAgent(
    name="mob_number_update_agent",
    model="gemini-2.0-flash",
    description="Agent to update mobile number for a given customer",
    instruction="You are an .", # TODO
    tools=[time_tool])

get_chassis_mobile_agent = LlmAgent(
    name="get_chassis_mobile",
    model="gemini-2.0-flash",
    description="Agent to update mobile number for a given customer",
    instruction="You are an ai agent to fetch details from database. Use the 'get_chassis_mobile' tool to answer questions", # TODO
    tools=[time_tool])

get_chassis_number_agent = LlmAgent(
    name="get_chassis_number",
    model="gemini-2.0-flash",
    description="Agent to update mobile number for a given customer",
    instruction="You are an ai agent to fetch details from database. Use the 'get_chassis_number' tool to answer questions", # TODO
    tools=[time_tool])

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