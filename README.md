# 🎙️ Voice AI Agent with CrewAI

A sophisticated voice-enabled AI system that uses multiple CrewAI agents working together to process voice queries and provide intelligent responses.

## 🌟 Features

- **Multi-Agent AI System**: Uses CrewAI to orchestrate multiple AI agents with specialized roles
- **Voice Input**: Real-time speech recognition using Google Speech Recognition
- **Voice Output**: Natural text-to-speech responses using gTTS
- **Intelligent Processing**: Multiple agents collaborate to:
  - Understand user intent
  - Research information
  - Analyze and synthesize data
  - Generate natural conversational responses
- **Web Search**: Integrated DuckDuckGo search for current information
- **Easy to Use**: Simple voice interface - just speak naturally!

## 🏗️ Architecture

The system uses 4 specialized CrewAI agents:

1. **Voice Input Processor**: Understands and interprets user queries
2. **Information Researcher**: Finds accurate information using web search
3. **Information Analyzer**: Processes and synthesizes information
4. **Response Generator**: Creates natural, voice-friendly responses

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Microphone and speakers
- Internet connection

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Install system dependencies (Linux/Mac)

**For Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev ffmpeg
```

**For macOS:**
```bash
brew install portaudio ffmpeg
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your OpenAI API key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Or export it directly:
export OPENAI_API_KEY='your-api-key-here'
```

## 🎯 Usage

### Full Voice AI Agent

Run the complete voice-enabled agent:

```bash
python voice_ai_agent.py
```

**How to use:**
1. Wait for the greeting
2. Speak naturally into your microphone
3. The AI agents will process your query
4. Listen to the spoken response
5. Say "exit", "quit", or "goodbye" to end

**Example queries:**
- "What is the weather like today?"
- "Tell me about artificial intelligence"
- "Who won the latest Nobel Prize?"
- "Explain quantum computing in simple terms"

### Simple Text-Based Agent (No Voice)

For testing or if you don't have audio hardware:

```bash
python simple_voice_agent.py
```

Type your queries instead of speaking them.

### Test the Setup

Run the test suite to verify everything is working:

```bash
python test_agent.py
```

## 📁 Project Structure

```
.
├── voice_ai_agent.py      # Main voice AI agent with full features
├── simple_voice_agent.py  # Simplified text-based version
├── test_agent.py          # Test suite for CrewAI functionality
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .env                  # Your API keys (create this)
├── app.py               # Original Flask app
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file or export these variables:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional (defaults to gpt-4)
OPENAI_MODEL=gpt-4
# or use gpt-3.5-turbo for faster/cheaper responses
```

### Customization

You can customize the agents in `voice_ai_agent.py`:

- **Agent roles and backstories**: Modify the `setup_crew()` method
- **Response length**: Adjust the task descriptions
- **Voice settings**: Change language in `gTTS()` calls
- **LLM model**: Change in the `ChatOpenAI()` initialization

## 🛠️ Troubleshooting

### PyAudio Installation Issues

**Linux:**
```bash
sudo apt-get install python3-dev portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

### Microphone Not Working

1. Check your default microphone in system settings
2. Grant microphone permissions to your terminal
3. Test with: `python -m speech_recognition`

### OpenAI API Errors

- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure you have access to GPT-4 (or switch to gpt-3.5-turbo)

### Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

## 💡 How It Works

1. **Voice Input**: User speaks into microphone → Speech Recognition converts to text
2. **Query Processing**: Text goes through 4 specialized CrewAI agents:
   - Agent 1 analyzes the intent
   - Agent 2 researches information
   - Agent 3 synthesizes insights
   - Agent 4 generates a natural response
3. **Voice Output**: Response text → Text-to-Speech → Audio playback

## 🔬 Advanced Usage

### Using Different LLM Models

```python
# In voice_ai_agent.py, modify:
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Faster and cheaper
    temperature=0.7,
    openai_api_key=self.openai_api_key
)
```

### Adding Custom Tools

```python
# Create a custom tool
custom_tool = Tool(
    name="CustomTool",
    func=your_function,
    description="Description of what this tool does"
)

# Add to agents
self.researcher_agent = Agent(
    ...
    tools=[search_tool, custom_tool],
    ...
)
```

### Changing Voice Language

```python
# In the speak() method:
tts = gTTS(text=text, lang='es', slow=False)  # Spanish
# Supported: 'en', 'es', 'fr', 'de', 'it', 'pt', etc.
```

## 📚 Technologies Used

- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM application framework
- **OpenAI GPT-4**: Large language model
- **SpeechRecognition**: Voice input processing
- **gTTS**: Text-to-speech conversion
- **Pygame**: Audio playback
- **DuckDuckGo Search**: Web search capabilities

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 🎓 Learning Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

## 💬 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Run the test suite: `python test_agent.py`
3. Try the simple version: `python simple_voice_agent.py`

---

**Made with ❤️ using CrewAI and Python**