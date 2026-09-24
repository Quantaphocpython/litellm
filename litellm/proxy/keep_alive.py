import asyncio
import os
import logging
import httpx

logger = logging.getLogger("LiteLLM_KeepAlive")

async def start_keep_alive():
    """
    Sends a periodic HTTP GET ping to keep Render / Cloud free instances awake.
    Configured via environment variables:
      - KEEP_ALIVE_URL or RENDER_EXTERNAL_URL: Target URL to ping (e.g., https://my-litellm.onrender.com/health/liveness)
      - KEEP_ALIVE_INTERVAL_MINUTES: Interval in minutes (default: 10 minutes)
    """
    url = os.getenv("KEEP_ALIVE_URL") or os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        logger.info("[KeepAlive] Disabled: KEEP_ALIVE_URL or RENDER_EXTERNAL_URL is not set.")
        return

    # Normalize URL to target /health/liveness endpoint
    if not url.endswith("/health/liveness") and not url.endswith("/health"):
        if url.endswith("/"):
            url = f"{url}health/liveness"
        else:
            url = f"{url}/health/liveness"

    try:
        interval_minutes = float(os.getenv("KEEP_ALIVE_INTERVAL_MINUTES", "10"))
    except ValueError:
        interval_minutes = 10.0

    interval_seconds = interval_minutes * 60.0

    logger.info(f"[KeepAlive] Enabled: Target URL = {url}, Interval = {interval_minutes} minutes")

    # Initial delay before starting periodic ping loop
    await asyncio.sleep(30)

    async with httpx.AsyncClient(timeout=15.0) as client:
        while True:
            try:
                response = await client.get(url)
                logger.info(f"[KeepAlive] Ping {url} -> Status {response.status_code}")
            except Exception as e:
                logger.warning(f"[KeepAlive] Ping {url} failed: {str(e)}")
            
            await asyncio.sleep(interval_seconds)
