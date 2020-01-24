import json

import falcon


class SourceList(object):
    """List all recipe sources that can be scraped."""

    def on_get(self, req, resp):
        doc = {
            'sources': [
                {
                    'name': 'The Full Helping',
                    'url': 'https://www.thefullhelping.com/recipes/'
                }
            ]
        }
        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200
