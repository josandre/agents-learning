from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search

from agents.agents import research_agent, sumarizer_agent


# This agent Orchestrates the workflow by calling sub-agents as tools. Is not a DO-ALL agent
def researcher_agent_coordinator(retry_config) -> Agent:
    return Agent(
            name="ResearchCoordinator",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=retry_config
            ),
            # This instruction tells the root agent HOW to use its tools (which are the other agents).
            instruction=(
                    "You are a coordinator agent. "
                    "Use the research agent when information is needed. "
                    "Use the summarizer agent only after research findings exist. "
                    "Read the value from `final_summary` and return that value to the user as the final answer. "
                    "Do not add extra commentary."),
            # We wrap the sub-agents in `AgentTool` to make them callable tools for the root agent.
            tools=[AgentTool(research_agent(retry_config)), AgentTool(sumarizer_agent(retry_config))],
)
