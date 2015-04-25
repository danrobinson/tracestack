import sys, urllib, webbrowser

def tracestack():
    last_error = sys.last_value
    if not last_error:
        raise Exception("No error message available.")
    error_query = urllib.encode("[python] " + str(last_error))
    search_url = "http://stackoverflow.com/search?q=" + error_query
    webbrowser.open(search_url)
    
