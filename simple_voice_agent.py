"""
Simplified Voice AI Agent with CrewAI
A simpler version for testing and demonstration purposes.
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun


class SimpleVoiceAIAgent:
    """Simplified Voice AI Agent for text-based interaction"""
    
    def __init__(self):
        """Initialize the agent"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("Please set OPENAI_API_KEY environment variable")
        
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )
        
        self.search_tool = DuckDuckGoSearchRun()
        self.setup_crew()
        print("✅ Simple Voice AI Agent initialized!\n")
    
    def setup_crew(self):
        """Setup CrewAI agents"""
        
        search_tool = Tool(
            name="Search",
            func=self.search_tool.run,
            description="Search the internet for current information"
        )
        
        # Intent Understanding Agent
        self.intent_agent = Agent(
            role='Query Analyzer',
            goal='Understand user intent and extract key information',
            backstory='Expert in natural language understanding and query analysis',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Research Agent
        self.research_agent = Agent(
            role='Researcher',
            goal='Find accurate information to answer queries',
            backstory='Skilled researcher who finds reliable information',
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            llm=self.llm
        )
        
        # Response Agent
        self.response_agent = Agent(
            role='Response Generator',
            goal='Create clear and helpful responses',
            backstory='Communication expert who creates natural responses',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def process_query(self, query: str) -> str:
        """Process query with CrewAI agents"""
        print(f"\n🤖 Processing: '{query}'\n")
        
        # Task 1: Analyze query
        analyze_task = Task(
            description=f"""Analyze this query and identify:
            1. Main intent
            2. Key information needed
            3. Type of response required
            
            Query: "{query}"
            """,
            agent=self.intent_agent,
            expected_output="Analysis of query intent and requirements"
        )
        
        # Task 2: Research
        research_task = Task(
            description="Research and gather information to answer the query. Use search if needed for current information.",
            agent=self.research_agent,
            expected_output="Research findings and relevant information"
        )
        
        # Task 3: Generate response
        response_task = Task(
            description="""Generate a clear, concise response (2-3 sentences).
            Make it natural and directly answer the question.
            Return ONLY the final response.""",
            agent=self.response_agent,
            expected_output="A concise, natural response"
        )
        
        # Create and execute crew
        crew = Crew(
            agents=[self.intent_agent, self.research_agent, self.response_agent],
            tasks=[analyze_task, research_task, response_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)
    
    def run(self):
        """Run the agent in text mode"""
        print("="*60)
        print("🤖 SIMPLE VOICE AI AGENT WITH CREWAI (Text Mode)")
        print("="*60)
        print("\nType your questions below.")
        print("Type 'exit' or 'quit' to end.\n")
        print("="*60 + "\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n👋 Goodbye!\n")
                    break
                
                response = self.process_query(query)
                print(f"\n🤖 Agent: {response}\n")
                print("-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point"""
    try:
        agent = SimpleVoiceAIAgent()
        agent.run()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nSet your API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}\n")


if __name__ == "__main__":
    main()
