#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

TRACK_FILE = 'track.json'

def load_tasks():
    if not os.path.exists(TRACK_FILE):
        return []

    with open(TRACK_FILE,"r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_task(tasks):
    with open(TRACK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def generate_id(tasks):
    dictionary = load_tasks()
    if not tasks:
        return 1
    return (tasks[-1]["id"]) + 1

def add_task(task):
    tasks = load_tasks()
    dictionary = {
        "id": generate_id(tasks),
        "description": task,
        "status": "todo",
        "createdAt": datetime.today().isoformat(),
        "updatedAt": datetime.today().isoformat()
    }
    tasks.append(dictionary)
    save_task(tasks)
    
    print(f"Task added successfully ID: {dictionary['id']}")

def delete_task(id):
    try:
        id = int(id)
    except ValueError:
        print("ID must be an integer")
        return

    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != id]

    if len(new_tasks) == len(tasks):
        print("Invalid ID")
        return

    save_task(new_tasks)
    print(f"Task ({id}) deleted succesfully")    

def update_task(id, updated_task):
    try:
        id = int(id)
    except ValueError:
        print("ID must be an integer")
        return

    tasks = load_tasks()
    found = False

    for task in tasks:
        if id == task["id"]:
            task["description"] = updated_task
            task["updatedAt"] = datetime.today().isoformat()
            found = True
            break
    
    if found:
        save_task(tasks)
        print(f"Task ({id}) updated successfully")
    else:
        print("Invalid ID")
            
def list_task():
    pass

def task_status():
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input action',nargs='+')

    args = parser.parse_args()
    inputs = args.input
    
    action = inputs[0]

    if action == "add" and len(inputs) >= 2:
        task = ' '.join(inputs[1:])
        add_task(task)

    elif action == "delete" and len(inputs) == 2:
        task_id = inputs[1]
        delete_task(task_id)

    elif action == "update" and len(inputs) >= 3:
        task_id = inputs[1]
        updated_task = ' '.join(inputs[2:])
        update_task(task_id, updated_task)

    else:
        print("Usage:")
        print("  add <task description>")
        print("  delete <task id>")
        print("  update <task id> <new description>")
        
if __name__ == "__main__":
    main()