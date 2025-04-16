import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os
import logging

# Optional tracing (comment out if unused)
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = "key"
FROM_EMAIL = "email"
TO_EMAIL = "email"
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인만 넣는 것이 보안상 안전합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/", StaticFiles(directory="./dist", html=True), name="static")

# Optional: OpenTelemetry
FastAPIInstrumentor.instrument_app(app)


@app.post("/api/contact")
async def email(request: Request):
    try:
        data = await request.json()

        # 필수 필드 확인
        name = data.get("name")
        email = data.get("email")
        message_text = data.get("message")

        if not (name and email and message_text):
            raise HTTPException(status_code=400, detail="Missing required fields.")

        # 메일 구성
        message = Mail(
            from_email={"email": FROM_EMAIL, "name": "Contact Form"},
            to_emails=TO_EMAIL,
            subject=f"New contact form submission from {name}",
            html_content=f"""
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message_text}</p>
            """,
        )

        # SendGrid로 메일 전송
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        return {"status": "success", "sendgrid_status_code": response.status_code}

    except Exception as e:
        logging.exception("Error sending email")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)