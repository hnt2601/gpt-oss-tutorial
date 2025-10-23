# ─── Standard Library ──────────────────────────────────────────────────────────
import asyncio
import os
from pathlib import Path

# ─── Third-Party ───────────────────────────────────────────────────────────────
import nest_asyncio
from openai import OpenAI
from agents import Agent, Runner
from agents.tracing import set_tracing_disabled
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Disable tracing to avoid sending telemetry to OpenAI servers
set_tracing_disabled(True)

# ───────────────────────────────────────────────────────────────────────────────
nest_asyncio.apply()

# ✏️  Put your key in an env-var or just replace the call below.
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://mkp-api.fptcloud.com")
API_KEY = os.getenv("API_KEY")
STT_MODEL_NAME = os.getenv("STT_MODEL_NAME", "whisper-large-v3-turbo")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-oss-20b")

# Set OpenAI SDK environment variables (required by openai-agents)
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = BASE_URL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
print("✅ OpenAI client ready")


# ── 1 · agent that replies in English ---------------------------------------
en_agent = Agent(
    name="Assistant-EN",
    instructions=(
        "You MUST respond ONLY in English. Your task is to translate Vietnamese text to English. "
        "Provide ONLY the English translation in a single sentence. Do NOT explain, do NOT add commentary, "
        "do NOT respond in Vietnamese. Just the English translation."
    ),
    model=LLM_MODEL_NAME,
)

# ── 2 · Simple voice interaction using HTTP transcription ------------------
async def process_audio(audio_path: Path):
    """Process audio file using regular HTTP transcription (not WebSocket).
    
    Args:
        audio_path: Path to the audio file to process
        
    Returns:
        Tuple of (transcription_text, agent_response)
    """
    
    print(f"\n🎤 Transcribing audio from: {audio_path.name}")
    
    # Transcribe using regular HTTP API
    with audio_path.open('rb') as f:
        transcription_result = client.audio.transcriptions.create(
            file=f,
            model=STT_MODEL_NAME,
            language='vi',  # Vietnamese
            response_format='verbose_json',
        )
    
    # Extract the text from the response
    transcription_text = transcription_result.text
    
    print(f"\n[User]: {transcription_text}")
    print("[Assistant]: ", end="", flush=True)
    
    # Get response from agent using Runner
    response = await Runner.run(
        starting_agent=en_agent,
        input=transcription_text,
    )
    
    # Print the response
    if response.final_output:
        print(response.final_output, flush=True)
    else:
        # Fallback to printing messages
        for message in response.new_messages:
            if hasattr(message, 'content'):
                print(message.content, flush=True)
    
    return transcription_text, response


async def main():
    """Main function to demonstrate voice agent usage."""
    # Example audio path - update this to your actual audio file
    AUDIO_PATH = Path('hello_fpt.mpga')
    
    if not AUDIO_PATH.exists():
        print(f'⚠️  Audio file not found: {AUDIO_PATH}')
        print('Please update AUDIO_PATH to point to a valid audio file.')
        return
    
    # Process the audio file
    transcription, response = await process_audio(AUDIO_PATH)
    
    print("\n" + "="*60)
    print("✅ Processing complete!")
    print(f"Transcription: {transcription}")
    print(f"Response: {response.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

