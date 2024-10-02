import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sendgrid import SendGridAPIClient
import os

origins = [
    "http://localhost:3000",
    "https://fightform.gg"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)

dotenv.load_dotenv()
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

@app.get("/")
def health():
    return {"status": "healthy"}

@app.get("/subscribe")
def subscribe(email: str):
    list_id = "cb5054b6-03e0-4f42-a254-5ac31ce0c816"
    data = {
        "list_ids": [ list_id ],
        "contacts": [
            {
                "email": email,
            }
        ]
    }
    response = sg.client.marketing.contacts.put(
    request_body=data
    )
    print(response.status_code)
    print(response.body)
    print(response.headers)

