from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins, methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio credentials and initialization
ACCOUNT_SID = 'ACa0649168589273e59a6d97cfb793b098'  # Your Account SID
AUTH_TOKEN = '5154bd246b808382b95b627a60d764c9'      # Your Auth Token
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Request model for sending SMS
class SMSRequest(BaseModel):
    to: str
    body: str

@app.post("/send-sms")
async def send_sms(sms_request: SMSRequest):
    try:
        message = client.messages.create(
            from_='+18508468650',  # Your Twilio number
            body=sms_request.body,
            to='+918104680835'
        )
        return {"success": True, "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")

# Server configuration for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
