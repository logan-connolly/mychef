import falcon

from resources.sources import SourceList

api = falcon.API()

sources = SourceList()
api.add_route('/sources', sources)
