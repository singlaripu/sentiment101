

# sentiment/webapp/views.py

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from helper import score
import info
import os
from twython import Twython
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

info.setup()


def home(request):
    context = {'not_logged_in': True}
    return render(request, 'webapp/login.html', context)


def login(request):
    response = HttpResponse()
    context = {}
    context['not_logged_in'] = False
    context['user'] = 'dummy_user'
    twitter = Twython(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
    auth_props = twitter.get_authentication_tokens(callback_url=request.build_absolute_uri(reverse('twitter_callback')))
    request.session['request_token'] = auth_props
    return HttpResponseRedirect(auth_props['auth_url'])


def twitter_callback(request):
    response = HttpResponse()
    context = {}
    context['not_logged_in'] = False
    context['user'] = 'dummy_user'
    oauth_verifier = request.GET['oauth_verifier']
    twitter = Twython(
        os.environ.get('consumer_key'), 
        os.environ.get('consumer_secret'),
        request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'],
    )
    authorized_tokens = twitter.get_authorized_tokens(oauth_verifier)
    request.session['oauth_token'] = authorized_tokens['oauth_token']
    request.session['oauth_token_secret'] = authorized_tokens['oauth_token_secret']

    rendered = render_to_string('webapp/search.html', context)
    response.write(rendered)
    return response



def search(request):
    query = request.GET['q']
    response = HttpResponse()
    context = {}
    context['query'] = query
    context['not_logged_in'] = False
    context['user'] = 'dummy_user'           

    twitter = Twython(
        os.environ.get('consumer_key'), 
        os.environ.get('consumer_secret'),
        request.session['oauth_token'],
        request.session['oauth_token_secret'],
    )
    access_response = twitter.search(q=query, result_type='mixed', count=100, include_entities='false', lang='en')

    if 'statuses' in access_response and type(access_response['statuses']) is list:
        context['is_list'] = True
        tweets = [{'text': t["text"], 'created_at':t['created_at'], 'screen_name': t['user']['screen_name']} for t in access_response["statuses"]]
        tweets, graph = score(tweets)
        context['graph'] = graph
        context['tweets'] = tweets
    else:
        context['data_errors'] = 'something went wrong'

    rendered = render_to_string('webapp/index.html', context)
    response.write(rendered)
    return response





