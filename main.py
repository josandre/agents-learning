
import asyncio
from google.adk.runners import InMemoryRunner, Runner
from build_agent import build_agent
from IPython.display import display, Image as IPImage
import base64
from google.adk.sessions import InMemorySessionService



async def main():
    agent = build_agent("image_agent")
    runner = InMemoryRunner(agent=agent)

    prompt = input("User > ")
    response = await runner.run_debug(prompt)

    if response:
        display_image(response)
   
    # create_agent_context(build_shipping_agent_HIL) -> Make tests

if __name__ == "__main__":
    asyncio.run(main())



def display_image(response):
   for event in response:
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "function_response") and part.function_response:
                for item in part.function_response.response.get("content", []):
                    if item.get("type") == "image":
                        display(IPImage(data=base64.b64decode(item["data"])))



def create_agent_context(agent_app) -> Runner:
    session_service = InMemorySessionService()


    return Runner(
        app = agent_app,  # Pass the app instead of the agent
        session_service=session_service,
    )





