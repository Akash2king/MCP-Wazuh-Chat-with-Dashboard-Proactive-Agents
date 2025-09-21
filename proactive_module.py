import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from db_module import save_message, save_tool_log

scheduler = BackgroundScheduler()
scheduler.start()
jobs = {}

def add_proactive_agent(name, interval_minutes, agent_task):
    # Remove if exists
    if name in jobs:
        scheduler.remove_job(name)
    jobs[name] = scheduler.add_job(agent_task, 'interval', minutes=interval_minutes, id=name)

def remove_proactive_agent(name):
    if name in jobs:
        scheduler.remove_job(name)
        del jobs[name]

async def default_health_check(agent):
    try:
        result = await agent.run("Check Wazuh system health and summarize")
        save_message("assistant", f"🔔 [{agent}] Proactive Update:\n{result}")
        save_tool_log("ProactiveAgent", "Health check executed")
    except Exception as e:
        save_message("assistant", f"⚠️ Proactive Check Error: {str(e)}")
