import unittest
from config import OpPyConfig
import json
from OPOAuthConnection import OPOAuthConnection
from UserAPI import UserAPI
from CampaignAPI import  CampaignAPI
from OPThings import Character

#from http://help.obsidianportal.com/kb/api/api-characters

class CharacterAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/campaigns/'

    #assumes the existence of a valid local configuration file
    def __init__(self, config):
        self.connection = OPOAuthConnection(config)

    def get(self, campaign_id ):
        url = CharacterAPI.requestUrl + campaign_id + "/characters.json"
        content = self.connection.get(url)
        characters = json.loads( content )
        ret = []
        for c in characters:
             ret.append( Character( c ) )
        return ret


class TestCharacterAPI( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.api = CharacterAPI( self.config )

    def testFetch(self):
        oppyCmpnId = 'af7946b642a111e0bbb240403656340d'
        characters = self.api.get( oppyCmpnId)
        self.assertTrue( characters )
        self.assertTrue( type(characters).__name__ == 'list' )
        self.assertTrue( len(characters) == 1 )
        character = characters[0]
        self.assertTrue( character )
        self.assertEqual( "Poppy", character.name())
        self.assertEqual( "poppy", character.slug())

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