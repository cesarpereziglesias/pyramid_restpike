from nose.tools import assert_true, assert_equals

from . import DummyVenusian, call_venusian

class TestResourceConfig(object):

    def _getTargetClass(self):
        from pyramid_restpike import resource_config
        return resource_config

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def _test_routes(self, prefix, routes):
        assert_true(prefix in routes)
        assert_true(prefix + '_list' in routes)
        assert_true(prefix + '_new' in routes)
        assert_true(prefix + '_edit' in routes)
        assert_true(prefix + '_show' in routes)
        assert_true(prefix + '_id' in routes)


    def test_check_routes(self):
        decorator = self._makeOne(resource='mysutresource', path='/sut')
        venusian = DummyVenusian()
        decorator.venusian = venusian

        class SUTResource(object):
            pass

        wrapped = decorator(SUTResource)
        assert_true(wrapped is SUTResource)
        config = call_venusian(venusian)

        mapper = config.get_routes_mapper()
        self._test_routes('mysutresource', mapper.routes)


    def test_check_routes_by_class_name(self):
        decorator = self._makeOne(path='/sut')
        venusian = DummyVenusian()
        decorator.venusian = venusian

        class SUTResource(object):
            pass

        wrapped = decorator(SUTResource)
        assert_true(wrapped is SUTResource)
        config = call_venusian(venusian)

        mapper = config.get_routes_mapper()
        self._test_routes('sutresource', mapper.routes)
