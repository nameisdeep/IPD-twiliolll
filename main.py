from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from twilio.rest import Client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Twilio configuration
TWILIO_ACCOUNT_SID = 'ACa0649168589273e59a6d97cfb793b098'
TWILIO_AUTH_TOKEN = '5154bd246b808382b95b627a60d764c9'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Define a request model
class SMSRequest(BaseModel):
    to: str
    body: str

@app.post("/send-sms")
async def send_sms(sms_request: SMSRequest):
    try:
        message = client.messages.create(
            body=sms_request.body,
            to='+918104680835',
            from_='+18508468650'
        )
        return {"success": True, "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

# Run the server (uncomment the following line if you wish to use uvicorn programmatically)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
