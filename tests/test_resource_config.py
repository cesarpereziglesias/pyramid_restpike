from nose.tools import assert_true, assert_equals

from . import DummyVenusian, call_venusian

class TestResourceConfig(object):

    def _getTargetClass(self):
        from pyramid_restpike import resource_config
        return resource_config

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def test_pass(self):

        decorator = self._makeOne(path='/sut')
        venusian = DummyVenusian()
        decorator.venusian = venusian

        class SUTResource(object):

            def index(self):
                pass

        wrapped = decorator(SUTResource)
        assert_true(wrapped is SUTResource)
        config = call_venusian(venusian)

        # TODO: Check view_callable
