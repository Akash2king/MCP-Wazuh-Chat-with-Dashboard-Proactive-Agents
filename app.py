import streamlit as st
import asyncio
from agent_module import init_agent, run_agent
from db_module import *
from proactive_module import add_proactive_agent, remove_proactive_agent, default_health_check
from dashboard_module import render_dashboard
import pandas as pd

st.set_page_config(page_title="MCP Chat", layout="wide")
st.title("🤖 MCP + Wazuh Chat with Dashboard & Proactive Agents")

# ------------------------------ Session State ------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = init_agent()
if "current_tool" not in st.session_state:
    st.session_state.current_tool = None

# ------------------------------ Tabs ------------------------------
tab1, tab2, tab3 = st.tabs(["💬 Chat", "⚙️ Proactive Agents", "📊 Dashboard"])

# ------------------------------ Chat Tab ------------------------------
with tab1:
    # Chat history selection
    st.subheader("Chat History Management")
    messages_df = pd.DataFrame(get_all_messages())
    if not messages_df.empty:
        conv_to_show = st.selectbox("Select Conversation", ["All Messages", "Last 50 Messages"])
        if conv_to_show == "Last 50 Messages":
            messages_to_display = messages_df.tail(50).to_dict('records')
        else:
            messages_to_display = messages_df.to_dict('records')
    else:
        messages_to_display = []

    for msg in messages_to_display:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Chat input
    prompt = st.chat_input("Type your message...")
    if prompt:
        save_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        # Run agent
        response = asyncio.run(run_agent(st.session_state.agent, prompt, previous_messages=get_all_messages()))
        save_message("assistant", response)
        st.chat_message("assistant").markdown(response, unsafe_allow_html=True)

    # Clear chat button
    if st.button("Clear Chat History"):
        conn = sqlite3.connect("chat_logs.db")
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        st.experimental_rerun()

# ------------------------------ Proactive Agents Tab ------------------------------
with tab2:
    st.header("Manage Proactive Agents")
    st.subheader("Add Custom Proactive Agent")
    name = st.text_input("Agent Name")
    interval = st.number_input("Interval (minutes)", min_value=1, value=60)
    task_code = st.text_area("Agent Task (Python code, use 'agent' variable)")

    if st.button("Add Agent"):
        try:
            exec(f"async def custom_task(agent):\n    {task_code.replace(chr(10), chr(10)+'    ')}", globals())
            add_proactive_agent(name, interval, lambda: asyncio.run(globals()['custom_task'](st.session_state.agent)))
            st.success(f"Proactive Agent '{name}' added!")
        except Exception as e:
            st.error(f"Error adding agent: {e}")

    st.subheader("Remove Agent")
    remove_name = st.text_input("Agent Name to Remove")
    if st.button("Remove Agent"):
        remove_proactive_agent(remove_name)
        st.success(f"Removed Agent '{remove_name}'")

# ------------------------------ Dashboard Tab ------------------------------
with tab3:
    render_dashboard()
