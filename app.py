import streamlit as st
import asyncio
import sqlite3
from agent_module import init_agent, run_agent
from db_module import *
from proactive_module import add_proactive_agent, remove_proactive_agent
from dashboard_module import render_dashboard
import pandas as pd

st.set_page_config(page_title="MCP Chat", layout="wide")

# Ensure database tables exist on first run
try:
    init_db()
except Exception:
    pass
st.title("🤖 MCP + Wazuh Chat with Proactive Agents & History")

# ------------------------------ Session State ------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = init_agent()
if "current_tool" not in st.session_state:
    st.session_state.current_tool = None

# ------------------------------ Sidebar - Chat History ------------------------------
st.sidebar.header("💬 Chat History")
conversations = pd.DataFrame(get_all_messages())
if not conversations.empty:
    selected_conv = st.sidebar.selectbox("View History", ["Last 50 Messages", "All Messages"])
else:
    selected_conv = None

if selected_conv == "Last 50 Messages":
    messages_to_display = conversations.tail(50).to_dict('records') if not conversations.empty else []
elif selected_conv == "All Messages":
    messages_to_display = conversations.to_dict('records') if not conversations.empty else []
else:
    messages_to_display = []

# ------------------------------ Tabs ------------------------------
tab1, tab2, tab3 = st.tabs(["💬 Chat", "⚙️ Proactive Agents", "📊 Dashboard"])

# ------------------------------ Chat Tab ------------------------------
with tab1:
    for msg in messages_to_display:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    prompt = st.chat_input("Type your message...")
    if prompt:
        save_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        response = asyncio.run(run_agent(st.session_state.agent, prompt, previous_messages=get_all_messages()))
        save_message("assistant", response)
        st.chat_message("assistant").markdown(response, unsafe_allow_html=True)

    if st.button("Clear Chat History"):
        conn = sqlite3.connect("chat_logs.db")
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        st.experimental_rerun()

# ------------------------------ Proactive Agents Tab ------------------------------
with tab2:
    st.header("Add Custom Proactive Agent (Prompt-Based)")

    name = st.text_input("Agent Name")
    interval = st.number_input("Interval (minutes)", min_value=1, value=60)
    prompt_task = st.text_area("Agent Prompt (AI will execute this prompt periodically)")

    if st.button("Add Agent"):
        if not name or not prompt_task:
            st.error("Agent Name and Prompt are required!")
        else:
            add_proactive_agent(name, interval, prompt_task, st.session_state.agent)
            st.success(f"Proactive Agent '{name}' added with prompt!")

    st.subheader("Remove Agent")
    remove_name = st.text_input("Agent Name to Remove")
    if st.button("Remove Agent"):
        remove_proactive_agent(remove_name)
        st.success(f"Removed Agent '{remove_name}'")

# ------------------------------ Dashboard Tab ------------------------------
with tab3:
    render_dashboard()
