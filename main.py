
import asyncio
import logging
import base64
from pathlib import types
import uuid

from google.adk.runners import InMemoryRunner, Runner
from agents.agent_coordinators import build_shipping_agent_HIL
from agents.agents import shipping_agent
from build_agent import build_agent, run_shipping_workflow
from IPython.display import display, Image as IPImage
from google.adk.sessions import InMemorySessionService

from helpers.helper_process_events import check_for_approval, create_approval_response, print_agent_response





async def main():
    agent = build_agent("build_shipping_agent_HIL")
    runner = InMemoryRunner(agent=agent)

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="u",
        session_id="s",
    )

    prompt = input("User > ")
    
    response = await runner.run_debug(prompt)

async def long_running_operations():
     await run_shipping_workflow(
        "Ship 3 containers to Singapore",
    )
     
     await run_shipping_workflow(
        "Ship 10 containers to Rotterdam",
        auto_approve=True,
    )
     
     await run_shipping_workflow(
        "Ship 8 containers to Los Angeles",
        auto_approve=False,
    )



if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(long_running_operations())






