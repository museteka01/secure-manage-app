from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "name": "Do laundry"},
    {"id": 2, "name": "Write report"}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return {"error": "Task not found"}, 404

@app.route('/')
def home():
    return "Welcome to the Secure App Manager API!"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
