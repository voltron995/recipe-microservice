from collections import OrderedDict
from flask.views import MethodView
from ..app import app
from ..models import Recipe, RecipeCategory
from ..facilities import json_response


class ActionList(MethodView):
    def get(self):
        rule_dict = OrderedDict()

        for rule in app.url_map.iter_rules():
            endpoint = rule.endpoint.rsplit('.', 1)[-1]

            if endpoint == 'static' or endpoint.startswith('action_'):
                continue

            rule_dict[endpoint] = OrderedDict([
                ('path', rule.rule),
                ('method', list(rule.methods - {'OPTIONS', 'HEAD'})),
            ])

            if rule.arguments:
                rule_dict[endpoint].update({'url_args': list(rule.arguments)})

            if 'POST' in rule_dict[endpoint]['method']:
                rule_dict[endpoint].update(OrderedDict({'post_data':[]}))

        return json_response(rule_dict)

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

        return json_response(rule_dict)
