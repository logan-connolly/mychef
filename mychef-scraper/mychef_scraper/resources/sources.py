import falcon
import msgpack


class Source(object):
    """List all recipe sources that can be scraped."""
    doc = {
        'sources': [
            {
                'id': 1,
                'name': 'The Full Helping',
                'url': 'https://www.thefullhelping.com/recipes/'
            },
            {
                'id': 2,
                'name': 'Food',
                'url': 'https://www.food.com/recipes/'
            }
        ]
    }

    def on_get(self, req, resp, sid):
        source = [s for s in self.doc['sources'] if s.get('id') == sid]
        if source:
            resp.data = msgpack.packb({"source": source}, use_bin_type=True)
        else:
            resp.data = msgpack.packb({"message": "Source not found."})
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200

    def on_get_collection(self, req, resp):
        resp.data = msgpack.packb(self.doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200
