# 08 - Voice Agent

This module demonstrates how to build a voice-powered agent using the OpenAI Agents SDK with speech-to-text integration.

## 📚 What You'll Learn

- How to use the Whisper API for audio transcription
- Integrating speech-to-text with AI agents
- Building a Vietnamese-to-English translation voice agent
- Async processing of audio files
- Working with the OpenAI Agents SDK

## 🎯 Examples

### 1. Voice Agent with Translation (`voice_agent.py`)

Demonstrates a complete voice interaction pipeline:

```python
# Process audio file
transcription, response = await process_audio(audio_path)

# Agent automatically translates Vietnamese to English
print(f"Input (Vietnamese): {transcription}")
print(f"Output (English): {response.final_output}")
```

**Key Features:**
- Audio transcription using Whisper Large V3 Turbo
- Vietnamese language support
- Agent-based processing with custom instructions
- Async/await pattern for efficient processing

## 🚀 Running the Examples

### Prerequisites

⚠️ **Important**: Voice agent requires OpenAI SDK 2.x which conflicts with standard examples (requires <2.0.0). 

**Recommended**: Use a separate virtual environment:

```bash
# Navigate to project root
cd /path/to/gpt-oss-tutorial

# Create a separate virtual environment for voice agent
python -m venv venv-voice
source venv-voice/bin/activate  # On Windows: venv-voice\Scripts\activate

# Install voice dependencies
pip install -e ".[voice]"
```

**Alternative**: If you only work with voice examples:

```bash
# From project root
pip install -e ".[voice]"
```

### Environment Setup

Create a `.env` file in the project root directory:

```bash
API_KEY=your_api_key_here
OPENAI_BASE_URL=https://mkp-api.fptcloud.com
STT_MODEL_NAME=whisper-large-v3-turbo
LLM_MODEL_NAME=gpt-oss-20b
```

### Run the Voice Agent

```bash
# From project root
python examples/08_voice_agent/voice_agent.py

# Or navigate to the example directory
cd examples/08_voice_agent
python voice_agent.py
```

### Quick Test

Verify your installation:

```bash
python -c "import openai; import agents; print('✅ Voice agent dependencies installed correctly')"
python -c "import openai; print(f'OpenAI SDK version: {openai.__version__}')"
```

Expected: OpenAI SDK version should be 2.x.x

## 📖 Core Components

### 1. Audio Transcription

Uses the OpenAI Whisper API to convert speech to text:

```python
transcription_result = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-large-v3-turbo",
    language='vi',  # Vietnamese
    response_format='verbose_json',
)
```

### 2. Agent Configuration

Creates an agent with specific instructions:

```python
en_agent = Agent(
    name="Assistant-EN",
    instructions="You MUST respond ONLY in English...",
    model="gpt-oss-20b",
)
```

### 3. Processing Pipeline

Combines transcription with agent processing:

```python
async def process_audio(audio_path: Path):
    # 1. Transcribe audio
    transcription = client.audio.transcriptions.create(...)
    
    # 2. Process with agent
    response = await Runner.run(
        starting_agent=en_agent,
        input=transcription.text,
    )
    
    return transcription.text, response
```

## 🎨 Architecture

```
┌─────────────┐
│ Audio File  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Whisper API     │  (Speech-to-Text)
│ Transcription   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Vietnamese Text │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Agent Processing│  (Translation)
│ (gpt-oss-20b)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ English Response│
└─────────────────┘
```

## 📋 Requirements

Core dependencies:
- `openai-agents[voice]>=0.4.0` - OpenAI Agents SDK with voice support
- `openai>=2.2.0` - OpenAI Python SDK
- `nest-asyncio>=1.5.8` - Nested async support
- `python-dotenv>=1.0.0` - Environment variable management
- `soundfile>=0.12.1` - Audio file I/O
- `resampy>=0.4.2` - Audio resampling
- `numpy>=2.2.0` - Numerical operations

See `requirements.txt` for complete list.

## 🔧 Configuration

### Supported Audio Formats

The Whisper API supports multiple audio formats:
- MP3
- MP4
- MPEG
- MPGA
- M4A
- WAV
- WEBM

### Language Codes

Common language codes for the `language` parameter:
- `vi` - Vietnamese
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

### Model Options

Available STT models:
- `whisper-large-v3-turbo` - Fast and accurate (recommended)
- `whisper-large-v3` - High accuracy
- `whisper-medium` - Balanced performance

## 💡 Use Cases

1. **Voice Translation Services**
   - Real-time translation from audio
   - Multi-language support
   
2. **Voice Command Systems**
   - Convert voice to text commands
   - Process with AI agents
   
3. **Transcription + Analysis**
   - Transcribe meetings/calls
   - Analyze content with AI
   
4. **Accessibility Tools**
   - Speech-to-text for accessibility
   - Automated translation

## 🎯 Best Practices

1. **Audio Quality**: Use clear audio with minimal background noise
2. **File Size**: Keep audio files under 25 MB for API calls
3. **Language Detection**: Specify the language for better accuracy
4. **Error Handling**: Always handle potential transcription errors
5. **Async Processing**: Use async/await for better performance
6. **Environment Variables**: Store sensitive data in `.env` files

## 🔗 Related Examples

- **01_basic**: For basic agent concepts
- **03_tools**: For function calling with agents
- **05_stateful**: For maintaining conversation state

## 📚 References

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents)
- [Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- [FPT Cloud AI Services](https://docs.fptcloud.com)

## 🐛 Troubleshooting

### Common Issues

**1. Audio file not found**
```
⚠️  Audio file not found: path/to/audio.mp3
```
Solution: Update `AUDIO_PATH` to point to a valid audio file.

**2. API authentication error**
```
AuthenticationError: Invalid API key
```
Solution: Check your `.env` file and ensure `API_KEY` is set correctly.

**3. Import errors**
```
ModuleNotFoundError: No module named 'agents'
```
Solution: Install dependencies with `pip install -r requirements.txt`

**4. Transcription timeout**
```
TimeoutError: Request timed out
```
Solution: Check audio file size (< 25 MB) and network connection.

## 🚧 Future Enhancements

- [ ] Real-time streaming audio processing
- [ ] WebSocket support for live transcription
- [ ] Multi-speaker diarization
- [ ] Text-to-speech response generation
- [ ] Support for more languages
- [ ] Audio preprocessing (noise reduction, normalization)

