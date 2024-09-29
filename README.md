Project-URL = https://roadmap.sh/projects/task-tracker

# Task Tracker CLI
1. Give execution permissions to the setupTaskTracker.sh script using the command <code>chmod +x setupTaskTracker.sh</code>
2. Run the script using the command <code>./setupTaskTracker.sh</code>
<blockquote>On windows execute the setupTaskTracker.ps1 PowerShell Script</blockquote>

There is also a -h command to display some informations to help in using the script

# Adding a new task
task-cli add "Buy groceries"<br>
Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"<br>
task-cli delete 1

# Marking a task as in progress or done
task-cli mark-in-progress 1<br>
task-cli mark-done 1

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done<br>
task-cli list todo<br>
task-cli list in-progress