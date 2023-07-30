from sqlmodel import SQLModel, Field
from typing import List, Optional

class Data(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    text: str
    link: str
