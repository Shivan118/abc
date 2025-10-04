# 🚀 Quick Start Guide - Voice AI Agent with CrewAI

## ⚡ Fast Setup (5 minutes)

### Step 1: Install Dependencies

```bash
# Quick install with the setup script
bash setup.sh
```

Or manually:

```bash
# Install Python packages
pip install -r requirements.txt

# Linux only:
sudo apt-get install python3-pyaudio portaudio19-dev ffmpeg
```

### Step 2: Set API Key

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='sk-your-key-here'
```

### Step 3: Test It!

```bash
# Test the setup (text-based, no voice needed)
python test_agent.py
```

If that works, try the simple text agent:

```bash
# Simple text-based agent
python simple_voice_agent.py
```

Then try the full voice agent:

```bash
# Full voice-enabled agent
python voice_ai_agent.py
```

## 📝 Example Interaction

```
$ python simple_voice_agent.py

🤖 SIMPLE VOICE AI AGENT WITH CREWAI (Text Mode)
============================================================

Type your questions below.
Type 'exit' or 'quit' to end.

============================================================

You: What is CrewAI?

🤖 Processing: 'What is CrewAI?'

[Agent processing...]

🤖 Agent: CrewAI is a framework for orchestrating autonomous AI agents 
that work together to accomplish complex tasks. It enables multiple 
specialized agents to collaborate, share information, and solve problems 
more effectively than a single agent could alone.

------------------------------------------------------------
```

## 🎯 What Each Script Does

### `test_agent.py`
- Tests basic CrewAI functionality
- No voice I/O required
- Quick verification that everything works
- **Start here!**

### `simple_voice_agent.py`
- Text-based agent (type instead of speak)
- Full multi-agent collaboration
- No microphone/speakers needed
- Great for testing agent logic

### `voice_ai_agent.py`
- Full voice-enabled agent
- Speak naturally, hear responses
- Requires microphone and speakers
- Complete voice AI experience

## 🔑 Getting OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Set it in your environment:
   ```bash
   export OPENAI_API_KEY='sk-your-key-here'
   ```

## ⚠️ Common Issues

### "No module named 'crewai'"
```bash
pip install crewai langchain langchain-openai
```

### "No OPENAI_API_KEY"
```bash
export OPENAI_API_KEY='your-key'
# Or add to ~/.bashrc or ~/.zshrc
```

### "PyAudio not found"
**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

### "Cannot access microphone"
- Check system microphone permissions
- Try the simple text version instead: `python simple_voice_agent.py`

## 💡 Tips

1. **Start with the test script** to verify setup
2. **Use simple_voice_agent.py** for testing without voice
3. **Grant microphone permissions** when prompted
4. **Use headphones** to avoid audio feedback
5. **Speak clearly** and wait for the listening prompt

## 📊 Cost Estimates

Using GPT-4:
- ~$0.01-0.05 per query (depends on complexity)
- Multiple agents = multiple API calls
- Consider using gpt-3.5-turbo for lower cost

To use GPT-3.5 (cheaper and faster):
```python
# In voice_ai_agent.py, change:
model="gpt-3.5-turbo"  # instead of "gpt-4"
```

## 🎬 Next Steps

After getting it running:

1. **Customize agents** - Edit their roles and backstories
2. **Add tools** - Integrate weather, calendar, etc.
3. **Change voice** - Try different languages in gTTS
4. **Optimize costs** - Use gpt-3.5-turbo instead of gpt-4
5. **Build your app** - Integrate into your own projects!

## 📚 Learn More

- Full documentation: See [README.md](README.md)
- CrewAI docs: https://docs.crewai.com/
- LangChain docs: https://python.langchain.com/

---

**Ready? Run `python test_agent.py` to get started!** 🚀
