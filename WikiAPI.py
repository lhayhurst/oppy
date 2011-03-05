import unittest
from OPThings import Wiki, WikiPage
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


    def show_page(self, campaignID, wikiID ):
        url = WikiAPI.requestUrl + campaignID + "/wikis/" + wikiID + ".json"
        content = self.connection.get( url, {'campaign_id' : campaignID, 'id' : wikiID } );
        wikiPage = WikiPage( json.loads( content ))
        return wikiPage

    def show_by_slug(self, campaignID, slug ):
        url = WikiAPI.requestUrl + campaignID + "/wikis/" + slug + ".json"
        print url
        content = self.connection.get( url, {'campaign_id' : campaignID, 'use_slug' : 1 } )

        wikiPage = WikiPage( json.loads( content ))
        return wikiPage

class TestAPIWiki( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.wiki = WikiAPI( self.config )
        self.oppyCmpnId = 'af7946b642a111e0bbb240403656340d'
        self.homepage_id = 'afa0074c42a111e0bbb240403656340d'
        self.homepage_slug = 'home-page'

    def test_show_page_by_slug(self):
        homepage = self.wiki.show_by_slug( self.oppyCmpnId, self.homepage_slug )
        self.assertTrue( homepage)
        self.homepage_basic_asserts( homepage )
        
    def homepage_basic_asserts(self, homepage):
        self.assertTrue(homepage.campaign())
        self.assertTrue( type(homepage.campaign()).__name__ == 'instance' )
        print homepage.campaign().campaign_url()
        self.assertEqual(homepage.campaign().id(), self.oppyCmpnId)
        self.assertEqual('Home Page', homepage.name())
        self.assertTrue( type(homepage.name()).__name__ == 'unicode' )
        self.assertEqual(self.homepage_id, homepage.id()) 
        self.assertTrue( type(homepage.id()).__name__ == 'unicode' )
        self.assertEqual(self.homepage_slug, homepage.slug())
        self.assertTrue( type(homepage.slug()).__name__ == 'unicode' )
        self.assertEqual('WikiPage', homepage.page_type())
        self.assertTrue( type(homepage.page_type()).__name__ == 'unicode' )
        self.assertFalse( homepage.is_game_master_only() )
        self.assertTrue( type(homepage.is_game_master_only()).__name__ == 'bool' )
        self.assertEqual('http://www.obsidianportal.com/campaigns/oppy/wiki_pages/home-page', homepage.wiki_page_url())
        self.assertTrue( type(homepage.wiki_page_url()).__name__ == 'unicode' )
        self.assertTrue( homepage.tags())
        self.assertTrue( type(homepage.tags()).__name__ == 'list' )
        self.assertEqual( 3, len(homepage.tags()))
        self.assertEqual( "oppy", homepage.tags()[0])
        self.assertEqual( "Test", homepage.tags()[1])
        self.assertEqual( "tags", homepage.tags()[2])



    def test_show_page(self ):
        homepage = self.wiki.show_page( self.oppyCmpnId, self.homepage_id )
        self.assertTrue( homepage )
        self.homepage_basic_asserts( homepage )
        #unlike fetching pages from the top level wiki, when you fetch them by individual page, you should get
        #real data back for body, body_html, game_master_info, game_master_info_html fields
        self.assertTrue( homepage.body )
        self.assertTrue( len(homepage.body()) > 0 )
        self.assertTrue( homepage.body_html() )
        self.assertTrue( len(homepage.body_html()) > 0 )
        self.assertTrue( homepage.game_master_info() )
        self.assertTrue( len(homepage.game_master_info()) > 0 )
        self.assertTrue( homepage.game_master_info_html() )
        self.assertTrue( len(homepage.game_master_info_html()) > 0 )


    def test_get(self):
        wiki = self.wiki.get( self.oppyCmpnId )
        self.assertTrue( wiki )
        self.assertEqual( 3, len( wiki.pages() ))
        self.assertTrue( wiki.adventure_log() )
        homepage = wiki.pages()[0]
        self.assertTrue( homepage )
        self.homepage_basic_asserts(homepage)
        #when the page is fetched from the top level, "For bandwidth conservation, the data returned does not
        #include the the body, body_html, game_master_info, game_master_info_html fields
        self.assertIsNone( homepage.body())
        self.assertIsNone( homepage.body_html())
        self.assertIsNone( homepage.game_master_info())
        self.assertIsNone( homepage.game_master_info_html())

        mainpage = wiki.pages()[1]
        self.assertTrue( mainpage )
        self.assertTrue( mainpage.campaign() )
        self.assertEqual( mainpage.campaign().id(), self.oppyCmpnId)
        self.assertEqual( 'Main Page', mainpage.name() )
        self.assertEqual( 'b0437bb642a111e0bbb240403656340d', mainpage.id() )
        self.assertEqual( 'main-page', mainpage.slug() )
        self.assertEqual( 'WikiPage', mainpage.page_type() )
        self.assertEqual( 'http://www.obsidianportal.com/campaigns/oppy/wiki_pages/main-page', mainpage.wiki_page_url() )
        adventurelog = wiki.pages()[2]
        self.assertTrue( adventurelog )
        self.assertTrue( adventurelog.campaign() )
        self.assertEqual( adventurelog.campaign().id(), self.oppyCmpnId)
        self.assertEqual( 'Welcome', adventurelog.name() )
        self.assertEqual( 'b076352442a111e0bbb240403656340d', adventurelog.id() )
        self.assertEqual( 'welcome', adventurelog.slug() )
        self.assertEqual( 'Post', adventurelog.page_type() )
        self.assertEqual( 'http://www.obsidianportal.com/campaigns/oppy/wiki_pages/welcome', adventurelog.wiki_page_url() )
        self.assertEqual( wiki.pages()[2], wiki.adventure_log())




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






