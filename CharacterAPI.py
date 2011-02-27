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

    def show_by_id(self, campaignID, characterID):
        campaign_url = CampaignAPI.requestUrl + campaignID + "/characters/" + characterID + ".json"
        content = self.connection.get( campaign_url )
        character = Character( json.loads( content ))
        return character

    def show_by_slug(self, campaignID, slug ):
        campaign_url = CampaignAPI.requestUrl + campaignID + "/characters/" + slug + ".json"
        content = self.connection.get( campaign_url, {'use_slug': '1'} )
        character = Character( json.loads( content ))
        return character

class TestCharacterAPI( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.api = CharacterAPI( self.config )

    def test_show_by_id(self):

        oppyCmpnId  = 'af7946b642a111e0bbb240403656340d'
        characterID = 'e9b9001e42a111e0845c40403656340d'
        character = self.api.show_by_id( oppyCmpnId, characterID)

        self.character_assertions(character, oppyCmpnId, characterID )

    def test_show_by_slug(self):

        oppyCmpnId  = 'af7946b642a111e0bbb240403656340d'
        slug        = 'poppy'
        character = self.api.show_by_slug( oppyCmpnId, slug )

        self.character_assertions( character, oppyCmpnId, 'e9b9001e42a111e0845c40403656340d')

    def test_get(self):

        oppyCmpnId = 'af7946b642a111e0bbb240403656340d'
        characterID = 'e9b9001e42a111e0845c40403656340d'

        characters = self.api.get( oppyCmpnId)
        self.assertTrue( characters )
        self.assertTrue( type(characters).__name__ == 'list' )
        self.assertTrue( len(characters) == 1 )
        character = characters[0]
        self.character_assertions(character, oppyCmpnId, characterID )

    def character_assertions(self, character, oppyCmpnId, characterID):
        self.assertTrue(character)
        self.assertEqual("Poppy", character.name())
        self.assertEqual("poppy", character.slug())
        self.assertTrue(character.author())
        self.assertEqual("sozin", character.author().username())
        self.assertTrue(character.campaign())
        self.assertEqual(oppyCmpnId, character.campaign().id())
        self.assertEqual('e9b9001e42a111e0845c40403656340d', character.id())
        self.assertFalse(character.is_game_master_only())
        self.assertTrue(character.is_player_character())
        self.assertTrue(character.dynamic_sheet_template())
        self.assertEqual('3b934b1815d111e0ade440403656340d', character.dynamic_sheet_template().id())
        self.assertEqual('Udalrich\'s Pathfinder DST', character.dynamic_sheet_template().name())
        self.assertEqual('udalrich_pathfinder', character.dynamic_sheet_template().slug())



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