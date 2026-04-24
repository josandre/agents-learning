
import asyncio
from google.adk.runners import InMemoryRunner

from build_agent import build_agent


async def main():
    agent = build_agent("researcher_agent_coordinator")
    runner = InMemoryRunner(agent=agent)

    prompt = input("User > ")
    response = await runner.run_debug(prompt)

    print("\nAssistant > ", end="")
    found_text = False

    for event in response:
        content = getattr(event, "content", None)
        parts = getattr(content, "parts", None)

        if not parts:
            continue

        for part in parts:
            text = getattr(part, "text", None)
            if text:
                print(text)
                found_text = True

    if not found_text:
        print("No text response found.")


if __name__ == "__main__":
    asyncio.run(main())