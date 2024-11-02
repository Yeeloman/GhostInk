from Taskara import Taskara

task_manager = Taskara()

task_manager.add_task("Initial setup", mode=Taskara.mode.TODO)
task_manager.ln("Setting up database connection")

# Simulate an error condition
try:
    # some code that raises an exception
    raise Exception("Simulated error")
except Exception:
    task_manager.add_task("Error occurred", mode=Taskara.mode.ERROR)

# Print all tasks
task_manager.print()
