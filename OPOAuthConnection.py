import oauth2 as oauth
import time

class OPOAuthConnection:

    def __init__(self, config):
        self.config = config

        key=config.get_consumer_key()
        secret=config.get_consumer_secret()
        self.consumer = oauth.Consumer( key, secret )

        self.token = oauth.Token( config.get_oauth_token(), config.get_oauth_secret() )
        self.client = oauth.Client( self.consumer, self.token )

    def get(self, url, optional_params = {} ):

        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
        }

        for k,v in optional_params.items():
            params[ k ] = v

        # Set our token/key parameters
        params['oauth_token'] = self.token.key
        params['oauth_consumer_key'] = self.consumer.key

        # Create our request. Change method, etc. accordingly.
        req = oauth.Request(method="GET", url=url, parameters=params)
        signature_method = oauth.SignatureMethod_HMAC_SHA1()

        #fetch the user info
        req.sign_request(signature_method, self.consumer, self.token)
        resp, content = self.client.request( req.to_url() )

        if resp['status'] != '200':
            raise Exception("Unable to fetch user information, reason: %s." % resp['status'])

        return content

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


