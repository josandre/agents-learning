# sample-agent/agent.py

import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from retry_config import build_retry_config


load_dotenv()

# DO-ALL agent
def simple_assistan_agent(retry_config) -> Agent:
    
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


def research_agent(retry_config) -> Agent:
    return Agent(
        name="ResearchAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",  # The result of this agent will be stored in the session state with this key.
    )


# summarize the response from specialized_research_agent using research_findings state key
def sumarizer_agent(retry_config) -> Agent:
    return  Agent(
        name="SummarizerAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        # The instruction is modified to request a bulleted list for a clear output format.
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary", # The result of this agent will be stored in the session state with this key.
    )






