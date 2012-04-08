/*
 * mustache-loader.js - Mustache template loader to go with flask-mustache
 *
 * This depends on jQuery, and either:
 * - Twitter's Hogan.js:  https://github.com/twitter/hogan.js or
 * - Mustache.js:         https://github.com/janl/mustache.js
 *
 * Usage:
 *
 *   $('#target').mustache('includes/_user.mustache', {user_name:'Jan'});
 *   var html = $.mustache('includes/_user.mustache', {user_name:'Jan'});
 *   $.mustacheAsFunction('includes/_user.mustache')({user_name:'Jan'});
 */

/*jslint
 browser: true,
 white: true,
 vars: true
*/

/*globals jQuery */

// authored as a jQuery plugin
(function($) {
    "use strict";

    // this is a cached lookup table of templates
    var cache = {};

    var load = function(templateName) {
        // this function takes names like: "includes/_user.mustache"
        // and loads them from somewhere else.

        // they can be cached as functions, or as strings.
        // Strings are template content.
        if (typeof cache[templateName] === 'undefined') {
            // first we need to convert slashes to hyphens, since
            // they're DOM valid
            var domTemplateName = templateName.replace('/', '-');

            if (document.getElementById(domTemplateName)) {
                // stupid hack to turn HTML-encoded templates into strings, see:
                // http://stackoverflow.com/a/2419664/61435
                cache[templateName] = $('<div />').html(
                    $(document.getElementById(domTemplateName)).html().trim()).text();
            }
        }

        return cache[templateName];
    };

    var compile = function(templateName) {
        // returns a compiled template.
        // only works with Hogan.js or if templates pre-compiled.
        var templateContent = load(templateName),
            template = null;

        if (typeof templateContent === 'string' && window.Hogan) {
            template = cache[templateName] = window.Hogan.compile(templateContent);
        }
        if (template === null) {
            $.error("Couldn't compile template " + templateName);
        }
        return template;
    };

    var renderFunction = function(templateName) {
        // returns a wrapped `render` function
        // only works with Hogan.js or if templates pre-compiled.
        var template = compile(templateName);

        return function(context) {
            // template is pre-compiled
            if (typeof template === 'function') {
                return template(context);
            }
            // template has been compiled by this file
            else {
                return template.render(context);
            }
        };
    };

    var render = function(templateName, context) {

        // first we need to try and load the template
        var template = load(templateName);

        if (typeof template === 'undefined') {
            $.error('Unknown template ' + templateName);
        }

        else if (typeof template === 'function') {
            // template has been pre-compiled, just return it
            return template(context);
        }

        // template hasn't been pre-compiled yet
        // so we need to do other things
        if (window.Hogan) {
            return window.Hogan.compile(template).render(context);
        }
        else if (window.Mustache) {
            return window.Mustache.render(template, context);
        }

        // we don't have Hogan or Mustache, so we need to bail
        $.error('Must have either Hogan.js or Mustache.js to load string templates');
    };

    $.fn.mustache = function(templateName, context) {
        // replaces the content of the passed in element with the content
        // rendered by Mustache

        return this.html(render(templateName, context));
    };

    $.mustache = function(templateName, context) {
        // returns the compiled HTML

        return render(templateName, context);
    };

    $.mustacheAsFunction = function(templateName) {
        // returns a function that can be used to render the
        // mustache template

        return renderFunction(templateName);
    };

}(jQuery));