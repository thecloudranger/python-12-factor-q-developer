# app.py
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
logging.basicConfig(level=app.config["LOG_LEVEL"])
logger = logging.getLogger(__name__)

# Set up database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task, "completed": self.completed}


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def hello():
    logger.info("Hello endpoint accessed")
    return "Welcome to the Task Management App!"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    logger.info("Fetching all tasks")
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "task" not in data:
        logger.warning("Invalid task data received")
        return jsonify({"error": "Invalid task data"}), 400

    task_description = data["task"]
    if not isinstance(task_description, str) or len(task_description) == 0:
        logger.warning("Invalid task description")
        return jsonify({"error": "Invalid task description"}), 400

    new_task = Task(task=task_description)
    db.session.add(new_task)
    db.session.commit()
    logger.info(f"New task added: {new_task.to_dict()}")
    return jsonify(new_task.to_dict()), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data or "completed" not in data:
        logger.warning("Invalid update data received")
        return jsonify({"error": "Invalid update data"}), 400

    task.completed = bool(data["completed"])
    db.session.commit()
    logger.info(f"Task updated: {task.to_dict()}")
    return jsonify(task.to_dict())


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    logger.info(f"Task deleted: {task_id}")
    return "", 204


def init_db():
    try:
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        if not inspector.has_table(Task.__tablename__):
            db.create_all()
            logger.info(f"Created table {Task.__tablename__}")
        else:
            logger.info(f"Table {Task.__tablename__} already exists")
    except Exception as e:
        logger.error(f"An error occurred during database initialization: {str(e)}")


with app.app_context():
    init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    app.run(debug=True)
