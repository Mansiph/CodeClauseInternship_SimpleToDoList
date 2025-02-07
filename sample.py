import tkinter as tk
from tkinter import messagebox, Scrollbar
import json

class SimpleToDoList:
    def __init__(self, root):
        self.tasks = []
        self.root = root
        self.root.title("To-Do List")
        self.load_tasks()
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.task_entry = tk.Entry(self.frame, width=40, font=("Arial", 14))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task, font=("Arial", 12))
        self.add_button.pack(side=tk.RIGHT)
        
        self.listbox_frame = tk.Frame(root)
        self.listbox_frame.pack()
        
        self.listbox = tk.Listbox(self.listbox_frame, width=50, height=10, font=("Arial", 12))
        self.listbox.pack(side=tk.LEFT, padx=5)
        
        self.scrollbar = Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.complete_button = tk.Button(root, text="Mark Completed", command=self.mark_completed, font=("Arial", 12))
        self.complete_button.pack(pady=5)
        
        self.remove_button = tk.Button(root, text="Remove Completed", command=self.remove_completed, font=("Arial", 12))
        self.remove_button.pack(pady=5)
        
        self.populate_listbox()
    
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.populate_listbox()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def mark_completed(self):
        try:
            selected_index = self.listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.save_tasks()
            self.populate_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")
    
    def remove_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        self.populate_listbox()
    
    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[Completed]" if task["completed"] else "[Pending]"
            self.listbox.insert(tk.END, f"{status} {task['task']}")
    
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleToDoList(root)
    root.mainloop()
