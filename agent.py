# sample-agent/agent.py

import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

load_dotenv()


def build_agent() -> Agent:
    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=2,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

    return Agent(
        name="helpful_assistant",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config,
        ),
        description="A simple assistant that answers general questions.",
        instruction=(
            "You are a precise and reliable assistant. "
            "Use Google Search when information may be outdated or uncertain."
        ),
        tools=[google_search],
    )