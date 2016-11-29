from collections import OrderedDict
from flask.views import MethodView
from ..app import app
from ..facilities import make_json_response
from ..app import logger
import logging


class ActionList(MethodView):
    def get(self):
        response_dict = OrderedDict()

        for rule in app.url_map.iter_rules():
            endpoint = rule.endpoint.rsplit('.', 1)[-1]

            if endpoint == 'static' or endpoint.startswith('action_'):
                continue

            if 'GET' in rule.methods:
                response_dict[endpoint+'_get'] = OrderedDict([
                    ('path', rule.rule),
                    ('method', 'GET')
                    ])
            if 'POST' in rule.methods:
                response_dict[endpoint+'_create'] = OrderedDict([
                    ('path', rule.rule),
                    ('method', 'POST')
                    ])
            if 'PUT' in rule.methods:
                response_dict[endpoint+'_update'] = OrderedDict([
                    ('path', rule.rule),
                    ('method', 'PUT')
                    ])
            if 'DELETE' in rule.methods:
                response_dict[endpoint+'_delete'] = OrderedDict([
                    ('path', rule.rule),
                    ('method', 'DELETE')
                    ])
        return make_json_response(response_dict)


class ActionName(MethodView):
    def get(self, action_name):
        rule_dict = OrderedDict()

        if action_name is not None:
            for rule in app.url_map.iter_rules():
                endpoint = rule.endpoint.rsplit('.', 1)[-1]

                if endpoint != action_name:
                    continue

                rule_dict[endpoint] = OrderedDict([
                    ('path', rule.rule),
                    ('method', list(rule.methods - {'OPTIONS', 'HEAD'})),
                ])

                if rule.arguments is not None:
                    rule_dict[endpoint].update({'url_args': list(rule.arguments)})

                break
        return make_json_response(rule_dict)
