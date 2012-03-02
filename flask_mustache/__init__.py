# flask-mustache Flask plugin
import os

from jinja2 import Template

from flask import current_app

class FlaskMustache(object):
    "Wrapper to inject Mustache stuff into Flask"
    def __init__(self, app=None, configure_jinja=True):
        self._configure_jinja = configure_jinja
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        if self._configure_jinja:
            app.jinja2.globals['mustache'] = mustache

        app.context_processor(mustache_templates)


# context processor
def mustache_templates():
    "Returns the content of all Mustache templates in the Jinja environment"
    # short circuit development
    if current_app.debug:
        return {}

    # get all the templates this env knows about
    all_templates = current_app.jinja_loader.list_templates()

    mustache_templates = {}
    for template_name in all_templates:

        # TODO: make this configurable
        # we only want a specific extension
        if template_name.endswith('mustache'):
            # throw away everything except the file content
            template, _, _ = \
              current_app.jinja_loader.get_source(current_app.jinja_env,
                                                  template_name)

            mustache_templates[template_name] = template

    # now we need to render the templates
    template_string = """{% if mustache_templates %}
    {% for template_name, content in mustache_templates.items() %}
        <script type="text/x-mustache-template" id="{{ template_name|replace('/', '-') }}" charset="utf-8">
            {{ content|e }}
        </script>
    {% endfor %}
    {% endif %}"""

    context = {
        'mustache_templates': mustache_templates
    }

    # returns the full HTML, ready to use in JavaScript
    return {'mustache_templates': Template(template_string).render(context)}

# template helper function
def mustache(template, **kwargs):
    """Usage:

        {{ mustache('path/to/whatever.mustache', key=value, key1=value1.. keyn=valuen) }}

    This uses the regular Jinja2 loader to find the templates, so your *.mustache files
    will need to be available in that path.
    """
    template, _, _ = current_app.jinja_loader.get_source(current_app.jinja_env, template)
    return pystache.render(template, kwargs, encoding='utf-8')
