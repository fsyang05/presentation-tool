#
# Registry for all LLM providers.
# todo: add more
#

from .openai import OpenAIClient

PROVIDERS = {
    "openai": OpenAIClient,
}

__all__ = ["PROVIDERS"]