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
            #settings['resource'] = instance on . lower;
            config = context.config.with_package(info.module)

            configurations = [('', '.{format}', 'index', 'GET'),
                              ('_new', '/new.{format}', 'new', 'GET'),
                              ('_create', '/create', 'create', 'POST'),
                              ('_edit', '/{id};edit.{format}', 'edit', 'GET'),
                              ('_show', '/{id}.{format}', 'show', 'GET'),
                              ('_update', '/{id}', 'update', 'POST'),
                              ('_delete', '/{id}', 'delete', 'DELETE')]

            for action in configurations:
                config.add_route(settings['resource']+action[0],
                                 settings['path']+action[1])
                config.add_view(ob,
                                attr=action[2],
                                route_name=settings['resource']+action[0],
                                request_method=action[3])          

            # config.add_route(settings['resource'], settings['path']+'.{format}')
            # config.add_view(ob, attr='index', route_name=settings['resource'])

            # config.add_route(settings['resource']+'_new', settings['path']+'.{format}/new')
            # config.add_view(ob, attr='new', route_name=settings['resource']+'_new')

            # config.add_route(settings['resource']+'_create', settings['path']+'/create')
            # config.add_view(ob, attr='create', route_name=settings['resource']+'_create', request_method='POST')

            # config.add_route(settings['resource']+'_edit', settings['path']+'.{format}/edit/{id}')
            # config.add_view(ob, attr='edit', route_name=settings['resource']+'_edit')

            # config.add_route(settings['resource']+'_update', settings['path']+'/update')
            # config.add_view(ob, attr='update', route_name=settings['resource']+'_update', request_method='POST')

            # config.add_route(settings['resource']+'_delete', settings['path']+'/delete/{id}')
            # config.add_view(ob, attr='delete', route_name=settings['resource']+'_delete')            

            # config.add_route(settings['resource']+'_show', settings['path']+'.{format}/{id}')
            # config.add_view(ob, attr='show', route_name=settings['resource']+'_show')

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
