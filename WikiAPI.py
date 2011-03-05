import unittest
from OPThings import Wiki
from config import OpPyConfig
import json
from OPOAuthConnection import OPOAuthConnection

#from http://help.obsidianportal.com/kb/api/api-wiki-pages
class WikiAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/campaigns/'

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
        self.assertTrue( wiki )
        self.assertEqual( 3, len( wiki.pages() ))
        homepage = wiki.pages()[0]
        self.assertTrue( homepage )
        self.assertTrue( homepage.campaign() )
        self.assertEqual( homepage.campaign().id(), oppyCmpnId)
        self.assertEqual( 'Home Page', homepage.name() )
        self.assertEqual( 'afa0074c42a111e0bbb240403656340d', homepage.id() )
        self.assertEqual( 'home-page', homepage.slug() )
        self.assertEqual( 'WikiPage', homepage.page_type() )
        self.assertEqual( 'http://www.obsidianportal.com/campaigns/oppy/wiki_pages/home-page', homepage.wiki_page_url() )
        mainpage = wiki.pages()[1]
        self.assertTrue( mainpage )
        self.assertTrue( mainpage.campaign() )
        self.assertEqual( mainpage.campaign().id(), oppyCmpnId)
        self.assertEqual( 'Main Page', mainpage.name() )
        self.assertEqual( 'b0437bb642a111e0bbb240403656340d', mainpage.id() )
        self.assertEqual( 'main-page', mainpage.slug() )
        self.assertEqual( 'WikiPage', mainpage.page_type() )
        self.assertEqual( 'http://www.obsidianportal.com/campaigns/oppy/wiki_pages/main-page', mainpage.wiki_page_url() )
        welcomepage = wiki.pages()[2]
        self.assertTrue( welcomepage )
        self.assertTrue( welcomepage.campaign() )
        self.assertEqual( welcomepage.campaign().id(), oppyCmpnId)
        self.assertEqual( 'Welcome', welcomepage.name() )
        self.assertEqual( 'b076352442a111e0bbb240403656340d', welcomepage.id() )
        self.assertEqual( 'welcome', welcomepage.slug() )
        self.assertEqual( 'Post', welcomepage.page_type() )
        self.assertEqual( 'http://www.obsidianportal.com/campaigns/oppy/wiki_pages/welcome', welcomepage.wiki_page_url() )




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






