
import asyncio
from google.adk.runners import InMemoryRunner
from agent import build_agent


async def main():
    agent = build_agent()
    runner = InMemoryRunner(agent=agent)

    prompt = input("User > ")
    response = await runner.run_debug(prompt)

    print("\nAssistant > ", end="")
    found_text = False

    for event in response:
        if getattr(event, "author", None) == "helpful_assistant" and getattr(event, "content", None):
            for part in event.content.parts:
                text = getattr(part, "text", None)
                if text:
                    print(text)
                    found_text = True

    if not found_text:
        print("No text response found.")


if __name__ == "__main__":
    asyncio.run(main())