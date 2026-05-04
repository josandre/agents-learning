
import asyncio
import logging
import base64

from google.adk.runners import InMemoryRunner, Runner
from build_agent import build_agent
from IPython.display import display, Image as IPImage
from google.adk.sessions import InMemorySessionService
from google.genai import types





async def main():
    agent = build_agent("filesystem_agent")
    runner = InMemoryRunner(agent=agent)

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="u",
        session_id="s",
    )

    prompt = input("User > ")
    response = await runner.run_debug(prompt)

   
    # create_agent_context(build_shipping_agent_HIL) -> Make tests

if __name__ == "__main__":
    asyncio.run(main())



def create_agent_context(agent_app) -> Runner:
    session_service = InMemorySessionService()


    return Runner(
        app = agent_app,  # Pass the app instead of the agent
        session_service=session_service,
    )





