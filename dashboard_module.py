import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

DB_FILE = "chat_logs.db"

def get_tool_usage():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT tool_name, COUNT(*) as usage_count FROM tools_log GROUP BY tool_name", conn)
    conn.close()
    return df

def get_proactive_stats():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(
        "SELECT tool_name, timestamp FROM tools_log WHERE tool_name='ProactiveAgent' ORDER BY timestamp", conn)
    conn.close()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        stats = df.groupby('hour').size().reset_index(name='executions')
        return stats
    return pd.DataFrame(columns=['hour','executions'])

def get_alerts():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(
        "SELECT content, timestamp FROM messages WHERE content LIKE '⚠️%'", conn)
    conn.close()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def render_dashboard():
    st.subheader("📊 Tool Usage Chart")
    df_tools = get_tool_usage()
    if not df_tools.empty:
        st.bar_chart(df_tools.set_index('tool_name')['usage_count'])
    else:
        st.info("No tool usage data yet.")

    st.subheader("🛠 Proactive Agent Execution Stats")
    df_proactive = get_proactive_stats()
    if not df_proactive.empty:
        st.line_chart(df_proactive.set_index('hour')['executions'])
    else:
        st.info("No proactive agent execution data yet.")

    st.subheader("🚨 Alerts")
    df_alerts = get_alerts()
    if not df_alerts.empty:
        st.table(df_alerts[['timestamp', 'content']])
    else:
        st.info("No alerts detected yet.")
