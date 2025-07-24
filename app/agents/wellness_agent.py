from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# Instantiate the agent
wellness_agent = Agent(
    name="genetic_wellness",
    model=LiteLlm(model="gemini-2.0-flash"),
    instruction="You are an expert in general genetic wellness and health advice."
)

# Session manager and runner
session_service = InMemorySessionService()
runner = Runner(
    app_name="wellness_app",
    agent=wellness_agent,
    session_service=session_service
)

# Async logic
async def run_wellness_agent(query: str) -> str:
    # ✅ Await session creation
    session = await session_service.create_session(
        app_name="wellness_app",
        user_id="user_1"
    )
    
    message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    # Run the agent
    async for event in runner.run_async(
        user_id="user_1",
        session_id=session.id,
        new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            return text or "Sorry, no reply text received."

    return "No AI response received."

async def arun(query: str) -> str:           # <-- async entry point
    return await run_wellness_agent(query)

# Sync wrapper to call from Flask
def run(query: str) -> str:
    return asyncio.run(run_wellness_agent(query))
