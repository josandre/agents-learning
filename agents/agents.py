# sample-agent/agent.py

import os
from dotenv import load_dotenv

from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool, google_search


from tools.build_in_tools import calculation_tool_agent, place_shipping_order
from tools.custom_function_tools import get_fee_for_payment_method, get_exchange_rate
from tools.mcp.mcp_s import mcp_filesystem_server




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


# Currency agent with custom function tools
def currency_agent(retry_config) -> Agent:
    return LlmAgent(
        name = "currency_agent",
        model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant. You must strictly follow these steps and use the available tools.

            For any currency conversion request:

            1. Get Transaction Fee: Use the get_fee_for_payment_method() tool to determine the transaction fee.
            2. Get Exchange Rate: Use the get_exchange_rate() tool to get the currency conversion rate.
            3. Error Check: After each tool call, you must check the "status" field in the response. If the status is "error", you must stop and clearly explain the issue to the user.
            4. Calculate Final Amount (CRITICAL): You are strictly prohibited from performing any arithmetic calculations yourself. You must use the calculation_agent tool to generate Python code that calculates the final converted amount. This 
                code will use the fee information from step 1 and the exchange rate from step 2.
            5. Provide Detailed Breakdown: In your summary, you must:
                * State the final converted amount.
                * Explain how the result was calculated, including:
                    * The fee percentage and the fee amount in the original currency.
                    * The amount remaining after deducting the fee.
                    * The exchange rate applied.
                """,
        tools=[get_fee_for_payment_method, get_exchange_rate, AgentTool(agent=calculation_tool_agent(retry_config))],
)


def filesystem_agent(retry_config) -> Agent:
    return LlmAgent(
        model="gemini-2.5-flash",
        name="filesystem_agent",
        instruction="""
                    You can use filesystem tools in /tmp.
                    When asked to create, list, or read a file, use the available filesystem capability.
                    Do not output code or JSON.
                    """,
        tools=[mcp_filesystem_server()],
    )

def shipping_agent(retry_config) -> Agent:
    return LlmAgent(
            name="shipping_agent",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""You are a shipping coordinator assistant.
        
        When users request to ship containers:
        1. Use the place_shipping_order tool with the number of containers and destination
        2. If the order status is 'pending', inform the user that approval is required
        3. After receiving the final result, provide a clear summary including:
            - Order status (approved/rejected)
            - Order ID (if available)
            - Number of containers and destination
        4. Keep responses concise but informative
        """,
            tools=[FunctionTool(func=place_shipping_order)],
    )






