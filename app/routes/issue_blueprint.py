from os import name
from flask import Blueprint
from app.controllers.issue_controller import create, read_all, read_by_id, update, delete

bp = Blueprint("bp_issue", __name__, url_prefix="/issues")

bp.post("")(create)
bp.get("")(read_all)
bp.get("/<int:issue_id>")(read_by_id)
bp.patch("/<int:issue_id>")(update)
bp.delete("/<int:issue_id>")(delete)
