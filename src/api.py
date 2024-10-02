import dotenv
from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sendgrid import SendGridAPIClient
import os

origins = ["http://localhost:3000", "https://fightform.gg"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

dotenv.load_dotenv()
sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))


@app.get("/")
def health():
    return {"status": "healthy"}


@app.get("/subscribe")
def subscribe(email: str):

    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized

    except EmailNotValidError as e:

        print(str(e))
        return {"error": "invalid email"}

    list_id = "cb5054b6-03e0-4f42-a254-5ac31ce0c816"
    data = {
        "list_ids": [list_id],
        "contacts": [
            {
                "email": email,
            }
        ],
    }
    response = sg.client.marketing.contacts.put(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)
    if response.status_code >= 400:
        return {"subscribe": "failure"}
    elif response.status_code == 200:
        return {"subscribe": "success"}
    else:
        return {"subscribe": response.status_code}
