
class NbaStats:

    def __init__(self, response):
        self.response = response

    def getColumnIndex(self, columnName):
        return self.response['resultSets'][0]['headers'].index(columnName)

    def getRows(self):
        return self.response['resultSets'][0]['rowSet']