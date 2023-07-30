from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime


class Data(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_input: str
    keyword: str
    text: str
    link: str
    createAt: datetime = Field(default=datetime.now())
