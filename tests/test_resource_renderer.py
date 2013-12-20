from nose.tools import assert_true, assert_equals
from pyramid.testing import DummyRequest
from pyramid.response import Response

class SUTResource(object):

    def __init__(self):
        self.request = DummyRequest()

    def index(self):
        return {}

class TestResourceRenderer(object):

    def _getTargetClass(self):
        from pyramid_restpike import resource_renderer
        return resource_renderer

    def _makeOne(self, *arg, **kw):
        decorator = self._getTargetClass()(*arg, **kw)
        class SUTResource(object):
            @decorator
            def index(self):
                return {}
        sut = SUTResource()
        sut.request = DummyRequest()
        return sut

    def test_default_renderer(self):
        sut = self._makeOne('json')
        response = sut.index()
        assert_true(isinstance(response, Response))
