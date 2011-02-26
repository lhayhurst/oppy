import unittest 
import oauth2 as oauth
from config import OpPyConfig
import json
from OPOAuthConnection import OPOAuthConnection
from OPThings import User

#from http://help.obsidianportal.com/kb/api/api-users
class UserAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/users/me.json'

    #assumes the existence of a valid local configuration file
    def __init__(self, config):
        self.connection = OPOAuthConnection(config)

    def get_me(self):
        content = self.connection.get( UserAPI.requestUrl )
        user_info = User(json.loads( content ))
        return user_info

class TestAPIUsers( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.userinfo = UserAPI( self.config )

    def test_get_me(self):
        user = self.userinfo.get_me()
        
        self.assertTrue(user.updated_at() != None )
        self.assertTrue( type(user.updated_at()).__name__ == 'unicode' )

        self.assertTrue(user.created_at() != None )
        self.assertTrue( type(user.created_at()).__name__ == 'unicode' )

        self.assertTrue(user.locale() != None )
        self.assertTrue( type(user.locale()).__name__ == 'unicode' )

        self.assertTrue(user.utc_offset() != None )
        self.assertTrue( type(user.utc_offset()).__name__ == 'unicode' )

        self.assertTrue(user.last_seen_at() != None )
        self.assertTrue( type(user.last_seen_at()).__name__ == 'unicode' )

        self.assertTrue(user.is_ascendant() != None )
        self.assertTrue( type(user.is_ascendant()).__name__ == 'bool' )

        self.assertTrue(user.campaigns() != None )
        self.assertTrue( type(user.campaigns()).__name__ == 'list' )

        self.assertTrue(user.profile_url() != None )
        self.assertTrue( type(user.profile_url()).__name__ == 'unicode' )

        self.assertTrue(user.avatar_image_url() != None )
        self.assertTrue( type(user.avatar_image_url()).__name__ == 'unicode' )

        self.assertTrue(user.username() != None )
        self.assertTrue( type(user.username()).__name__ == 'unicode' )


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




        
        
  