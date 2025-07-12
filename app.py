from smolagents import CodeAgent, DuckDuckGoSearchTool, load_tool, tool
import datetime
import requests
import pytz
import yaml
import torch
from tools.final_answer import FinalAnswerTool
from tools.free_image_generator import FreeImageGeneratorTool

from Gradio_UI import GradioUI


# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:  # it's import to specify the return type
    # Keep this format for the description / args / args description but feel free to modify the tool
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
def create_model():
    try:
        # Try to import the correct model class
        from smolagents.models import HfApiModel
        return HfApiModel(
            max_tokens=2096,
            temperature=0.5,
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
            custom_role_conversions=None,
        )
    except ImportError:
        try:
            # Fallback to using HfModel
            from smolagents.models import HfModel
            return HfModel(
                model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
                max_tokens=2096,
                temperature=0.5,
            )
        except ImportError:
            try:
                # Try alternative model setup
                from transformers import AutoTokenizer, AutoModelForCausalLM
                from smolagents.models import TransformersModel

                model_id = 'microsoft/DialoGPT-medium'  # Smaller, more compatible model
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                hf_model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    torch_dtype=torch.float32,  # Use float32 instead of float16
                    device_map="auto" if torch.cuda.is_available() else None
                )

                return TransformersModel(model=hf_model, tokenizer=tokenizer)
            except Exception as e:
                print(f"Error creating model: {e}")
                # Final fallback - use a basic model
                try:
                    from smolagents.models import OpenAIModel
                    return OpenAIModel(model_id="gpt-3.5-turbo")  # This will fail without API key but won't crash
                except:
                    return None


model = create_model()

# Import tool from Hub
try:
    image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)
except Exception as e:
    print(f"Could not load external image generation tool: {e}")
    image_generation_tool = None

# Load prompts if available, with fallback defaults
try:
    with open("prompts.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
except FileNotFoundError:
    print("prompts.yaml not found, using default prompts")
    # Create minimal required prompt templates
    prompt_templates = {
        'final_answer': "Provide the final answer to the user's question: {answer}",
        'system_prompt': "You are a helpful AI assistant that can answer questions and generate images.",
        'user_prompt': "User question: {input}",
        'planning_prompt': "Let me think about this step by step.",
        'tool_call_prompt': "I need to use a tool to help with this request.",
        'error_prompt': "I encountered an error: {error}. Let me try a different approach."
    }

image_generator = FreeImageGeneratorTool()

# Create agent with error handling
if model is None:
    print("No model available, creating a basic agent")
    # Create a simple agent without model for testing
    agent = CodeAgent(
        model=create_model(),  # Try one more time
        tools=[final_answer, image_generator],
        max_steps=6,
        verbosity_level=1,
        prompt_templates=prompt_templates
    )
else:
    try:
        agent = CodeAgent(
            model=model,
            tools=[final_answer, image_generator],  ## add your tools here (don't remove final answer)
            max_steps=6,
            verbosity_level=1,
            grammar=None,
            planning_interval=None,
            name=None,
            description=None,
            prompt_templates=prompt_templates
        )
    except Exception as e:
        print(f"Error creating agent with full config: {e}")
        # Try with minimal configuration
        agent = CodeAgent(
            model=model,
            tools=[final_answer, image_generator],
            max_steps=6,
            verbosity_level=1,
            prompt_templates=prompt_templates
        )

GradioUI(agent).launch()