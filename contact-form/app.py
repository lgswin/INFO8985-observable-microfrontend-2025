import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv
import os
import logging

# Optional tracing (comment out if unused)
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = "sender@example.com"
TO_EMAIL = "recipient@example.net"
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
app.mount("/static", StaticFiles(directory="./dist"), name="static")

# Optional: OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def read_root():
    return FileResponse("./dist/index.html")

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

        # 테스트 모드: 실제 이메일 전송 대신 성공 응답 반환
        print(f"테스트 모드: {name}님의 메시지가 성공적으로 처리되었습니다.")
        print(f"이메일: {email}")
        print(f"메시지: {message_text}")
        
        return {"status": "success", "message": "Form submitted successfully (test mode)"}

    except Exception as e:
        print(str(e))
        logging.exception("Error sending email")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)