from HTMLParser import HTMLParser

class HTMLStripper(HTMLParser):
    """
    Class that cleans HTML, removing all tags and HTML entities.
    """
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    def strip(self, d):
        self.reset()
        self.fed = []
        self.feed(d)
        return self.get_data().strip()

