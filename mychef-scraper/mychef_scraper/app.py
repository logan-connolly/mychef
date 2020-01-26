import falcon

from resources.sources import Source


api = falcon.API()

source = Source()
api.add_route('/source/{sid:int}', source)
api.add_route('/sources', source, suffix='collection')
