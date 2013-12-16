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
            config = context.config.with_package(info.module)

            route = settings.get('resource', ob.__name__.lower())
            route_list = route + '_list'
            route_new = route + '_new'
            route_edit = route + '_edit'
            route_show = route + '_show'
            route_id = route + '_id'

            path = settings['path']

            routes = (
                (route, path + ''),
                (route_list, path + '.{format}'),
                (route_new, path + '/new'),
                (route_edit, path + '/{id};edit'),
                (route_show, path + '/{id}.{format}'),
                (route_id, path + '/{id}'),
            )

            [config.add_route(*route_args) for route_args in routes]

            views = (
                {'route_name': route, 'attr': 'create', 'request_method': 'POST'},
                {'route_name': route_list, 'attr': 'index', 'request_method': 'GET'},
                {'route_name': route_new, 'attr': 'new', 'request_method': 'GET'},
                {'route_name': route_show, 'attr': 'show', 'request_method': 'GET'},
                {'route_name': route_id, 'attr': 'update', 'request_method': 'PUT'},
                {'route_name': route_id, 'attr': 'delete', 'request_method': 'DELETE'},
                {'route_name': route_edit, 'attr': 'edit', 'request_method': 'GET'}
            )

            [config.add_view(ob, **key_view_config_args)
                for key_view_config_args in views]

        info = self.venusian.attach(wrapped, callback)
        return wrapped


class resource_renderer(object):

    def __init__(self, *default, **renderers):
        if len(default) > 1:
            raise Exception('*args can be greater than 1')

        self._default = None if len(default) == 0 else default[0]
        self._renderers = renderers

    def _check_format(self, format_):
        return format_ in self._renderers

    def __call__(self, wrapped):
        def callback(resource):
            format_ = resource.request.matchdict.get('format', None)
            renderer = self._renderers[format_] if format_ is not None else self._default

            if renderer is not None:
                return Response(render(renderer, wrapped(resource), request=resource.request))
            #else: //Throw 404 error

        return callback
