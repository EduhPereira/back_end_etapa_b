from flask import request, current_app, jsonify
from app.exceptions.issue_exceptions import InvalidKeysError
from app.models.issue_model import IssueModel
from werkzeug.exceptions import NotFound

def create():
    data = request.get_json()
    try:
        IssueModel.post_validate(data)
        new_issue = IssueModel(**data)
        current_app.db.session.add(new_issue)
        current_app.db.session.commit()
        return jsonify(new_issue), 201
    except InvalidKeysError as e:
        return {"error":str(e)}, 409

def read_all():
    issues = (
        IssueModel.query.all()
    )

    issues_found = [IssueModel for IssueModel in issues]
    return jsonify(issues_found), 200

def read_by_id(issue_id):
    try:
        issue_found = IssueModel.query.get_or_404(issue_id, description="issue not found")
        current_app.db.session.commit()
        return jsonify(issue_found), 200
    except NotFound as e:
        return {"error":e.description}, 404

def update(issue_id):
    data = request.get_json()
    try:
        issue_found = IssueModel.query.get_or_404(issue_id, description="issue not found to be updated")

        IssueModel.update_validate(data)

        for key in data.keys():   
            if key == "doing":
                new_data = data.copy()
                new_data['todo'] = False
                new_data['doing'] = True
                new_data['done'] = False
            elif key == "done":
                new_data = data.copy()
                new_data['todo'] = False
                new_data['doing'] = False
                new_data['done'] = True
            else:
                new_data = data.copy()
                new_data['todo'] = True
                new_data['doing'] = False
                new_data['done'] = False

        for key, value in new_data.items():
            setattr(issue_found, key, value)
        
        current_app.db.session.add(issue_found)
        current_app.db.session.commit()
        return jsonify(issue_found), 200
    except (InvalidKeysError, NotFound) as e:
        if type(e).__name__ == "InvalidKeysError":
            return {"error":str(e)}, 409

        if type(e).__name__ == "NotFound":
            return {"error":e.description}, 404

def delete(issue_id):
    try:
        issue_found = IssueModel.query.get_or_404(issue_id, description="issue not found to be deleted")
        current_app.db.session.delete(issue_found)
        current_app.db.session.commit()
        return "", 204
    except NotFound as e:
        return {"error":e.description}, 404
