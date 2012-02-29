# flask-mustache Flask plugin
from flask import current_app

# context processor
def mustache_templates():
    "Returns the content of all Mustache templates in the Jinja environment"
    all_templates = current_app.jinja_loader.list_templates('.mustache')
    # returns a dictionary of {template name:content}
    mustache_templates = {}
    for template in all_templates:
        # TODO: need to remove Jinja load path from path and leave
        # trailing path
        pass
    return {'mustache_templates': mustache_templates}

# template helper function
def mustache(template, **kwargs):
    """Usage:

        {{ mustache('path/to/whatever.mustache', key=value, key1=value1.. keyn=valuen) }}

    This uses the regular Jinja2 loader to find the templates, so your *.mustache files
    will need to be available in that path.
    """
    template, _, _ = current_app.jinja_loader.get_source(current_app.jinja_env, template)
    return pystache.render(template, kwargs, encoding='utf-8')
