"flask-mustache Flask plugin"

from jinja2 import Template

import pystache

from flask import current_app, Blueprint

__all__ = ('FlaskMustache',)

mustache_app = Blueprint('mustache', __name__, template_folder='templates', static_folder='static')

class FlaskMustache(object):
    "Wrapper to inject Mustache stuff into Flask"
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        "Wrapper around the app so that we can instantiate it from different places"
        self.app = app

        # XXX: this url_prefix is due to a bug in Blueprints where the
        # static assets aren't available until they have a `url_prefix`
        app.register_blueprint(mustache_app, url_prefix='/_mustache')

        # set up global `mustache` function
        app.jinja_env.globals['mustache'] = mustache

        # attach context processor with template content
        app.context_processor(mustache_templates)

    @staticmethod
    def attach(app):
        "This is written so it can work like WSGI middleware"
        # noop
        _ = FlaskMustache(app)

        return app


# context processor
def mustache_templates():
    "Returns the content of all Mustache templates in the Jinja environment"
    # short circuit production mode
    if not current_app.debug:
        return {}

    # get all the templates this env knows about
    all_templates = current_app.jinja_env.loader.list_templates()

    ctx_mustache_templates = {}

    for template_name in all_templates:

        # TODO: make this configurable
        # we only want a specific extension
        if template_name.endswith('mustache'):
            # throw away everything except the file content
            template, _, _ = \
              current_app.jinja_env.loader.get_source(current_app.jinja_env,
                                                      template_name)

            ctx_mustache_templates[template_name] = template

    # prepare context for Jinja
    context = {
        'mustache_templates': ctx_mustache_templates
    }

    # returns the full HTML, ready to use in JavaScript
    template = current_app.jinja_env.get_template('_template_script_block.jinja')
    return {'mustache_templates': template.render(context)}

# template helper function
def mustache(template, **kwargs):
    """Usage:

        {{ mustache('path/to/whatever.mustache', key=value, key1=value1.. keyn=valuen) }}

    This uses the regular Jinja2 loader to find the templates, so your
    *.mustache files will need to be available in that path.
    """
    # TODO: cache loaded templates
    template, _, _ = current_app.jinja_loader.get_source(current_app.jinja_env,
                                                         template)
    return pystache.render(template, kwargs, encoding='utf-8')
