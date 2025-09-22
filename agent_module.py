import os
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient
from langchain_groq import ChatGroq

load_dotenv()

def init_agent():
    config = {
        "mcpServers": {
            "wazuh": {
                "command": os.getenv("MCP_COMMAND"),
                "args": [],
                "env": {
                    "WAZUH_API_HOST": os.getenv("WAZUH_API_HOST"),
                    "WAZUH_API_PORT": os.getenv("WAZUH_API_PORT"),
                    "WAZUH_API_USERNAME": os.getenv("WAZUH_API_USERNAME"),
                    "WAZUH_API_PASSWORD": os.getenv("WAZUH_API_PASSWORD"),
                    "WAZUH_INDEXER_HOST": os.getenv("WAZUH_INDEXER_HOST"),
                    "WAZUH_INDEXER_PORT": os.getenv("WAZUH_INDEXER_PORT"),
                    "WAZUH_INDEXER_USERNAME": os.getenv("WAZUH_INDEXER_USERNAME"),
                    "WAZUH_INDEXER_PASSWORD": os.getenv("WAZUH_INDEXER_PASSWORD"),
                    "WAZUH_VERIFY_SSL": os.getenv("WAZUH_VERIFY_SSL"),
                    "WAZUH_TEST_PROTOCOL": os.getenv("WAZUH_TEST_PROTOCOL"),
                    "RUST_LOG": os.getenv("RUST_LOG")
                }
            }
        }
    }

    client = MCPClient.from_dict(config)
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=os.getenv("GROQ_API_KEY")
    )
    # Set max_steps to 10 for all agent runs
    agent = MCPAgent(llm=llm, client=client, max_steps=10)
    return agent

async def run_agent(agent, prompt, previous_messages=[]):
    # Include RAG context
    context_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in previous_messages])
    full_prompt = f"{context_prompt}\nUser: {prompt}\nAssistant:"
    # Make sure max_steps is always 10 for each run (if agent.run supports override)
    result = await agent.run(full_prompt, max_steps=10)
    return result