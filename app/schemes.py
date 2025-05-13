from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    full_name: str
    phone: str
    message: str