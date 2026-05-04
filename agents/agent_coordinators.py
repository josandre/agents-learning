from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.apps.app import App, ResumabilityConfig
from agents.agents import research_agent, shipping_agent, sumarizer_agent, tech_researcher, health_researcher, finance_researcher, aggregator_agent


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

# The ParallelAgent runs all its sub-agents simultaneously.
def researcher_agent_coordinator_paralell(retry_config) -> Agent:
    return ParallelAgent(
            name="ParallelResearchTeam",
            sub_agents=[tech_researcher(retry_config), health_researcher(retry_config), finance_researcher(retry_config)],
        )

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.    
def  researcher_agent_coordinator_paralell_root(retry_config) -> Agent:
    return SequentialAgent(
        name="ResearchSystem",
        sub_agents=[researcher_agent_coordinator_paralell(retry_config), aggregator_agent(retry_config)],
    )


def build_shipping_agent_HIL() -> App:
    return App(
        name="shipping_coordinator",
        root_agent=shipping_agent(),
        resumability_config=ResumabilityConfig(is_resumable=True),
    )



