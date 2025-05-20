import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from langchain_groq import ChatGroq

async def run_memory_chat():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"
    
    print("Initializing Chat...")
    
    # Initialize MCP client
    client = MCPClient.from_config_file(config_file)
    
    # Initialize LLM
    llm = ChatGroq(model="qwen-qwq-32b")
    
    # create agent with client
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        verbose=True,
    )
    
    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")
    
    try:
        # Main Chat loop 
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\n===== Conversation Ended =====")
                print("Thank you for using the MCP Chat!")
                print("==================================\n")
                break
            elif user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("\nConversation history cleared.")
                continue
            
            # Get response from agent
            print("\nAssistant: ", end="", flush=True)
            
            try:
                # Get response from agent
                response = await agent.run(user_input)
                print(f"\nMCP Agent: {response}")
            except Exception as e:
                print(f"Error: {e}")
    finally:
        print("\n===== Conversation Ended =====")
        print("Thank you for using the MCP Chat!")
        print("==================================\n")
        if client and client.sessions:
            await client.close_all_sessions()
        
if __name__ == "__main__":
    asyncio.run(run_memory_chat())
    
    
    
    
    