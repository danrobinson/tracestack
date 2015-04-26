import sys, urllib, webbrowser

def tracestack():
    try:
        last_error = "{0} {1}".format(sys.last_type, sys.last_value)
    except:
        raise Exception("No error message available.")
    error_query = urllib.urlencode({"q": "[python] " + last_error})
    search_url = "http://stackoverflow.com/search?q=" + error_query
    webbrowser.open(search_url)
    
