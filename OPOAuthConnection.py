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

        self._init_error_codes()

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

        status = resp['status']
        if status != '200':
            raise Exception("Unable to fetch information from url %s, reason: %s, notes: %s" %( url,
                                                                                                 resp['status'],
                                                                                                 self.error_codes[status]))
        return content

    #a simple structure used to pretty print out the reasons behind the error codes
    def _init_error_codes(self):
        self.error_codes = {
              '200' :	"Success. This is the most common response when everything works normally.",
              '201'	:   "Created. This is returned when something is created, like a new wiki page.",
              '204' :	"No Content. The server has received the request and acted on it, but nothing needs to be returned. " +
                        "Often returned from a delete request.",
              '400' :	"Request Error. The most common error response. Something was wrong with the request. " +
                        "Inspect the error messages for more information.",
              '403' :	"Forbidden. You are not authorized to see the resource. Often returned when requesting a private campaign " +
                        "or a gm-only page. Inspect the error message for more information.",
              '404' :	"Not Found. The resource you requested cannot be found.",
              '500' :	"Server Error. An error happened on the server. If it continues, please notify us and we'll look into it.",
              '503'	:   "Service Unavailable. The server is temporarily down for maintenance. We do this quite often, so we highly suggest " +
                        "building your apps to be prepared for it. Note: No guarantee that the response body will be a valid format (ie." +
                        " JSON or XML) so it's best to look for the 503 and stop parsing if it's found."
            }

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


