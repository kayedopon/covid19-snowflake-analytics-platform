from pydantic import BaseModel


class AnnotationCreate(BaseModel):
    country: str
    year: int
    metric: str
    comment: str
    author: str | None = None


class AnnotationUpdate(BaseModel):
    comment: str