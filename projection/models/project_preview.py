from pydantic import BaseModel

class ProjectPreview(BaseModel):
    id: str
    title: str
    author: str