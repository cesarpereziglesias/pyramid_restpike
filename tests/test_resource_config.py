from nose.tools import assert_true, assert_equals

from . import DummyVenusian, call_venusian

class TestResourceConfig(object):

    def _getTargetClass(self):
        from pyramid_restpike import resource_config
        return resource_config

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def _get_config(self, decorator):
        venusian = DummyVenusian()
        decorator.venusian = venusian

        class SUTResource(object):
            pass

        wrapped = decorator(SUTResource)
        assert_true(wrapped is SUTResource)
        return call_venusian(venusian)


    def _test_routes(self, prefix, routes):
        assert_true(prefix in routes)
        assert_true(prefix + '_list' in routes)
        assert_true(prefix + '_new' in routes)
        assert_true(prefix + '_edit' in routes)
        assert_true(prefix + '_show' in routes)
        assert_true(prefix + '_id' in routes)


    def test_routes(self):
        decorator = self._makeOne(resource='mysutresource', path='/sut')
        config = self._get_config(decorator)

        mapper = config.get_routes_mapper()
        self._test_routes('mysutresource', mapper.routes)


    def test_routes_by_class_name(self):
        decorator = self._makeOne(path='/sut')
        config = self._get_config(decorator)

        mapper = config.get_routes_mapper()
        self._test_routes('sutresource', mapper.routes)


    def test_paths(self):
        decorator = self._makeOne(resource='sut', path='/sut')
        config = self._get_config(decorator)

        mapper = config.get_routes_mapper()
        assert_equals('/sut', mapper.routes['sut'].path)
        assert_equals('/sut.{format}', mapper.routes['sut_list'].path)
        assert_equals('/sut/new', mapper.routes['sut_new'].path)
        assert_equals('/sut/{id};edit', mapper.routes['sut_edit'].path)
        assert_equals('/sut/{id}.{format}', mapper.routes['sut_show'].path)
        assert_equals('/sut/{id}', mapper.routes['sut_id'].path)
