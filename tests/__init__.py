from pyramid import testing

class DummyVenusianInfo(object):
    module = None

class DummyVenusian(object):
    def __init__(self):
        info = DummyVenusianInfo()
        self.info = info
        self.attachments = []

    def attach(self, wrapped, callback, category=None, depth=1):
        self.attachments.append((wrapped, callback, category))
        self.depth = depth
        return self.info

class DummyRegistry(object):
    pass

class DummyVenusianContext(object):
    def __init__(self):
        self.config = testing.setUp()

def call_venusian(venusian):
    context = DummyVenusianContext()
    for wrapped, callback, category in venusian.attachments:
        callback(context, None, wrapped)
    return context.config
