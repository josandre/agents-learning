import uuid

from dotenv import load_dotenv
from google.adk import Runner
from google.adk.agents import Agent
from agents.agent_coordinators import build_shipping_agent_HIL, researcher_agent_coordinator, researcher_agent_coordinator_paralell_root
from agents.agents import research_agent, shipping_agent, simple_assistan_agent, sumarizer_agent, currency_agent, filesystem_agent, image_agent
from helpers.helper_process_events import check_for_approval, create_approval_response, print_agent_response
from retry_config import build_retry_config
from google.adk.sessions import InMemorySessionService
from google.genai import types


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
        "image_agent": image_agent
    }

    agent_requested = agents.get(agent)

    if agent_requested is None:
        raise ValueError(
            f"Unknown agent '{agent}'. "
            f"Available agents: {', '.join(agents.keys())}"
        )

    return agent_requested(retry_config)



async def run_shipping_workflow(query: str, auto_approve: bool = True):
    """Runs a shipping workflow with approval handling.

    Args:
        query: User's shipping request
        auto_approve: Whether to auto-approve large orders (simulates human decision)
    """

    session_service = InMemorySessionService()

    # Create runner with the resumable app
    shipping_runner = Runner(
        app=build_shipping_agent_HIL(),  # Pass the agent
        session_service=session_service,
    )

    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session
    await session_service.create_session(
        app_name="shipping_coordinator", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # STEP 1: Send initial request to the Agent. If num_containers > 5, the Agent returns the special `adk_request_confirmation` event
    async for event in shipping_runner.run_async(
        user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # STEP 2: Loop through all the events generated and check if `adk_request_confirmation` is present.
    approval_info = check_for_approval(events)

    # --------------------------------------------
      # -----------------------------------------------------------------------------------------------
    # STEP 3: If the event is present, it's a large order - HANDLE APPROVAL WORKFLOW
    if approval_info:
        print(f"⏸️  Pausing for approval...")
        print(f"🤔 Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # PATH A: Resume the agent by calling run_async() again with the approval decision
        async for event in shipping_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(
                approval_info, auto_approve
            ),  # Send human decision here
            invocation_id=approval_info[
                "invocation_id"
            ],  # Critical: same invocation_id tells ADK to RESUME
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent > {part.text}")

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    else:
        # PATH B: If the `adk_request_confirmation` is not present - no approval needed - order completed immediately.
        print_agent_response(events)

    print(f"{'='*60}\n")




     
    

     

     








