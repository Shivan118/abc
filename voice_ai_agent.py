"""
Voice AI Agent with CrewAI
A sophisticated voice-enabled AI system using multiple CrewAI agents
that work together to process voice queries and provide intelligent responses.
"""

import os
import sys
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import tempfile
from datetime import datetime


class VoiceAIAgent:
    """
    Main Voice AI Agent class that integrates speech recognition,
    text-to-speech, and CrewAI agents for intelligent conversation.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Voice AI Agent
        
        Args:
            openai_api_key: OpenAI API key for LLM (defaults to env variable)
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )
        
        # Initialize tools
        self.search_tool = DuckDuckGoSearchRun()
        
        # Setup CrewAI agents
        self.setup_crew()
        
        print("🎤 Voice AI Agent initialized successfully!")
    
    def setup_crew(self):
        """Setup CrewAI agents with different roles"""
        
        # Search tool for agents
        search_tool = Tool(
            name="Search",
            func=self.search_tool.run,
            description="Useful for searching the internet for current information, facts, news, and data."
        )
        
        # 1. Listener Agent - Processes and understands the input
        self.listener_agent = Agent(
            role='Voice Input Processor',
            goal='Accurately understand and interpret user voice input, extract intent and key information',
            backstory="""You are an expert in natural language understanding with years of 
            experience in processing voice commands. You excel at understanding context, 
            intent, and extracting meaningful information from user queries.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 2. Researcher Agent - Searches and gathers information
        self.researcher_agent = Agent(
            role='Information Researcher',
            goal='Find accurate and relevant information to answer user queries',
            backstory="""You are a skilled researcher with expertise in finding reliable 
            information from various sources. You know how to verify facts and provide 
            comprehensive answers based on current data.""",
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            llm=self.llm
        )
        
        # 3. Analyzer Agent - Processes and analyzes information
        self.analyzer_agent = Agent(
            role='Information Analyzer',
            goal='Analyze gathered information and synthesize insights',
            backstory="""You are an analytical expert who excels at processing complex 
            information, identifying patterns, and drawing meaningful conclusions. You can 
            break down complex topics into understandable insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 4. Response Agent - Generates conversational responses
        self.response_agent = Agent(
            role='Conversational Response Generator',
            goal='Create natural, engaging, and helpful voice responses',
            backstory="""You are a communication expert specialized in voice interactions. 
            You create responses that sound natural when spoken aloud, are concise yet 
            informative, and maintain a friendly, professional tone.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def listen(self) -> Optional[str]:
        """
        Listen to user voice input and convert to text
        
        Returns:
            Transcribed text or None if recognition failed
        """
        print("\n🎤 Listening... (speak now)")
        
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            
            # Convert speech to text using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected. Timeout.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def speak(self, text: str):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to convert to speech
        """
        print(f"\n🔊 Agent: {text}\n")
        
        try:
            # Create text-to-speech
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"❌ Error in text-to-speech: {e}")
    
    def process_query(self, query: str) -> str:
        """
        Process user query through CrewAI agents
        
        Args:
            query: User's query text
            
        Returns:
            Generated response
        """
        print("\n🤖 Processing with AI agents...")
        
        # Task 1: Understand the query
        understand_task = Task(
            description=f"""Analyze this user query and extract the key intent and information needed:
            Query: "{query}"
            
            Provide:
            1. Main intent of the query
            2. Key entities or topics mentioned
            3. Type of response needed (factual, opinion, action, etc.)
            4. Any implicit context or assumptions""",
            agent=self.listener_agent,
            expected_output="A detailed analysis of the user's query including intent, entities, and response requirements"
        )
        
        # Task 2: Research information
        research_task = Task(
            description="""Based on the query analysis, research and gather relevant information.
            Find current, accurate data that will help answer the user's query comprehensively.
            Use search tools if needed for current information.""",
            agent=self.researcher_agent,
            expected_output="Comprehensive research findings with relevant facts, data, and sources"
        )
        
        # Task 3: Analyze and synthesize
        analyze_task = Task(
            description="""Analyze the researched information and synthesize key insights.
            Create a structured summary that addresses the user's query.
            Ensure accuracy and relevance.""",
            agent=self.analyzer_agent,
            expected_output="A synthesized analysis with key insights and structured information"
        )
        
        # Task 4: Generate voice-friendly response
        response_task = Task(
            description="""Create a natural, conversational voice response.
            The response should be:
            - Concise (30-50 words ideally, max 100 words)
            - Natural when spoken aloud
            - Directly answer the query
            - Friendly and professional
            - Easy to understand
            
            Return ONLY the final response text, nothing else.""",
            agent=self.response_agent,
            expected_output="A concise, natural voice response (30-100 words)"
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[
                self.listener_agent,
                self.researcher_agent,
                self.analyzer_agent,
                self.response_agent
            ],
            tasks=[
                understand_task,
                research_task,
                analyze_task,
                response_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Extract the response text
        response = str(result)
        return response
    
    def run(self):
        """
        Main run loop for the voice AI agent
        """
        print("\n" + "="*60)
        print("🎙️  VOICE AI AGENT WITH CREWAI")
        print("="*60)
        print("\nWelcome! I'm your AI assistant with voice capabilities.")
        print("I use multiple AI agents to provide intelligent responses.")
        print("\nCommands:")
        print("  - Speak naturally to ask questions")
        print("  - Say 'exit', 'quit', or 'goodbye' to end")
        print("  - Press Ctrl+C to force quit")
        print("="*60 + "\n")
        
        self.speak("Hello! I am your voice AI assistant. How can I help you today?")
        
        while True:
            try:
                # Listen for user input
                query = self.listen()
                
                if query is None:
                    continue
                
                # Check for exit commands
                if any(word in query.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                    self.speak("Goodbye! Have a great day!")
                    break
                
                # Process query with CrewAI agents
                response = self.process_query(query)
                
                # Speak the response
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                self.speak("I'm sorry, I encountered an error. Please try again.")


def main():
    """Main entry point"""
    try:
        # Initialize and run the voice AI agent
        agent = VoiceAIAgent()
        agent.run()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
