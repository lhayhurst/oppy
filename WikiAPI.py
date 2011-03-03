import unittest
from config import OpPyConfig
import json
from OPOAuthConnection import OPOAuthConnection

#from http://help.obsidianportal.com/kb/api/api-wiki-pages
class WikiAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/campaigns'

    #assumes the existence of a valid local configuration file
    def __init__(self, config):
        self.connection = OPOAuthConnection(config)

    def get(self, campaignID ):
        # http://api.obsidianportal.com/v1/campaigns/campaign_id/wikis.format is the format of the request url
        url = WikiAPI.requestUrl + campaignID + "/wikis.json"
        content = self.connection.get( url, {'campaign_id' : campaignID } )
        wiki = Wiki(json.loads( content ))
        return wiki

class TestAPIWiki( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.wiki = WikiAPI( self.config )

    def test_get(self):
        oppyCmpnId = 'af7946b642a111e0bbb240403656340d'
        wiki = self.wiki.get( oppyCmpnId )
        assertTrue( wiki )



if __name__ == '__main__':
    unittest.main()

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






