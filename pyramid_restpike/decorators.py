import venusian

class resource_config(object):

    venusian = venusian

    def __init__(self, **settings):
        #TODO: Check mandatory params
        self.__dict__.update(settings)

    def __call__(self, wrapped):

        settings = self.__dict__.copy()

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_route(settings['resource'], settings['path'])
            config.add_view(ob, attr='index', route_name=settings['resource'])

        info = self.venusian.attach(wrapped, callback)
        return wrapped
