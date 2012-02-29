# Flask-Mustache #

[Mustache](http://mustache.github.com/) templating tools for
integration with [Flask](http://flask.pocoo.org).

## Warning: this extension is opionated ##

It assumes the following things:

* You want first-class Mustache template rendering inside your Jinja
  templates;
* You want to share templates between Javascript and your server;
* `.mustache` files live alongside your regular Jinja templates;
* You're using [jQuery](http://jquery.com) on the client.

If you're okay with all of the above, read on.

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

Flask-Mustache provided a jQuery plugin that lets you load templates
off the filesystem automatically. To load the above example (no `kwargs`
in Javascript):

    $('<div />').mustache('includes/_user_profile.mustache', {user_id:1, user_name:'Bob'})

Creates a new `div` with the contents of whatever Mustache returned.

The jQuery plugin requires either
[Hogan.js](https://github.com/twitter/hogan.js) or
[Mustache.js](https://github.com/janl/mustache.js) in development.

### Loading templates via Javascript in development ###

The templates are read off the file system and dropped into the
template by a context processor. After this the Javascript can pick
them up via regular DOM methods. Put this into your main `jinja` template:

    {{ mustache_templates }}

and that's it.

### Loading templates via Javascript in production ###

Your templates should be pre-compiled in production so you don't tax
the client. Information about how to do this will be forthcoming.
