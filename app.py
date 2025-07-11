from smolagents import CodeAgent, DuckDuckGoSearchTool, load_tool, tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
from tools.free_image_generator import FreeImageGeneratorTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# Use the model from Hugging Face Hub instead of HfApiModel
try:
    # Try to import the correct model class
    from smolagents.models import HfApiModel
    model = HfApiModel(
        max_tokens=2096,
        temperature=0.5,
        model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
        custom_role_conversions=None,
    )
except ImportError:
    # Fallback to using a model from the hub
    try:
        from smolagents.models import HfModel
        model = HfModel(
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
            max_tokens=2096,
            temperature=0.5,
        )
    except ImportError:
        # Final fallback - use a simpler model setup
        print("Warning: Using fallback model configuration")
        # You might need to adjust this based on what's available in your smolagents version
        model = None

# Import tool from Hub
try:
    image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)
except Exception as e:
    print(f"Could not load external image generation tool: {e}")
    image_generation_tool = None

# Load prompts if available
try:
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
except FileNotFoundError:
    print("prompts.yaml not found, using default prompts")
    prompt_templates = None

image_generator = FreeImageGeneratorTool()

# Create agent with error handling
try:
    agent = CodeAgent(
        model=model,
        tools=[final_answer, image_generator], ## add your tools here (don't remove final answer)
        max_steps=6,
        verbosity_level=1,
        grammar=None,
        planning_interval=None,
        name=None,
        description=None,
        prompt_templates=prompt_templates
    )
except Exception as e:
    print(f"Error creating agent: {e}")
    # Create a basic agent without model specification
    agent = CodeAgent(
        tools=[final_answer, image_generator],
        max_steps=6,
        verbosity_level=1,
    )

GradioUI(agent).launch()