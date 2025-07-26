import asyncio
from pyrogram import Client
from fastapi import FastAPI, Request
import uvicorn

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
    },
    {
        "session_string": "BQFkP6MATNv1_ZvSbYgncqNuF4pBZ43S9196GeNvxdstxOyQfxtKSsKZZD5oYQ5rbkgMAsfiqu5GQAk6TR4LLTOQaSvhDNtpPNMk6MeEG3wcLYHktiFO2ac0ejZLc7SzbYoOshsoKbz1NYFK3hDdsQf2sMXQr_c6GAkP0ksYbuATldMZf4hi1_OR8UkPpT5hXH4UXZFQXpdqaBHDzY6XuVkkv9pkd7sRZ3FfAruFU7pFvy_pqkRe_3R1rIEtpnfdxmzWB2wzhWRWdjjZCiA0EmlRidgXftcQs7p6jDiIGjSowDkvZWTLynxeLS1ustTPuSX8AuUZSb30NKXPsTfBpZ_uwLkfAAAAAAHQPiQNAA",
        "emoji": "😍"
    },
    {
        "session_string": "BQFkP6MADUdYCtGiaVdFCLEs3Oaev-80pB5fkv55ePT6RhvDJpQiLw4LKisieBN8dqoh1tB03xrNAkuO2617NDr3xJ_w1Uf90T85hJidAE_lcJ3SjF0JNMaeuXzqokN1-lXG2THbiGu81jWXIdHhbUutzEA9JWRrYgrjZnDN7Y5XQW9QgkfAtkF9aF-KHxoQWXwjW6NHwl9ulBolscCu7RUQ6S6uNI9a3vHUI7Zy-G_RPvjMKMevoawnv_RgMrGhMAmGpy6ccP2d3hHxw4GW5LZqPZcTnpay2BKEDC04gT2Ec4baT5s_CDlmfiqBPy_MrScYxEJjZgZdGu5q_YEb1kxvkHdIOgAAAAG9GPzuAA",
        "emoji": "🥴"
    }
]

# ✅ API credentials
api_id = 23347107
api_hash = "8193110bf32a08f41ac6e9050b2a4df4"

app = FastAPI()

@app.get("/api")
async def react(request: Request):
    link = request.query_params.get("link")
    if not link:
        return {"status": "error", "message": "Missing ?link parameter."}

    try:
        parts = link.strip().split("/")
        chat = parts[-2]
        msg_id = int(parts[-1])
    except:
        return {"status": "error", "message": "Invalid link format."}

    result = []

    for s in sessions:
        try:
            async with Client(
                name=s["emoji"],
                session_string=s["session_string"],
                api_id=api_id,
                api_hash=api_hash,
                in_memory=True
            ) as app:
                await app.send_reaction(chat_id=chat, message_id=msg_id, emoji=s["emoji"])
                result.append({"emoji": s["emoji"], "status": "sent"})
        except Exception as e:
            result.append({"emoji": s["emoji"], "status": "error", "error": str(e)})

    return {"status": "done", "results": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
