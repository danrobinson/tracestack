try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class Engine(object):
    """Object that generates a search URL based on an error
    message, for a given engine."""

    def __init__(self, *args, **kwargs):
        self.additional_terms = []
        self.keywords = ["python"]

    def search(self, error_string):
        error_arguments = self.query_args(error_string)
        error_query = urlencode(error_arguments)
        search_url = self.base_url + error_query
        return search_url

    def query_words(self, error_text):
        return [error_text] + self.keywords + self.additional_terms

    def query_args(self, error_text):
        return {"q": " ".join(self.query_words(error_text))}

class GoogleEngine(Engine):

    base_url = "http://www.google.com/search?"

    def __init__(self, *args, **kwargs):
        super(GoogleEngine, self).__init__(*args, **kwargs)
        if kwargs["engine"] == "default":
            self.additional_terms.append("site:stackoverflow.com")
            self.additional_terms.append("inurl:questions")

    def name(self):
        if "site:stackoverflow.com" in self.additional_terms:
            return "Stack Overflow (using Google)"
        else:
            return "the web (using Google)"

class StackEngine(Engine):

    base_url = "http://www.stackoverflow.com/search?"

    def name(self):
        return "Stack Overflow"

    def query_words(self, error_text):
        bracketed_keywords = ["[%s]" % kw for kw in self.keywords]
        return [error_text] + bracketed_keywords + self.additional_terms

