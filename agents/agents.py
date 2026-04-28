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


def tech_researcher(retry_config) -> Agent:
    return Agent(
        name="TechResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
                        the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",  # The result of this agent will be stored in the session state with this key.
        )       

def health_researcher(retry_config) -> Agent:
    return Agent(
            name="HealthResearcher",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=retry_config
            ),
            instruction="""Research recent medical breakthroughs. Include 3 significant advances,
                            their practical applications, and estimated timelines. Keep the report concise (100 words).""",
            tools=[google_search],
            output_key="health_research",  # The result will be stored with this key.
        )


def finance_researcher(retry_config) -> Agent:
    return Agent(
    name="FinanceResearcher",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        instruction="""Research current fintech trends. Include 3 key trends,
                        their market implications, and the future outlook. Keep the report concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",  # The result will be stored with this key.
    )


def aggregator_agent(retry_config) -> Agent:
    return Agent(
        name="AggregatorAgent",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
        instruction="""Combine these three research findings into a single executive summary:

        **Technology Trends:**
        {tech_research}
        
        **Health Breakthroughs:**
        {health_research}
        
        **Finance Innovations:**
        {finance_research}
        
        Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
        output_key="executive_summary",  # This will be the final output of the entire system.
)






