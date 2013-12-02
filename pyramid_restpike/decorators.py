import venusian

from pyramid.response import Response
from pyramid.renderers import render

class resource_config(object):

    venusian = venusian

    def __init__(self, **settings):
        #TODO: Check mandatory params
        self.__dict__.update(settings)

    def __call__(self, wrapped):

        settings = self.__dict__.copy()

        def callback(context, name, ob):
            settings['resource'] = instance on . lower;
            config = context.config.with_package(info.module)
            config.add_route(settings['resource'], settings['path']+'.{format}')
            config.add_view(ob, attr='index', route_name=settings['resource'])

        info = self.venusian.attach(wrapped, callback)
        return wrapped


class resource_renderer(object):
    _default_format = 'json'

    def __init__(self, **renderers):
        self._renderers = renderers

    def _check_format(self, format_):
        return format_ in self._renderers

    def __call__(self, wrapped):
        def callback(resource):
            format_ = resource.request.matchdict['format']
            if self._check_format(format_):
                return Response(render(self._renderers[format_], wrapped(resource), request=resource.request))
            #else: //Throw 404 error

        return callback
