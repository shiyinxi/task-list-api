from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
import json
from app.routes.route_utilities import validate_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task.from_dict(request_body)
    except:
        response = {"details":"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%")).order_by(Task.id)
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Task.id)
   
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
         
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return task.to_dict()

@bp.put("/<task_id>")
def update_book(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = f"Task #{task_id} successfully updated"
    # return Response(response, status=200, mimetype="application/json")
    return Response(json.dumps(response),status=200, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    response = f"Task #{task_id} successfully deleted"
    return Response(json.dumps(response),status=200, mimetype="application/json")