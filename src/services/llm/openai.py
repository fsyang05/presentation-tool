from services.llm.config import LLMConfig, PresentationLevels, Prompt
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OpenAIConfig = LLMConfig(
    instructions = Prompt,
    max_output_tokens = 10000,
    model = "gpt-5"
)

class OpenAIClient:
    def __init__(self):
        self._config = OpenAIConfig
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_response(self, presentation: PresentationLevels):
        formatted_data = {
            "title": "Repair/Replacement Options",
            "subtitle": "Generated presentation",
            "level_1": presentation.level_1.model_dump(),
            "level_2": presentation.level_2.model_dump(),
            "level_3": presentation.level_3.model_dump(),
            "level_4": presentation.level_4.model_dump(),
        }
        return formatted_data

    def generate_response(self, input: str):
        try:
            response = self._client.responses.parse(
                model=self._config.model,
                instructions=self._config.instructions,
                input=input,
                max_output_tokens=self._config.max_output_tokens,
                text_format=PresentationLevels
            )
            data = self.format_response(response.output_parsed)
            return {"success": True, "data": data}
        
        except openai.APIError as e:
            # todo: retry or log here
            print(f"OpenAI API returned an API Error: {e}")
            return {"success": False, "error": str(e)}
        except openai.APIConnectionError as e:
            # todo: handle this
            print(f"Failed to connect to OpenAI API: {e}")
            return {"success": False, "error": str(e)}
        except openai.RateLimitError as e:
            # todo: handle this
            print(f"OpenAI API request exceeded rate limit: {e}")
            return {"success": False, "error": str(e)}    