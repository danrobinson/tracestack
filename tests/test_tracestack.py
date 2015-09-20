import unittest
import sys
import tracestack
import webbrowser
try:
	from mock import Mock, patch
except ImportError:
	from unittest.mock import Mock, patch

exc_return_value = (type(Exception('exception message')), Exception('exception message'), Mock())
mock_sys_exc_info = Mock(return_value=exc_return_value)
mock_webbrowser = Mock()
mock_traceback_print_exception = Mock()
mock_getch = Mock(return_value=' ')
mock_sys = Mock()
mock_sys.last_type = exc_return_value[0]
mock_sys.last_value = exc_return_value[1]
mock_sys.last_traceback = exc_return_value[2]
mock_print = Mock()


@patch('tracestack.handler.sys.exc_info', mock_sys_exc_info)
@patch('tracestack.handler.webbrowser', mock_webbrowser)
@patch('tracestack.handler.traceback.print_exception', mock_traceback_print_exception)
@patch('tracestack.handler.getch', mock_getch)
@patch('tracestack.handler.print', mock_print)
class TestHandler(unittest.TestCase):

	default_details = {
		'url': ('http://www.google.com/search?q=Exception%3A' + 
			  '+exception+message%0A+python+site%3Astackoverflow.com' +
			  '+inurl%3Aquestions'),
		'message': ('Searching this error message on Stack Overflow ' + 
			   	  '(using Google)...'),
		'prompt_message': ('Hit spacebar to search this error ' + 
			   			 'message on Stack Overflow (using Google): ')
	}

	google_details = {
		'url': ('http://www.google.com/search?q=Exception%3A' + 
			  '+exception+message%0A+python'),
		'message': ('Searching this error message on the web (using Google)...'),
		'prompt_message': ('Hit spacebar to search this error message ' +
			   			 'on the web (using Google): ')
		}

	stackoverflow_details = {
		'url': ('http://www.stackoverflow.com/search?' + 
			  'q=Exception%3A+exception+message%0A+%5Bpython%5D'),
		'message':'Searching this error message on Stack Overflow...',
		'prompt_message':'Hit spacebar to search this error message on Stack Overflow: '
	}


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

	def test_default_prompt(self):
		handler = tracestack.handler.ExceptionHandler(prompt=True)
		handler()
		self.check_results(prompt=True)

	def test_google(self):
		handler = tracestack.handler.ExceptionHandler(engine='google')
		handler()
		self.check_results(engine_details=self.google_details)

	def test_google_prompt(self):
		handler = tracestack.handler.ExceptionHandler(engine='google', 
													  prompt=True)
		handler()
		self.check_results(engine_details=self.google_details, prompt=True)

	def test_stackoverflow(self):
		handler = tracestack.handler.ExceptionHandler(engine='stackoverflow')
		handler()
		self.check_results(engine_details=self.stackoverflow_details)

	def test_stackoverflow_prompt(self):
		handler = tracestack.handler.ExceptionHandler(engine='stackoverflow',
													  prompt=True)
		handler()
		self.check_results(engine_details=self.stackoverflow_details, prompt=True)

	def check_results(self, engine_details=None, prompt=False):
		engine_details = engine_details or self.default_details
		mock_traceback_print_exception.assert_called_once_with(*exc_return_value)
		if prompt:
			mock_print.assert_called_with(engine_details['prompt_message'], end='')
		else:
			mock_print.assert_called_with(engine_details['message'])
		mock_webbrowser.open.assert_called_once_with(engine_details['url'])

	@patch('tracestack.debugger.sys', mock_sys)
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


