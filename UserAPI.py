import unittest 
import oauth2 as oauth
from config import OpPyConfig
import time
import json
from Campaign import Campaign
from OPOAuthConnection import OPOAuthConnection

#from http://help.obsidianportal.com/kb/api/api-users
class UserAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/users/me.json'

    #assumes the existence of a valid local configuration file
    def __init__(self, config):
        self.connection = OPOAuthConnection(config)

    def fetch(self):
        content = self.connection.get( UserAPI.requestUrl )
        self.userinfo = json.loads( content )

    #id - identifier - A unique identifier for the given user. This will never change.
    def id(self): return self.userinfo['id']

    #username - string - The user's username. Note: The user can change this value.
    def username(self): return self.userinfo['username']

    #avatar_image_url - string - The URL of the user's avatar image.
    def avatar_image_url(self): return self.userinfo['avatar_image_url']


    #profile_url - string - The URL of the user's profile on Obsidian Portal.
    def profile_url(self): return self.userinfo['profile_url']

    #campaigns - campaign mini-object An array of the user's campaigns
    def campaigns(self):
        ret = []
        for v in self.userinfo['campaigns']:
            campaign = Campaign( v )
            ret.append( campaign )
        return ret

    #is_ascendant - boolean - Indicates if the user is an Ascendant member.
    #@todo: return a User type
    def is_ascendant(self): return self.userinfo['is_ascendant']

    #last_seen_at - timestamp - The last time the user was active on the website. ISO-8601 timestamp.
    def last_seen_at(self): return self.userinfo['last_seen_at']

    #utc_offset - string - Formatted string representing the user's time zone.
    # It is formatted as "+HH:MM" and represents the offset from UTC. Example: "-05:00" is Eastern US time.
    def utc_offset(self): return self.userinfo['utc_offset']


    #locale - string - ISO 639-1 language code for the user's preferred language.
    def locale(self): return self.userinfo['locale']

    #created_at - timestamp - Indicates when the user first created their account. ISO-8601 timestamp.
    def created_at(self): return self.userinfo['created_at']

    #updated_at - timestamp - Indicates when the user first created their account. ISO-8601 timestamp
    def updated_at(self): return self.userinfo['updated_at']

class TestAPIUsers( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.userinfo = UserAPI( self.config )

    def testFetch(self):
        self.userinfo.fetch()
        self.assertTrue(self.userinfo.updated_at() != None )
        self.assertTrue( type(self.userinfo.updated_at()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.created_at() != None )
        self.assertTrue( type(self.userinfo.created_at()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.locale() != None )
        self.assertTrue( type(self.userinfo.locale()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.utc_offset() != None )
        self.assertTrue( type(self.userinfo.utc_offset()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.last_seen_at() != None )
        self.assertTrue( type(self.userinfo.last_seen_at()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.is_ascendant() != None )
        self.assertTrue( type(self.userinfo.is_ascendant()).__name__ == 'bool' )

        self.assertTrue(self.userinfo.campaigns() != None )
        self.assertTrue( type(self.userinfo.campaigns()).__name__ == 'list' )

        self.assertTrue(self.userinfo.profile_url() != None )
        self.assertTrue( type(self.userinfo.profile_url()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.avatar_image_url() != None )
        self.assertTrue( type(self.userinfo.avatar_image_url()).__name__ == 'unicode' )

        self.assertTrue(self.userinfo.username() != None )
        self.assertTrue( type(self.userinfo.username()).__name__ == 'unicode' )


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




        
        
  