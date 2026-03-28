import os
from langchain_community.tools.file_management import WriteFileTool, ReadFileTool

class ToDoMiddleware:
    def __init__(self, todo_file="ToDo.md"):
        self.todo_file = todo_file
        # Using basic LangChain tools for consistency if needed later
        self.writer = WriteFileTool()
        self.reader = ReadFileTool()

    def add_task(self, task):
        current_todo = self.read_todo()
        new_todo = current_todo + f"\n- [ ] {task}"
        self.write_todo(new_todo)
        print(f"To-Do Update: Added task '{task}'")

    def complete_task(self, task_keyword):
        current_todo = self.read_todo()
        # Simple string replacement for [ ] to [X]
        lines = current_todo.split("\n")
        new_lines = []
        for line in lines:
            if task_keyword.lower() in line.lower() and "[ ]" in line:
                line = line.replace("[ ]", "[X]")
                print(f"To-Do Update: Completed task matching '{task_keyword}'")
            new_lines.append(line)
        self.write_todo("\n".join(new_lines))

    def read_todo(self):
        if not os.path.exists(self.todo_file):
            return "# To-Do List"
        with open(self.todo_file, "r") as f:
            return f.read()

    def write_todo(self, content):
        with open(self.todo_file, "w") as f:
            f.write(content)

if __name__ == "__main__":
    todo = ToDoMiddleware()
    # todo.add_task("Verify LangChain middleware")
    # todo.complete_task("Verify")
