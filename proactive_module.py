import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from db_module import save_message, save_tool_log

scheduler = BackgroundScheduler()
scheduler.start()
jobs = {}

def add_proactive_agent(name, interval_minutes, prompt, agent_obj):
    """Add a proactive agent that runs the prompt periodically"""
    async def job_task():
        try:
            response = await agent_obj.run(f"Proactive Task Prompt: {prompt}")
            save_message("assistant", f"🔔 [{name}] Proactive Update:\n{response}")
            save_tool_log(name, f"Prompt executed: {prompt}")
        except Exception as e:
            save_message("assistant", f"⚠️ [{name}] Proactive Check Error: {str(e)}")

    # Remove existing job if any
    if name in jobs:
        scheduler.remove_job(name)
    jobs[name] = scheduler.add_job(lambda: asyncio.run(job_task()), 'interval', minutes=interval_minutes, id=name)

def remove_proactive_agent(name):
    if name in jobs:
        scheduler.remove_job(name)
        del jobs[name]
