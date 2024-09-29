import argparse
import json
import re
import os
from datetime import date

TASKDIRECTORY = './task/'

TASK_KEY_NR = 'task_id'
TASK_KEY_DATA = 'task_data'
TASK_KEY_STATUS = 'task_status'
TASK_KEY_CREATION_DATE = 'task_creation_date'

TASK_STATUS_TODO = 'todo'
TASK_STATUS_IN_PROGRESS = 'in-progress'
TASK_STATUS_DONE = 'done'
LIST_DEFAULT = 'all'

WRITE_MODE = 'w'
READ_MODE = 'r'
FILE_EXTENSION = '.json'

PRINT_SEPARATOR = '#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#'


def initParser() -> argparse.ArgumentParser:
	"""
	Initialize the argument parser
	:return: argparse.ArgumentParser
	"""
	parser = argparse.ArgumentParser(description='Add, update, remove or show Tasks you added',
	                                 epilog='Project-URL: https://roadmap.sh/projects/task-tracker you should check is out :D')
	parser.add_argument('-a', '-add', nargs='?', metavar='TASK_TEXT', type=addTask, help='Add a task')
	parser.add_argument('-u', '-update', nargs=2, metavar=('TASK_ID', 'NEW_TEXT'), help='Update a task with {ID}')
	parser.add_argument('-d', '-delete', nargs='?', metavar='TASK_ID', type=deleteTask, help='Delete a Task with {ID}')
	parser.add_argument('-md', '-mark-done', nargs='?', metavar='TASK_ID', type=markDone, help='Mark task with {ID} as done')
	parser.add_argument('-mp', '-mark-in-progress', metavar='TASK_ID', type=markInProgress, nargs='?',
	                    help='Mark task with {ID} as in_progress')
	parser.add_argument('-l', '-list', metavar='STATUS_TO_LIST', nargs='?', type=listTasks, const=LIST_DEFAULT,
	                    help='List all tasks, Possible arguments are ' + TASK_STATUS_TODO + ', ' + TASK_STATUS_IN_PROGRESS + ', ' + TASK_STATUS_DONE)
	return parser


def main() -> None:
	"""
	Main Function to read input from STDIN and execute task for output via argparser
	:return: None
	"""
	# Initialize Parser for inputmethods and parse arguments to execute action
	args = initParser().parse_args()

	# need to seperate the update method so we can read all 2 arguments
	if args.u:
		updateTask(*args.u)


def addTask(task) -> None:
	"""
	Creates a task in json format and saves in task folder
	:param task: The Task to add (TEXT)
	:return: None
	"""
	# Create task directory if it doesnt exists
	if not os.path.exists(TASKDIRECTORY):
		try:
			os.makedirs(TASKDIRECTORY)
		except Exception as e:
			print("Count create Directory for tasks, maybe there is a permission error?")
			print(e)
			return

	json_files = getJsonFiles()

	# if there is no json file, then first task
	if not json_files:
		task_nr = 1
	else:
		# Map all files to a new list that matches the RegEx, cast them to int, and get max Number
		task_nr = max(map(int, [file for file in json_files if re.match("^\d+$", file)])) + 1

	task_json = {
		TASK_KEY_NR: task_nr,
		TASK_KEY_DATA: task,
		TASK_KEY_STATUS: TASK_STATUS_TODO,
		TASK_KEY_CREATION_DATE: str(date.today())
	}

	if not save(task_nr, task_json):
		print('Your task couldn\'t be saved')
		return

	print('Task added successfully (ID: ' + str(task_nr) + ')')


def getJsonFiles() -> list:
	# get all files from the directory
	files = os.listdir(TASKDIRECTORY)

	# Listcomprehension to remove .json ending and get only filename (should be numbers)
	return [file[:-5] for file in files if file.endswith(FILE_EXTENSION)]


def save(task_id, task_json) -> bool:
	"""
	Saves the file with given data
	:param task_id: TASK ID
	:param task_json: TASK VALUE FOR FILE (JSON-FORMAT)
	:return: True on success, False otherwise
	"""
	try:
		with open(TASKDIRECTORY + str(task_id) + FILE_EXTENSION, WRITE_MODE) as outfile:
			json.dump(task_json, outfile, indent=4)
	except Exception as e:
		print("Couldnt save Task... Maybe there is a permission error?")
		print(e)
		return False
	return True


def readFileContent(task_id) -> dict:
	"""
	Reads the file content
	:param task_id: TASK ID
	:return: the Task values as DICT
	"""
	try:
		if not check_file_exists(task_id):
			return {}

		with open(TASKDIRECTORY + str(task_id) + FILE_EXTENSION, READ_MODE) as file:
			file_content = json.load(file)
			return file_content

	except Exception as e:
		print(e)
		return {}


def check_file_exists(task_id) -> bool:
	"""
	Checks if a file exists
	:param task_id: TASK ID
	:return: true if file exists, false otherwise
	"""
	return os.path.exists(TASKDIRECTORY + str(task_id) + FILE_EXTENSION)


def updateTask(task_id, text) -> None:
	"""
	Updates the Task text with given text
	:param task_id: TASK ID
	:param text: Text to be updated
	:return: None
	"""
	changeFileValue(task_id, TASK_KEY_DATA, text)


def deleteTask(task_id) -> None:
	"""
	Delte a Task
	:param task_id: TASK ID
	:return: None
	"""
	if not check_file_exists(task_id):
		print('Task doesn\'t exists...')
		return

	os.remove(TASKDIRECTORY + str(task_id) + FILE_EXTENSION)
	if not check_file_exists(task_id):
		print("Task succesfully deleted!")
		return
	print('Failed to delete task!')


def changeFileValue(task_id, task_key, new_task_value) -> None:
	"""
	Change the status of a task
	:param task_id: TASK ID
	:param task_key: Key in file content to update
	:param new_task_value: New value for task_key
	:return: None
	"""
	file_content = readFileContent(task_id)

	# If dict is empty there was probablly and error while reading, stop execution
	if not file_content:
		return

	file_content[task_key] = new_task_value
	if not save(task_id, file_content):
		print('Failed to update task!')

	print('Task successfully updated!')


def markDone(task_id) -> None:
	"""
	Update Task-Status to Done
	:param task_id: TASK ID
	:return: None
	"""
	changeFileValue(task_id, TASK_KEY_STATUS, TASK_STATUS_DONE)


def markInProgress(task_id) -> None:
	"""
	Update Task-Status to In Progress
	:param task_id: TASK ID
	:return: None
	"""
	changeFileValue(task_id, TASK_KEY_STATUS, TASK_STATUS_IN_PROGRESS)


def listTasks(task) -> None:
	"""
	List all task, if a argument is provided List all task with the given argument
	:return:
	"""
	list_cases = {TASK_STATUS_DONE: listDone,
	              TASK_STATUS_TODO: listToDo,
	              TASK_STATUS_IN_PROGRESS: listInProgress,
	              LIST_DEFAULT: listAll}

	# execute function where specific argument got passed
	if task in list_cases:
		list_cases[task]()


def printTasks(status='') -> None:
	if not os.path.exists(TASKDIRECTORY):
		print('No tasks found')
		return

	tasks = getJsonFiles()

	if status:
		tasks = [task for task in tasks if readFileContent(task)[TASK_KEY_STATUS] == status]

	for task in tasks:
		print(f"ID: {readFileContent(task)[TASK_KEY_NR]}\nTASK: {readFileContent(task)[TASK_KEY_DATA]}")
		print(PRINT_SEPARATOR)


def listAll() -> None:
	"""
	Prints all tasks
	:return: None
	"""
	printTasks()


def listDone() -> None:
	"""
	Prints all Tasks with Status done
	:return: None
	"""
	printTasks(TASK_STATUS_DONE)


def listToDo() -> None:
	"""
	Prints all Tasks with Status to-do
	:return: None
	"""
	printTasks(TASK_STATUS_TODO)


def listInProgress() -> None:
	"""
	Prints all Tasks with Status in progress
	:return: None
	"""
	printTasks(TASK_STATUS_IN_PROGRESS)


if __name__ == "__main__":
	main()
