

# sentiment/webapp/views.py

from django.http import HttpResponse
# from authomatic import Authomatic
# from authomatic.adapters import DjangoAdapter
from django.shortcuts import render
from django.template.loader import render_to_string
from helper import score
import info
from config import CONFIG
import os
from twython import Twython
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

info.setup()
# authomatic = Authomatic(CONFIG, os.environ.get('authomatic_key'))



def home(request):
    context = {'not_logged_in': True}
    return render(request, 'webapp/login.html', context)

# def login(request):
#     # We we need the response object for the adapter.
#     response = HttpResponse()
#     context = {}
#     context['login_success'] = False
#     context['not_logged_in'] = True
#     provider_name = "tw"
#     global user_session
#     global credentials
    
#     # Start the login procedure.
#     user_session = authomatic.login(DjangoAdapter(request, response), provider_name)
    
#     # If there is no result, the login procedure is still pending.
#     # Don't write anything to the response if there is no result!
#     if user_session:
#         # If there is result, the login procedure is over and we can write to response.
#         context['login_success'] = True
#         context['error_message'] = False
#         context['user'] = False
#         context['not_logged_in'] = False

#         if user_session.error:
#             # Login procedure finished with an error.
#             context['error_message'] = user_session.error.message
        
#         elif user_session.user:
#             # Hooray, we have the user!
#             # OAuth 2.0 and OAuth 1.0a provide only limited user data on login,
#             # We need to update the user to get more info.
#             if not (user_session.user.name and user_session.user.id):
#                 user_session.user.update()

#             if user_session.user.credentials:
#                 request.session['request_token'] = user_session.user.credentials
#                 credentials = user_session.user.credentials
#                 print credentials
#                 print user_session

#             context['user'] = user_session.user
#             context['user_session'] = user_session
#             context['credentials'] = credentials
                      
#         rendered = render_to_string('webapp/search.html', context)
#         response.write(rendered)
#     return response


# def search1(request):
#     query = request.GET['q']
#     response = HttpResponse()
#     context = {}
#     context['login_success'] = False
#     context['not_logged_in'] = True
#     provider_name = 'tw'
#     context['query'] = query

#     global user_session
#     global credentials

#     context['user_session'] = user_session
#     context['credentials'] = request.session['request_token'] 

#     # global user_session
#     # global credentials
    
#     # Start the login procedure.
#     # user_session = authomatic.login(DjangoAdapter(request, response), provider_name)

#     # if not user_session:
#     #     global user_session
#     #     user_session = authomatic.login(DjangoAdapter(request, response), provider_name)

#     if False:
#         # If there is result, the login procedure is over and we can write to response.
#         context['login_success'] = True
#         context['error_message'] = False
#         context['result_user'] = False
#         context['not_logged_in'] = False
#         if user_session.error:
#             # Login procedure finished with an error.
#             context['error_message'] = user_session.error.message
#             context['not_logged_in'] = True
#         elif user_session.user:
#             context['user'] = user_session.user            
#             # OAuth 2.0 and OAuth 1.0a provide only limited user data on login,
#             # We need to update the user to get more info.
#             if not (user_session.user.name and user_session.user.id):
#                 user_session.user.update()
            
#             context['provider_name'] = False
#             # Seems like we're done, but there's more we can do...
#             # If there are credentials (only by AuthorizationProvider),
#             # we can _access user's protected resources.
#             if user_session.user.credentials:
#                 if user_session.provider.name == 'tw':
#                     context['provider_name'] = 'Twitter'                    
#                     url = 'https://api.twitter.com/1.1/search/tweets.json'
#                     # You can pass a dictionary of querystring parameters.
#                     access_response = user_session.provider.access(url, {
#                                                                     'q': query, 
#                                                                     'include_entities':'false',
#                                                                     'count': 100,
#                                                                     'result_type': 'mixed',
#                                                                     'lang': 'en'
#                                                             })
#                     # access_response = authomatic.access(credentials, url, {
#                     #                                                 'q': query, 
#                     #                                                 'include_entities':'false',
#                     #                                                 'count': 100,
#                     #                                                 'result_type': 'mixed',
#                     #                                                 'lang': 'en'
#                     #                                         })
#                     context['status'] = False
#                     # Parse response.
#                     if access_response.status == 200:
#                         context['status'] = True
#                         context['is_list'] = False
#                         if type(access_response.data) is dict:
#                             context['is_list'] = True
#                             tweets = [{'text': t["text"], 'created_at':t['created_at'], 'screen_name': t['user']['screen_name']} for t in access_response.data["statuses"]]
#                             tweets, graph = score(tweets)
#                             context['graph'] = graph
#                             context['tweets'] = tweets
#                         elif access_response.data.get('errors'):
#                             context['data_errors'] = access_response.data.get('errors')
#                     else:
#                         context['status_error'] = access_response.status

#         rendered = render_to_string('webapp/index.html', context)
#         response.write(rendered)
#     else:
#         # login(request)
#         pass

#     rendered = render_to_string('webapp/index.html', context)
#     response.write(rendered)
#     return response
    


def login1(request):
    response = HttpResponse()
    context = {}
    context['not_logged_in'] = False
    context['user'] = 'dummy_user'

    twitter = Twython(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
    # auth_props = twitter.get_authentication_tokens(callback_url='http://sentiment101.herokuapp.com:8000/twitter_callback')
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

    context['provider_name'] = 'Twitter'                    
    url = 'https://api.twitter.com/1.1/search/tweets.json'

    twitter = Twython(
        os.environ.get('consumer_key'), 
        os.environ.get('consumer_secret'),
        request.session['oauth_token'],
        request.session['oauth_token_secret'],
    )

    # You can pass a dictionary of querystring parameters.
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





