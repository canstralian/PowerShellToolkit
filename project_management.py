import uuid
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description, due_date, assigned_to=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_to = assigned_to
        self.status = "Not Started"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_status(self, new_status):
        self.status = new_status
        self.updated_at = datetime.now()

class Project:
    def __init__(self, name, description):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tasks = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_task(self, task):
        self.tasks.append(task)
        self.updated_at = datetime.now()

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.updated_at = datetime.now()

    def get_task(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

class ProjectManagement:
    def __init__(self):
        self.projects = []

    def create_project(self, name, description):
        project = Project(name, description)
        self.projects.append(project)
        return project

    def get_project(self, project_id):
        return next((project for project in self.projects if project.id == project_id), None)

    def create_task(self, project_id, title, description, due_date, assigned_to=None):
        project = self.get_project(project_id)
        if project:
            task = Task(title, description, due_date, assigned_to)
            project.add_task(task)
            return task
        return None

    def update_task_status(self, project_id, task_id, new_status):
        project = self.get_project(project_id)
        if project:
            task = project.get_task(task_id)
            if task:
                task.update_status(new_status)
                return True
        return False

    def get_project_tasks(self, project_id):
        project = self.get_project(project_id)
        return project.tasks if project else []

    def get_overdue_tasks(self):
        overdue_tasks = []
        for project in self.projects:
            overdue_tasks.extend([task for task in project.tasks if task.due_date < datetime.now() and task.status != "Completed"])
        return overdue_tasks

# Example usage
if __name__ == "__main__":
    pm = ProjectManagement()
    
    # Create a project
    project = pm.create_project("Website Redesign", "Redesign the company website")
    
    # Create tasks
    task1 = pm.create_task(project.id, "Design mockups", "Create initial design mockups", datetime.now() + timedelta(days=7), "Designer")
    task2 = pm.create_task(project.id, "Develop frontend", "Implement the frontend based on mockups", datetime.now() + timedelta(days=14), "Frontend Developer")
    
    # Update task status
    pm.update_task_status(project.id, task1.id, "In Progress")
    
    # Get project tasks
    project_tasks = pm.get_project_tasks(project.id)
    print(f"Project '{project.name}' tasks:")
    for task in project_tasks:
        print(f"- {task.title} ({task.status})")
    
    # Get overdue tasks
    overdue_tasks = pm.get_overdue_tasks()
    print("\nOverdue tasks:")
    for task in overdue_tasks:
        print(f"- {task.title} (Due: {task.due_date})")
