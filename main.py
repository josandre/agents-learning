
import asyncio
import base64

from google.adk.runners import InMemoryRunner
from build_agent import build_agent, run_shipping_workflow
from IPython.display import display, Image as IPImage
import base64
from helpers.helper_process_events import check_for_approval, create_approval_response, print_agent_response
from helpers.show_image_helper import show_image




async def main():
    agent = build_agent("image_agent")
    runner = InMemoryRunner(agent=agent)


    prompt = input("User > ")
    
    response = await runner.run_debug(prompt)
    show_image(response)


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






