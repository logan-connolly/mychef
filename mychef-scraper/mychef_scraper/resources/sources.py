import json
import falcon


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
            resp.body = json.dumps(source[0])
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"message": "source not found."})
            resp.status = falcon.HTTP_404

    def on_get_collection(self, req, resp):
        resp.body = json.dumps(self.doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        pass
