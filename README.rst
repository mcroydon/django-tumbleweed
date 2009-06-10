=================
django-tumbleweed
=================

Tumbleweed allows you to easily create a tumbleog by taking advantage of data
already denormalized in Haystack_.  Tumbleweed runs quite slowly under Whoosh_
but is quite quick using Solr_.

Getting started
===============

The quickest way to get started with tumbleweed is to download tumbleweed,
make sure it is on your ``PYTHONPATH``, and add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
    ...
    'tumbleweed',
    )

Once in your ``INSTALLED_APPS``, add the default tumbleweed urlconf to your
main ``urlpatterns`` in your project's ``urls.py``::

    urlpatterns = patterns('',
        ...
        (r'tumble/', include('tumbleweed.urls')),
    )

The main tumble view will now be available at ``/tumble/``.
Tumbleweed also includes paginated date-based tumble views:

    - ``/tumble/2009/``
    - ``/tumble/2009/jan/``
    - ``/tumble/2009/jan/01/``

If you have ``/admin/doc/`` enabled in your root urlconf, each of the tumbleweed
views is documented.

Tumbleweed philosophy
=====================

Tumbleweed is less of a tumblelog app and more of a tumblelog framework.  In
order to use tumbleweed, you need a collection of Haystack_ SearchIndexes_
that share as much common information as possible.  For example, most objects
that you might want to tumble (blog posts, links, photos, tweets) should have
at least a title, a publication date, and a tease/description.  If you ensure
that each of your SearchIndexes_ contains at least that much information
as fielded data, you can access those fields from your tumble views without
having to hit the database at all.

Extending default behavior
==========================

Tumbleweed ships with sane defaults but like Django's generic views and
Haystack's search view, there are many points for extension.

By default, the tumble view looks for a field on your SearchIndexes_ called
``pub_date``.  If you have called the date field that you would like to tumble
by in your view something else, you can pass ``date_field`` in either as a
dictionary in a urlconf or by calling the view with a ``date_field`` argument.

The default template of ``tumbleweed/tumble.html`` can also be overridden by
overriding ``template_name``.

You can also influence what results are returned by the tumble view by passing
a keyword argument called ``searchqueryset`` in.  For example, if your indexes
have an ``is_public`` field, you could show public items only by modifying your
urls.py::

    from haystack.query import SearchQuerySet
    tumble_dict = {'searchqueryset' : SearchQuerySet().filter(is_public__exact=True)}
    
    urlpatterns = patterns('',
        ...
        (r'tumble/', include('tumbleweed.urls'), tumble_dict),
    )

You can also influence how many items are tumbled on each page by passing in a
``paginate_by`` keyword argument.  If ``paginate_by`` is not included,
tumbleweed will check for ``TUMBLEWEED_RESULTS_PER_PAGE`` in your settings
file, or will fall back to a default of 20.

If you have a custom Context class, you can also pass that in as
``context_class``.

Finally if you would like to add something to the tumble context, you can do so
by passing a dictionary in as ``extra_context``, much like Django's generic
views.

Tumbleweed's date-based views are just thin wrappers around the main tumble
view and show how to customize the tumble view.

TODO
====

- Further documentation
- Tumble template tag
- Tests

License
=======

Tumbleweed is released under the new-style BSD license.

.. _Haystack: http://haystacksearch.org/
.. _Whoosh: http://whoosh.ca/
.. _Solr: http://lucene.apache.org/solr/
.. _SearchIndexes: http://haystacksearch.org/docs/searchindex_api.html