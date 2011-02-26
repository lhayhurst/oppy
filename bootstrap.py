import urlparse
import oauth2 as oauth
import argparse
from config import OpPyConfig

#note:
#this code is taken pretty much verbatim from
#https://github.com/simplegeo/python-oauth2/blob/master/README.md#readme

def boostrap( config ):

    if config.is_default_consumer():
        print "You need to register your application's consumer key and secret."
        print "Please go to the following link in your browser:"
        print OpPyConfig.register_url
        print "Come back here when you've filled out the form"
        consumer_key = raw_input("What is the consumer key that Obsidian Portal provided you (please paste it here exactly)?:")
        consumer_secret = raw_input( "What is the consumer secret?: ")
        config.save_consumer_key( consumer_key )
        config.save_consumer_secret( consumer_secret )

    consumer = oauth.Consumer(config.get_consumer_key(), config.get_consumer_secret())
    client = oauth.Client(consumer)

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token.

    resp, content = client.request(OpPyConfig.request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    print "Request Token:"
    print "    - oauth_token        = %s" % request_token['oauth_token']
    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
    print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (OpPyConfig.authorize_url, request_token['oauth_token'])
    print


    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(OpPyConfig.access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    config.save_oauth_token( access_token['oauth_token'] )
    config.save_oath_token_secret( access_token['oauth_token_secret'] )

    print "Access Token:"
    print "    - oauth_token        = %s" % access_token['oauth_token']
    print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
    print
    print "You may now access protected resources using the access tokens above."
    print "These tokens have been saved into " + config.config_file_name + "."
    print

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fetch an access token from Obisidian Portal for OAuth access.')
    parser.add_argument('--config_file', action="store", metavar="PATH TO FILE",
                        help="Config file.  I will create one for you if it does not already exist.")
    args = parser.parse_args()
    cfg = OpPyConfig( args.config_file)
    if not args.config_file:
        cfg.create_default_config()


    boostrap(cfg)


"""
The MIT License

Copyright (c) 2011 Lyle Hayhurst

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""



  