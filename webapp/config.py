# sentiment/webapp/config.py

from authomatic.providers import oauth1
import os

CONFIG = {
    
    'tw': { # Your internal provider name
        
        # Provider class
        'class_': oauth1.Twitter,
        
        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': os.environ.get('consumer_key'),
        'consumer_secret': os.environ.get('consumer_secret'),
    }
    
    
}