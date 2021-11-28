from datetime import datetime
from sqlalchemy.sql.expression import null, update
from werkzeug.exceptions import NotFound
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from dataclasses import dataclass

from app.exceptions.issue_exceptions import InvalidKeysError

@dataclass
class IssueModel(db.Model):
    post_valid_keys = ["desc"]
    update_valid_keys = ["desc", "todo", "doing", "done"]

    id: int
    desc: str
    create_at: datetime
    todo: bool
    doing: bool
    done: bool

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    create_at = Column(DateTime, default=datetime.now())
    todo = Column(Boolean, default=True)
    doing = Column(Boolean, default=False)
    done = Column(Boolean, default=False)

    @staticmethod
    def post_validate(data):
        for key in data.keys():
            if not key in IssueModel.post_valid_keys:
                raise InvalidKeysError("invalid data to register a new issue")
    
    @staticmethod
    def update_validate(data):
        for key in data.keys():
            if not key in IssueModel.update_valid_keys:
                raise InvalidKeysError("invalid data to update an issue")
