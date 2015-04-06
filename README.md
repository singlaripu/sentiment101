# Sentiment Analysis for recent Movie Tweets


Approach (time taken ~10 hours):

1. Use basic Django framework to create the desired layout with some dummy data - https://www.djangoproject.com/

2. Use Twython for twitter sign up and pull tweets and feed actual data to above  - https://github.com/ryanmcgrath/twython

3. I also tried Authomatic, but found Twython to be little better - http://peterhudec.github.io/authomatic/

4. Use Twitter Bootstrap for styling - http://getbootstrap.com/. 

5. Design is influenced by - http://www.sentiment140.com/

6. Studied this paper for sentiment analysis - http://arxiv.org/pdf/1305.6143v2.pdf

7. Used their open source implementation to plug this into my webapp - https://github.com/vivekn/sentiment

8. Host on to Heroku using Gunicorn as middle layer to handle the requests.

9. Post to Github.

Links:

http://sentiment101.herokuapp.com/

https://github.com/singlaripu/sentiment101