from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseServerError
from haystack.query import SearchQuerySet
from django.conf import settings
import datetime, time

RESULTS_PER_PAGE = getattr(settings, 'TUMBLEWEED_RESULTS_PER_PAGE', 20)

def tumble(request, date_field='pub_date', template_name='tumbleweed/tumble.html', searchqueryset=None, 
    paginate_by=RESULTS_PER_PAGE, context_class=RequestContext, extra_context={}):
    """
    A tumblelog view that harnesses the denormalized data in a haystack index.
    
    Optional parameters:
    
        date_field
            The name of the field in your `haystack`_ index that you would like to order
            your tumbles by.  Default: ``pub_date``.
        
        template_name
            The name of the template to render.  Default: :template:`tumbleweed/tumble.html`.
        
        searchqueryset
            You may pass in your own SearchQuerySet_ if you would like to further restrict
            what items show up in the tumble view.  This is useful for filtering only live
            objects or only objects whose publication date has passed.  Default: ``None``.
        
        paginate_by
            The number of objects to include in each page of the tumble.  Default:
            ``TUMBLEWEED_RESULTS_PER_PAGE`` in your settings file, or 20.
        
        context_class
            Pass in your own `context class`_.  Default: Django's ``RequestContext``.
        
        extra_context
            A dictionary containing extra variables to be included in the context, similar
            to ``extra_context`` included in Django's generic views.
    
    Template context:
    
        page
            The current page of haystack results.
        
        paginator
            The Paginator_ for access to information about the paginated list
            for creating next/previous links, showing the total number of
            tumbled items, etc.
    
    .. _haystack: http://haystacksearch.org/
    .. _SearchQuerySet: http://haystacksearch.org/docs/searchqueryset_api.html
    .. _context class: http://docs.djangoproject.com/en/dev/ref/templates/api/#id1
    .. _Paginator: http://docs.djangoproject.com/en/dev/topics/pagination/
    """

    if not searchqueryset:
        searchqueryset = SearchQuerySet().all()
    things = searchqueryset.order_by('-%s' % date_field)

    paginator = Paginator(things, paginate_by)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except ValueError:
        raise Http404

    context_dict = {
        'page': page,
        'paginator': paginator,
    }
    context_dict.update(extra_context)
    return render_to_response(template_name, context_dict, context_instance=context_class(request))

def archive_year(request, year, searchqueryset=None, date_field='pub_date', template_name='tumbleweed/tumble_archive_year.html', **kwargs):
    """
    A paginated list of tumbled item for a given year.
    
    Required parameters:
    
        year
            The year to tumble, usually passed in as part of the URL.
    
    Optional parameters:
    
        date_field
            The name of the field in your `haystack`_ index that you would like to order
            your tumbles by.  Default: ``pub_date``.
        
        template_name
            The name of the template to render.  Default: :template:`tumbleweed/tumble.html`.
        
        searchqueryset
            You may pass in your own SearchQuerySet_ if you would like to further restrict
            what items show up in the tumble view.  This is useful for filtering only live
            objects or only objects whose publication date has passed.  Default: ``None``.
        
        paginate_by
            The number of objects to include in each page of the tumble.  Default:
            ``TUMBLEWEED_RESULTS_PER_PAGE`` in your settings file, or 20.
        
        context_class
            Pass in your own `context class`_.  Default: Django's ``RequestContext``.
        
        extra_context
            A dictionary containing extra variables to be included in the context, similar
            to ``extra_context`` included in Django's generic views.
        
    Template context:

        page
            The current page of haystack results.
        
        paginator
            The Paginator_ for access to information about the paginated list
            for creating next/previous links, showing the total number of
            tumbled items, etc.
    
    .. _haystack: http://haystacksearch.org/
    .. _SearchQuerySet: http://haystacksearch.org/docs/searchqueryset_api.html
    .. _context class: http://docs.djangoproject.com/en/dev/ref/templates/api/#id1
    .. _Paginator: http://docs.djangoproject.com/en/dev/topics/pagination/
    """
    if not searchqueryset:
        searchqueryset = SearchQuerySet().all()

    try:
        year = int(year)
    except ValueError:
        return HttpResponseServerError(u'An integer is required for year.')

    # TODO: Less ugly, please.
    lookup_kwargs = {
        '%s__gte' % date_field: datetime.datetime(year, 1, 1),
        '%s__lte' % date_field: datetime.datetime(year, 12, 31, 23, 59, 59)
    }
    return tumble(request, searchqueryset=searchqueryset.filter(**lookup_kwargs), template_name=template_name, **kwargs)

def archive_month(request, year, month, searchqueryset=None, date_field='pub_date', month_format='%b',
    template_name='tumbleweed/tumble_archive_month.html', **kwargs):
    """
    A paginated list of tumbled item for a given month.
    
    Required parameters:
    
        year
            The year to tumble, usually passed in as part of the URL.
        month
            The month to tumble, usually passed in as part of the URL.
    
    Optional parameters:
    
        month_format
            The `date formatting`_ code used to interpret the month passed in as a string.
            Default: ``%b``.
        
        date_field
            The name of the field in your `haystack`_ index that you would like to order
            your tumbles by.  Default: ``pub_date``.
        
        template_name
            The name of the template to render.  Default: :template:`tumbleweed/tumble.html`.
        
        searchqueryset
            You may pass in your own SearchQuerySet_ if you would like to further restrict
            what items show up in the tumble view.  This is useful for filtering only live
            objects or only objects whose publication date has passed.  Default: ``None``.
        
        paginate_by
            The number of objects to include in each page of the tumble.  Default:
            ``TUMBLEWEED_RESULTS_PER_PAGE`` in your settings file, or 20.
        
        context_class
            Pass in your own `context class`_.  Default: Django's ``RequestContext``.
        
        extra_context
            A dictionary containing extra variables to be included in the context, similar
            to ``extra_context`` included in Django's generic views.
        
    Template context:

        page
            The current page of haystack results.
        
        paginator
            The Paginator_ for access to information about the paginated list
            for creating next/previous links, showing the total number of
            tumbled items, etc.
    
    .. _date formatting: http://docs.djangoproject.com/en/dev/ref/templates/builtins/#now
    .. _haystack: http://haystacksearch.org/
    .. _SearchQuerySet: http://haystacksearch.org/docs/searchqueryset_api.html
    .. _context class: http://docs.djangoproject.com/en/dev/ref/templates/api/#id1
    .. _Paginator: http://docs.djangoproject.com/en/dev/topics/pagination/
    """
    if not searchqueryset:
        searchqueryset = SearchQuerySet().all()

    # TODO: day list?

    # This logic courtesy of Django's date-based generic views
    try:
        tt = time.strptime("%s-%s" % (year, month), '%s-%s' % ('%Y', month_format))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    now = datetime.datetime.now()

    # Calculate first and last day of month, for use in a date-range lookup.
    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {
        '%s__gte' % date_field: first_day,
        '%s__lt' % date_field: last_day,
    }
    return tumble(request, searchqueryset=searchqueryset.filter(**lookup_kwargs), template_name=template_name, **kwargs)

def archive_day(request, year, month, day, searchqueryset=None, date_field='pub_date', month_format='%b', day_format='%d',
        template_name='tumbleweed/tumble_archive_day.html', **kwargs):
    """
    A paginated list of tumbled item for a given month.

    Required parameters:

        year
            The year to tumble, usually passed in as part of the URL.
        month
            The month to tumble, usually passed in as part of the URL.
        day
            The day to tumble, usualy passed in as part of the URL.

    Optional parameters:

        month_format
            The `date formatting`_ code used to interpret the month passed in as a string.
            Default: ``%b``.
        
        day_format
            The `date formatting`_ code used to interpret the day pass in as a string.
            Default: ``%d``.
        date_field
            The name of the field in your `haystack`_ index that you would like to order
            your tumbles by.  Default: ``pub_date``.

        template_name
            The name of the template to render.  Default: :template:`tumbleweed/tumble.html`.

        searchqueryset
            You may pass in your own SearchQuerySet_ if you would like to further restrict
            what items show up in the tumble view.  This is useful for filtering only live
            objects or only objects whose publication date has passed.  Default: ``None``.

        paginate_by
            The number of objects to include in each page of the tumble.  Default:
            ``TUMBLEWEED_RESULTS_PER_PAGE`` in your settings file, or 20.

        context_class
            Pass in your own `context class`_.  Default: Django's ``RequestContext``.

        extra_context
            A dictionary containing extra variables to be included in the context, similar
            to ``extra_context`` included in Django's generic views.

    Template context:

        page
            The current page of haystack results.

        paginator
            The Paginator_ for access to information about the paginated list
            for creating next/previous links, showing the total number of
            tumbled items, etc.

    .. _date formatting: http://docs.djangoproject.com/en/dev/ref/templates/builtins/#now
    .. _haystack: http://haystacksearch.org/
    .. _SearchQuerySet: http://haystacksearch.org/docs/searchqueryset_api.html
    .. _context class: http://docs.djangoproject.com/en/dev/ref/templates/api/#id1
    .. _Paginator: http://docs.djangoproject.com/en/dev/topics/pagination/
    """
    if not searchqueryset:
        searchqueryset = SearchQuerySet().all()

    # More logic courtesy of Django
    try:
        tt = time.strptime('%s-%s-%s' % (year, month, day),
                           '%s-%s-%s' % ('%Y', month_format, day_format))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    lookup_kwargs = {
        '%s__gte' % date_field: datetime.datetime.combine(date, datetime.time.min),
        '%s__lte' % date_field: datetime.datetime.combine(date, datetime.time.max)
    }
    return tumble(request, searchqueryset=searchqueryset.filter(**lookup_kwargs), template_name=template_name, **kwargs)
