from pyramid import testing
from pyramid_restpike import resource_config

class TestResourceConfig(object):

    def setup(self):
        self.config = testing.setUp()

    def test_pass(self):

        @resource_config(resource='sut', path='/sut')
        class SUTResource(object):

            def index(self):
                pass

        self.config.scan()
