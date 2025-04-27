from flask import Flask, request, render_template, jsonify

'''
    It creates an instance of the Flask class,
    which will be your WSGI (Web Server Gateway Interface) application.
'''

app = Flask(__name__)

toDoList = [
    {
      "id": 1,
      "task": "Buy groceries",
      "completed": False
    },
    {
      "id": 2,
      "task": "Finish homework",
      "completed": False
    },
    {
      "id": 3,
      "task": "Call mom",
      "completed": True
    },
    {
      "id": 4,
      "task": "Clean the house",
      "completed": False
    },
    {
      "id": 5,
      "task": "Schedule dentist appointment",
      "completed": True
    },
    {
      "id": 6,
      "task": "Prepare for the meeting",
      "completed": False
    },
    {
      "id": 7,
      "task": "Walk the dog",
      "completed": True
    },
    {
      "id": 8,
      "task": "Read a chapter from the book",
      "completed": False
    },
    {
      "id": 9,
      "task": "Buy birthday gift for Sarah",
      "completed": False
    },
    {
      "id": 10,
      "task": "Do laundry",
      "completed": True
    }
  ]

@app.route("/")
def home():
    return "Welcome to Sample ToDO List App"

@app.route("/items", methods=['GET'])
def get_itemList():
    return jsonify(toDoList)

# GET
@app.route("/items/<int:item_id>", methods=['GET'])
def get_item(item_id):
    item = next((item for item in toDoList if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "item not found"})
    return jsonify(item)

# POST
@app.route("/items", methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"error": "item not found"})
    new_item = {
        "id":toDoList[-1]['id'] + 1 if toDoList else 1,
        "task": request.json['task'],
        "completed": request.json['completed']
    }
    toDoList.append(new_item)
    return jsonify(new_item)

# PUT
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in toDoList if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "item not found"})
    item['task'] = request.json.get('task', item['task'])
    return jsonify(item)


# DELETE
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global toDoList
    toDoList = [item for item in toDoList if item["id"] != item_id]
    return jsonify({"result": "Item Deleted"})
    
if __name__ == "__main__":
    app.run(debug=True)
