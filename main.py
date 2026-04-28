
import asyncio
from google.adk.runners import InMemoryRunner

from build_agent import build_agent


async def main():
    agent = build_agent("researcher_agent_coordinator_paralell_root")
    runner = InMemoryRunner(agent=agent)

    prompt = input("User > ")
    response = await runner.run_debug(prompt)
    

if __name__ == "__main__":
    asyncio.run(main())