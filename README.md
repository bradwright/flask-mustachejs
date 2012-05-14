# Flask-Mustache #

[Mustache](http://mustache.github.com/) templating tools for
integration with [Flask](http://flask.pocoo.org).

## Warning: this extension is opinionated ##

It assumes the following things:

* You want first-class Mustache template rendering inside your Jinja
  templates;
* You want to share templates between Javascript and your server;
* `.mustache` files live alongside your regular Jinja templates;
* You're using [jQuery](http://jquery.com) on the client.

If you're okay with all of the above, read on.

## Adding to Flask ##

If Flask-Mustache is installed in your `pythonpath`, it'll be
automatically made available under `flask.ext`:

    from flask.ext.mustache import FlaskMustache

There are two ways to add your app, depending on preference.

    # noop style
    FlaskMustache(app)

    # or as a WSGI-middleware style wrapper
    app = FlaskMustache.attach(app)

In both cases the results are the same.

### Serving static assets ###

Flask-Mustache is implemented as a
[Flask Blueprint](http://flask.pocoo.org/docs/blueprints/) so that it
can bring its own Jinja templated and static assets along. One
interesting quirk (bug) of Flask Blueprints is that they can only
serve static assets if
[they're configured with a URL prefix](https://github.com/mitsuhiko/flask/issues/348).
In the case of Flask-Mustache, that URL prefix is automatically set to
`/_mustache`.

Flask-Mustache comes with a jQuery plugin that loads your templates
for you in Javascript. To serve this file the regular Flask way:

    {{ url_for('mustache.static', filename='mustache-loader.js') }}

or via [Flask-Assets](http://flask-assets.readthedocs.org/en/latest/index.html):

    Bundle('mustache/mustache-loader.js')

and that's it.

## Using in Jinja ##

This extension provides a global function named `mustache`. It takes a
few arguments:

1. A path to a template. This path is based on your Flask template
   path (it uses the Flask `jinja_env` load path to find templates)
2. A context object in the form of a dictionary; or
3. `**kwargs` that become the Mustache context.

Examples:

    {{ mustache('includes/_user_profile.mustache', {'user_id':1, 'user_name': 'Bob'}) }}
    {{ mustache('includes/_user_profile.mustache', user_id=1, user_name='Bob') }}

## Using in Javascript ##

Flask-Mustache provides a jQuery plugin that lets you load templates
off the "filesystem" automatically. To load the above example (no `kwargs`
in Javascript):

    $('<div />').mustache('includes/_user_profile.mustache', {user_id:1, user_name:'Bob'})

Creates a new `div` with the contents of whatever Mustache returned.

There are two other ways of using the plugin. The first just returns
the rendered HTML (so you can use it however you want):

    $('<div />'>.html($.mustache('includes/_user_profile.mustache', {user_id:1, user_name:'Bob'}));

and the second returns a function that can be stored as a variable,
for example in the
[Backbone.js](http://documentcloud.github.com/backbone/) style:

    var MyView = Backbone.View.extend({
        template: $.mustacheAsFunction('includes/_user_profile.mustache'),
        render: function() {
            this.$el.html(this.template({user_id:1, user_name:'Bob'}));
        }
    })

The jQuery plugin requires either
[Hogan.js][hoganjs] or
[Mustache.js](https://github.com/janl/mustache.js) in development.

### Loading templates via Javascript in development ###

The templates are read off the file system and dropped into the
template by a context processor. After this the Javascript can pick
them up via regular DOM methods. Put this into your main inherited
`jinja` template:

    {{ mustache_templates }}

and that's it.

### Loading templates via Javascript in production ###

Your templates should be pre-compiled in production so you don't tax
the client. You can do this using the [Hogan.js][hoganjs] binary `hulk`,
which is available if you have installed [Hogan.js][hoganjs] using npm.
`hulk` takes a space separated list of files as arguments and outputs
the compiled template javascript to `stdout`. You can output this
javascript to a file, e.g.:

    hulk templates/includes/_user_profile.mustache > static/compiled_mustache.js

If you have a number of templates, and/or you want to make the
pre-compilation part of your deployment process, you might want to
discover the templates and pass them to `hulk` programmatically.
[This gist](https://gist.github.com/2693186) shows an example
[Flask-Script](https://github.com/rduplain/flask-script/) manager
command that does this.

[hoganjs]:https://github.com/twitter/hogan.js