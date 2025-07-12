from smolagents import CodeAgent, tool
import datetime
import pytz
import yaml
import torch
from tools.final_answer import FinalAnswerTool
from tools.free_image_generator import FreeImageGeneratorTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from Gradio_UI import GradioUI

# Custom tool
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

# Timezone tool
@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

# Initialize tools
final_answer = FinalAnswerTool()
image_generator = FreeImageGeneratorTool()
web_search = DuckDuckGoSearchTool()
visit_webpage = VisitWebpageTool()

# Model creation function
def create_model():
    try:
        from smolagents.models import TransformersModel
        from transformers import AutoTokenizer, AutoModelForCausalLM

        model_id = 'HuggingFaceTB/SmolLM2-1.7B-Instruct'
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        hf_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            device_map="cpu"  # Force CPU for free-tier Spaces
        )

        return TransformersModel(
            model=hf_model,
            tokenizer=tokenizer,
            max_tokens=2096,
            temperature=0.5
        )
    except Exception as e:
        print(f"Error creating model: {e}")
        return None

# Create model
model = create_model()

# Load prompts with fallback
try:
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
except FileNotFoundError:
    print("prompts.yaml not found, using default prompts")
    prompt_templates = {
        'final_answer': "Provide the final answer to the user's question: {answer}",
        'system_prompt': "You are a helpful AI assistant that can answer questions and generate images.",
        'user_prompt': "User question: {input}",
        'planning_prompt': "Let me think about this step by step.",
        'tool_call_prompt': "I need to use a tool to help with this request.",
        'error_prompt': "I encountered an error: {error}. Let me try a different approach.",
        'managed_agent': "Delegate the task to a team member: {request}"
    }

# Create agent with all tools
if model is None:
    print("No model available, cannot proceed")
    exit(1)
else:
    try:
        agent = CodeAgent(
            model=model,
            tools=[final_answer, image_generator, web_search, visit_webpage],
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
        agent = CodeAgent(
            model=model,
            tools=[final_answer, image_generator, web_search, visit_webpage],
            max_steps=6,
            verbosity_level=1,
            prompt_templates=prompt_templates
        )

# Launch Gradio UI with file upload support
file_upload_folder = "./uploads"
GradioUI(agent, file_upload_folder=file_upload_folder).launch()