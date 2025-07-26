import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pyrogram import Client
import uvicorn

app = FastAPI()

# ✅ Session Strings & Emojis
sessions = [
    {
        "session_string": "BQFkP6MAecJP8lDAPnxVAFV8G-tGxphqRwEWjvE8_8vyUHaLREqyaEk-N1A8koY-3JKPpnH2nfP2N6DQR8wHhNmrh-PRAtYeLKnzrYfI7h6XfM4keQhznIiowiIJNqGINBdIaiAY-ohj0ysS9OwWE1cZHvjE6uDkz8-ru6nflrbqogMOPlMG85nkZ4ghUl4yO8maWbtbIlIrB0qhWlyQS0UUXJ-_XGqzxofoIaeiK4VshaN7FJvPDwJmjqfAyODqiXqVjQsOKkljv1OQeGt98xeTlCkCf_VUJtzV_M30xyiLsYn9MFv-YsTi1E7cOLbZpHDKxBqFJ8J0pnExKxQC253OJyinKwAAAAHyyQW1AA",
        "emoji": "❤️"
    },
    {
        "session_string": "BQFkP6MAvfFYzMo4v_dKtRzB9pTaaBwiIkdH8lBg-uv7FaVPIVI4xy-MRYD90W8ZElBUfxJwwojkL4zogn10V_mraazL8nSoHHlmIKgmqd0eZPFMsixPE0b0F6K2tstMRTHWt5X2nL-3fmQGVBAMdye6Vje3X35JGs7UMzMjtMHQQXijbohDWXC068hZr5Tk3NMsJ1w3L7hyYBh__2p73LCc9tZpnn9CpvDfGap4Tf2dLS5K37aEmZt72qXT1Lix20IXVQ5pWc273IndDv-h0Pxj19t_wYeuRLJiGF5b-az23-4CT32bOCO9U3LSnQTH_F3PT8QK2k4SQK8lYlvm-z8wDr10bgAAAAG__jchAA",
        "emoji": "🥰"
    },
    {
        "session_string": "BQFkP6MApjWuPUE60IqlngaK5h5iLSbikJ8zI6mMaxeA3IRJ2735IpoEXBdEHdczx1gi5H9R0xjeAJrb6GSbbolnPq8k1CSvyUA2FXSp8JMrOv0PFAUgKh8y_0UQIoMjVqfMl48suTrWOlmbYykXsXI7WL1Nh6YWgsxGlp4Bk85qPTvFfJ8GuvzIJCR0s2bLa9ALXThk4ek5QTPwK06TZeEBQkUEop75b1oVpJKU3uMoFOQxsMDkFYccuVgqqL6e1Fy_CDzE0m_eGDaByMUEKn278bbdiM_87hT-KJJjrPbclWabt-T0o8mDm0NcMhCV4jNzkdtjwQNxr04ipOjDkzKucT9SlgAAAAHEVuWUAA",
        "emoji": "😘"
    }
]

# ✅ API credentials
api_id = 23347107
api_hash = "8193110bf32a08f41ac6e9050b2a4df4"

async def react_to_post(post_link: str):
    try:
        parts = post_link.strip().split("/")
        if "t.me" not in parts[2]:
            raise ValueError("Invalid link format")
        chat = parts[-2]
        message_id = int(parts[-1])
    except Exception as e:
        return {"success": False, "error": "Invalid link format. Use: https://t.me/channel/12345"}

    responses = []

    for s in sessions:
        try:
            async with Client(
                name=s['emoji'],
                session_string=s['session_string'],
                api_id=api_id,
                api_hash=api_hash,
                in_memory=True
            ) as app:
                await app.send_reaction(chat_id=chat, message_id=message_id, emoji=s['emoji'])
                responses.append({"emoji": s["emoji"], "status": "sent"})
        except Exception as e:
            responses.append({"emoji": s["emoji"], "status": f"error: {str(e)}"})

    return {"success": True, "results": responses}

@app.get("/api")
async def api_react(request: Request):
    link = request.query_params.get("link")
    if not link:
        return JSONResponse({"success": False, "error": "Missing ?link= parameter"}, status_code=400)

    result = await react_to_post(link)
    return JSONResponse(result)

# For local test (optional)
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
