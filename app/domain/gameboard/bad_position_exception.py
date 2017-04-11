class BadPositionException(Exception):
    def __init__(self, x, y):
        message = "Bad position given : " + str(x) + " y : " + str(y)
        Exception.__init__(self, message)
