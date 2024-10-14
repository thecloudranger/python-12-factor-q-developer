# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for tasks (we'll replace this with a database later)
tasks = []


@app.route("/")
def hello():
    return "Welcome to the Task Management App!"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.json.get("task")
    if task:
        new_task = {"id": len(tasks) + 1, "task": task, "completed": False}
        tasks.append(new_task)
        return jsonify(new_task), 201
    return jsonify({"error": "Invalid task"}), 400


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        task["completed"] = request.json.get("completed", task["completed"])
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
