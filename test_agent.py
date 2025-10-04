"""
Test script for Voice AI Agent
This script tests the basic functionality without voice I/O
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


def test_basic_crew():
    """Test basic CrewAI functionality"""
    print("🧪 Testing CrewAI Basic Functionality\n")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Please set OPENAI_API_KEY environment variable")
        return False
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=api_key
        )
        print("✅ LLM initialized")
        
        # Create a simple agent
        agent = Agent(
            role='Test Agent',
            goal='Respond to test queries',
            backstory='You are a helpful AI assistant for testing',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        print("✅ Agent created")
        
        # Create a simple task
        task = Task(
            description="Say hello and introduce yourself as a CrewAI test agent in one sentence.",
            agent=agent,
            expected_output="A brief greeting and introduction"
        )
        print("✅ Task created")
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        print("✅ Crew created")
        
        # Execute
        print("\n" + "="*60)
        print("Executing test...")
        print("="*60 + "\n")
        
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result)
        print("="*60 + "\n")
        
        print("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_multi_agent():
    """Test multiple agents working together"""
    print("\n🧪 Testing Multi-Agent Collaboration\n")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Please set OPENAI_API_KEY environment variable")
        return False
    
    try:
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # Agent 1: Analyst
        analyst = Agent(
            role='Question Analyst',
            goal='Analyze questions and break them down',
            backstory='Expert at understanding and analyzing questions',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
        # Agent 2: Responder
        responder = Agent(
            role='Answer Provider',
            goal='Provide clear and concise answers',
            backstory='Expert at creating helpful responses',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
        # Tasks
        analyze_task = Task(
            description="Analyze this question: 'What is CrewAI?' Identify what information is needed.",
            agent=analyst,
            expected_output="Analysis of the question"
        )
        
        respond_task = Task(
            description="Based on the analysis, provide a clear 2-sentence answer about CrewAI.",
            agent=responder,
            expected_output="A concise answer about CrewAI"
        )
        
        # Crew
        crew = Crew(
            agents=[analyst, responder],
            tasks=[analyze_task, respond_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("\n" + "="*60)
        print("Executing multi-agent test...")
        print("="*60 + "\n")
        
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result)
        print("="*60 + "\n")
        
        print("✅ Multi-agent test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Multi-agent test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("VOICE AI AGENT TEST SUITE")
    print("="*60 + "\n")
    
    # Run tests
    test1 = test_basic_crew()
    test2 = test_multi_agent()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Basic Crew Test: {'✅ PASSED' if test1 else '❌ FAILED'}")
    print(f"Multi-Agent Test: {'✅ PASSED' if test2 else '❌ FAILED'}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
