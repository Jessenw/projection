from pydantic import BaseModel

class Project(BaseModel):
    id: str
    title: str
    content: str