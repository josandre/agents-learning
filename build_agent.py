from dotenv import load_dotenv

from google.adk.agents import Agent
from agents.agent_coordinators import researcher_agent_coordinator, researcher_agent_coordinator_paralell_root
from agents.agents import research_agent, shipping_agent, simple_assistan_agent, sumarizer_agent, currency_agent, filesystem_agent
from retry_config import build_retry_config


load_dotenv()


def build_agent(agent: str) -> Agent:
    retry_config = build_retry_config()

    agents = {
        "simple_assistan_agent": simple_assistan_agent,
        "research_agent": research_agent,
        "sumarizer_agent": sumarizer_agent,
        "researcher_agent_coordinator": researcher_agent_coordinator,
        "researcher_agent_coordinator_paralell_root": researcher_agent_coordinator_paralell_root,
        "currency_agent": currency_agent,
        "filesystem_agent": filesystem_agent,
        "shipping_agent": shipping_agent,
    }

    agent_requested = agents.get(agent)

    if agent_requested is None:
        raise ValueError(
            f"Unknown agent '{agent}'. "
            f"Available agents: {', '.join(agents.keys())}"
        )

    return agent_requested(retry_config)