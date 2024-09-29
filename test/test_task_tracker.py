import argparse
import os.path
import unittest
import task_tracker

class TestTaskTracker(unittest.TestCase):

	def testParser(self):
		parser = task_tracker.initParser()
		self.assertIsNotNone( parser, 'The Parser is not null')
		self.assertEqual( parser.__class__.__name__, argparse.ArgumentParser().__class__.__name__, 'Parser is not the parser Object we expect')

	def testCheckForFile(self):
		result = task_tracker.check_file_exists(0)
		self.assertFalse(result, 'File does not exist')

	def testgetJsonFiles(self):
		if os.path.exists(task_tracker.TASKDIRECTORY):
			result = task_tracker.getJsonFiles()
			[self.assertTrue(file, list) for file in result]
			self.assertIsNotNone(result, 'List of tasks is not null')
			self.assertIsInstance(result, list, 'List of tasks is not a list')

	def testAddAndRemoveTask(self):
		self.assertIsNone(task_tracker.addTask('test'))
		self.assertTrue(task_tracker.check_file_exists(1))

		self.assertIsNone(task_tracker.deleteTask(1))
		self.assertFalse(task_tracker.check_file_exists(1))

	def testCheckFileExists(self):
		self.assertFalse(task_tracker.check_file_exists(0), "File does not exist")

		if os.path.exists(task_tracker.TASKDIRECTORY + '1.json'):
			self.assertTrue(task_tracker.check_file_exists(1), "File exists")

	def testUpdateTask(self):
		task_tracker.addTask('another Test')

		if task_tracker.check_file_exists(1):
			file_content = task_tracker.readFileContent(1)

			task_tracker.updateTask(1, "updated")
			file_content_new = task_tracker.readFileContent(1)
			self.assertNotEqual(file_content[task_tracker.TASK_KEY_DATA], file_content_new[task_tracker.TASK_KEY_DATA], "File content does not match")
			self.assertEqual(file_content[task_tracker.TASK_KEY_NR], file_content_new[task_tracker.TASK_KEY_NR], "TaskID is not the same after update")

			task_tracker.deleteTask(1)
			self.assertTrue(not task_tracker.check_file_exists(1))

	def testMarkDone(self):
		task_tracker.addTask('another Test')
		if task_tracker.check_file_exists(1):
			file_content = task_tracker.readFileContent(1)

			task_tracker.markDone(1)
			file_content_new = task_tracker.readFileContent(1)
			self.assertNotEqual(file_content[task_tracker.TASK_KEY_STATUS], file_content_new[task_tracker.TASK_KEY_STATUS], "File Status didnt update")
			self.assertEqual(file_content_new[task_tracker.TASK_KEY_STATUS], task_tracker.TASK_STATUS_DONE)

			task_tracker.deleteTask(1)

	def testMarkInProgress(self):
		task_tracker.addTask('another Test')
		if task_tracker.check_file_exists(1):
			file_content = task_tracker.readFileContent(1)

			task_tracker.markInProgress(1)
			file_content_new = task_tracker.readFileContent(1)
			self.assertNotEqual(file_content[task_tracker.TASK_KEY_STATUS],
			                    file_content_new[task_tracker.TASK_KEY_STATUS], "File Status didnt update")
			self.assertEqual(file_content_new[task_tracker.TASK_KEY_STATUS], task_tracker.TASK_STATUS_IN_PROGRESS)

			task_tracker.deleteTask(1)




