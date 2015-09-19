import unittest
import sys
import tracestack
import webbrowser

try:
	from mock import Mock, patch
except ImportError:
	from unittest.mock import Mock, patch

exc_return_value = (type(Exception("exception message")), Exception("exception message"), Mock())
mock_sys_exc_info = Mock(return_value=exc_return_value)
mock_webbrowser = Mock()
mock_traceback_print_exception = Mock()
mock_getch = Mock(return_value=" ")


@patch('tracestack.handler.sys.exc_info', mock_sys_exc_info)
@patch('tracestack.handler.webbrowser', mock_webbrowser)
@patch('tracestack.handler.traceback.print_exception', mock_traceback_print_exception)
@patch('tracestack.handler.getch', mock_getch)
class TestHandler(unittest.TestCase):

	default_url = 		('http://www.google.com/search?q=Exception%3A' + 
						 '+exception+message%0A+python+site%3Astackoverflow.com' +
						 '+inurl%3Aquestions')
	google_url = 		('http://www.google.com/search?q=Exception%3A' + 
						 '+exception+message%0A+python')
	stackoverflow_url = ('http://www.stackoverflow.com/search?' + 
						 'q=Exception%3A+exception+message%0A+%5Bpython%5D')
	default_prompt = 	   'Hit spacebar to search this error message on Stack Overflow (using Google): '
	google_prompt =		   'Hit spacebar to search this error message on the web (using Google): '
	stackoverflow_prompt = 'Hit spacebar to search this error message on Stack Overflow: '

	def setUp(self):
		pass

	def tearDown(self):
		mock_sys_exc_info.reset_mock()
		mock_webbrowser.reset_mock()
		mock_traceback_print_exception.reset_mock()
		mock_getch.reset_mock()

	def test_default(self):
		handler = tracestack.handler.ExceptionHandler()
		handler()
		self.check_results()

	def test_skip(self):
		handler = tracestack.handler.ExceptionHandler(skip=True)
		handler()
		self.skip=True
		self.check_results(skip=True)

	def test_google(self):
		handler = tracestack.handler.ExceptionHandler(engine="google")
		handler()
		self.check_results(prompt=self.google_prompt, url=self.google_url)

	def test_stackoverflow(self):
		handler = tracestack.handler.ExceptionHandler(engine="stackoverflow")
		handler()
		self.check_results(prompt=self.stackoverflow_prompt, url=self.stackoverflow_url)

	def check_results(self, skip=False, prompt=None, 
					  url=None):
		prompt = prompt or self.default_prompt
		url = url or self.default_url
		mock_sys_exc_info.assert_called_once_with()
		mock_traceback_print_exception.assert_called_once_with(*exc_return_value)
		if skip:
			mock_getch.assert_not_called()
		else:
			mock_getch.assert_called_with(prompt)
		mock_webbrowser.open.assert_called_once_with(url)

	def test_pm(self):
		tracestack.pm()
		self.check_results()

	def test_nothing(self):
		with self.assertRaises(AssertionError):
			self.check_results()		


class TestFunctions(unittest.TestCase):

	def test_enable(self):
		tracestack.enable()
		self.assertIsNot(sys.excepthook, sys.__excepthook__)
		self.assertTrue(isinstance(sys.excepthook, 
								   tracestack.handler.ExceptionHandler))
		tracestack.disable()
		self.assertIs(sys.excepthook, sys.__excepthook__)

	def test_decorator(self):
		@tracestack.trace
		def buggy_function():
			self.assertIsNot(sys.excepthook, sys.__excepthook__)
			self.assertTrue(isinstance(sys.excepthook, 
									   tracestack.handler.ExceptionHandler))
		buggy_function()
		self.assertIs(sys.excepthook, sys.__excepthook__)


