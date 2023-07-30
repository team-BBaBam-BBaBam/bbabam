from typing import List, Any, Dict
from sqlmodel import Session, create_engine, select
from .model import Data

DB_URL = "sqlite:///./database.db"
engine = create_engine(DB_URL)
Data.metadata.create_all(engine)


def save_data(keyword:str, data: Dict[str, str]) -> None:
    with Session(engine) as session:
        data["keyword"] = keyword
        data_model = Data(**data)
        session.add(data_model)
        session.commit()


def save_multiple_data(keyword: str, data_list: List[Dict[str, str]]) -> None:
    with Session(engine) as session:
        for data in data_list:
            data["keyword"] = keyword
            data_model = Data(**data)
            session.add(data_model)
        session.commit()

def read_data() -> List[Data]:
    with Session(engine) as session:
        statement = select(Data)
        results = session.exec(statement)
        data_list = results.all()
        for data in data_list:
            data.contents = data.contents.split(', ')
        return data_list