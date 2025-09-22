import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from db_module import save_message, save_tool_log

# Singleton scheduler to survive Streamlit reloads
_scheduler = None
_jobs = {}

def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.start()
    return _scheduler

def add_proactive_agent(name, interval_minutes, prompt, agent_obj, retries=2):
    """Add a proactive agent that runs the prompt periodically in the background"""
    async def job_task():
        attempt = 0
        while attempt <= retries:
            try:
                # Always use max_steps=10
                response = await agent_obj.run(f"Proactive Task Prompt: {prompt}", max_steps=10)
                save_message("assistant", f"🔔 [{name}] Proactive Update:\n{response}")
                save_tool_log(name, f"Prompt executed: {prompt}")
                break
            except Exception as e:
                save_message("assistant", f"⚠️ [{name}] Proactive Check Error (Attempt {attempt+1}): {str(e)}")
                attempt += 1
                await asyncio.sleep(5)  # Wait before retry

    def run_async_job():
        try:
            asyncio.run(job_task())
        except RuntimeError:
            # If already running an event loop (e.g. with Streamlit), use create_task
            loop = asyncio.get_event_loop()
            loop.create_task(job_task())

    # Remove existing job if any
    scheduler = get_scheduler()
    if name in _jobs:
        scheduler.remove_job(name)
    _jobs[name] = scheduler.add_job(run_async_job, 'interval', minutes=interval_minutes, id=name)

def remove_proactive_agent(name):
    scheduler = get_scheduler()
    if name in _jobs:
        scheduler.remove_job(name)
        del _jobs[name]