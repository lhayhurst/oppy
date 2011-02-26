import ConfigParser
import unittest
import os
import shutil

class OpPyConfig:

    #constants


    #these are the names of the configuration keys in the config file
    REQUEST_TOKEN_URL_OPTION = "request_token_url"
    ACCESS_TOKEN_URL_OPTION = "access_token_url"
    AUTHORIZE_URL_OPTION = "authorize_url"
    REGISTER_URL_OPTION = "register_url"
    CONSUMER_KEY_OPTION = "consumer_key"
    CONSUMER_SECRET_OPTION = "consumer_secret"
    OATH_SECRET_OPTION = "oath_secret"
    OATH_TOKEN_OPTION = "oath_token"

    #these are the default values
    request_token_url = 'https://www.obsidianportal.com/oauth/request_token'
    access_token_url  = 'https://www.obsidianportal.com/oauth/access_token'
    authorize_url     = 'https://www.obsidianportal.com/oauth/authorize'
    register_url      = 'http://www.obsidianportal.com/oauth/clients/new'
    URL_SECTION       = "URLS"
    SECRET_SECTION    = "SECRET"

    def __init__(self, config_file_name ):
        if not config_file_name:
            config_file_name = 'oppy.cfg'
        self.config = ConfigParser.RawConfigParser()
        self.config_file_name = config_file_name

    def create_default_config(self):

       self.config.add_section( OpPyConfig.URL_SECTION )
       self.config.set( OpPyConfig.URL_SECTION, OpPyConfig.REQUEST_TOKEN_URL_OPTION, OpPyConfig.request_token_url)
       self.config.set( OpPyConfig.URL_SECTION, OpPyConfig.ACCESS_TOKEN_URL_OPTION, OpPyConfig.access_token_url)
       self.config.set( OpPyConfig.URL_SECTION, OpPyConfig.AUTHORIZE_URL_OPTION, OpPyConfig.authorize_url)
       self.config.set( OpPyConfig.URL_SECTION, OpPyConfig.REGISTER_URL_OPTION, OpPyConfig.register_url)

       self.config.add_section( OpPyConfig.SECRET_SECTION )
       self.config.set( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_KEY_OPTION, "YOUR_CONSUMER_KEY")
       self.config.set( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_SECRET_OPTION, "YOUR_CONSUMER_SECRET")
       self.config.set( OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_TOKEN_OPTION, "YOUR_OATH_TOKEN")
       self.config.set( OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_SECRET_OPTION, "YOUR_OATH_SECRET")

       self._write()

    def is_default_consumer(self):
        if cmp(self.get_consumer_key(),'YOUR_CONSUMER_KEY') or cmp(self.get_consumer_secret(),'YOUR_CONSUMER_SECRET'):
            return 0
        return 1

 
    def get_request_token_url(self):
        return self.get_configuration( OpPyConfig.URL_SECTION, OpPyConfig.REQUEST_TOKEN_URL_OPTION )

    def get_consumer_key(self):
        return self.get_configuration( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_KEY_OPTION )

    def get_consumer_secret(self):
        return self.get_configuration(OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_SECRET_OPTION )

    def get_oauth_token(self):
        return self.get_configuration( OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_TOKEN_OPTION )

    def get_oauth_secret(self):
        return self.get_configuration(OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_SECRET_OPTION )
    
    def get_configuration(self, section, option):
        self._open()
        return self.config.get( section, option )

    def save_oauth_token(self, ouath_token):
        self.save_key( OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_TOKEN_OPTION, ouath_token )

    def save_oath_token_secret(self, oauth_secret ):
        self.save_key( OpPyConfig.SECRET_SECTION, OpPyConfig.OATH_SECRET_OPTION, oauth_secret )


    def save_consumer_key(self, consumer_key ):
        self.save_key( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_KEY_OPTION, consumer_key )

    def save_consumer_secret(self, consumer_secret):
        self.save_key( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_SECRET_OPTION, consumer_secret )
        
    def save_key(self, section, option, value ):
        self._open()
        self.config.set( section, option, value )
        self._write()

    def _open(self ):
        #@TODO: don't read if already open
        file = self.config.read( self.config_file_name )
        if not len(file) == 1:
            return 0
        return 1

    def _write(self):
        #@TODO: maybe back the file up on write?
        with open( self.config_file_name, 'wb') as configfile:
            self.config.write(configfile)

class TestOpPyConfig( unittest.TestCase ):
    config_test_file =  'oppy.cfg.test'
    def setUp( self ):
        self.cfg = OpPyConfig( TestOpPyConfig.config_test_file)
        self.cfg.create_default_config()

    def testCreateDefault(self):
        self.assertTrue( os.path.exists( self.cfg.config_file_name ) )
        self.assertTrue( self.cfg.is_default_consumer())
        self.assertTrue( self.cfg.config.has_option( OpPyConfig.URL_SECTION, 'request_token_url' ) )
        self.assertTrue( self.cfg.config.has_option( OpPyConfig.SECRET_SECTION, 'consumer_key') )

    def testOpen(self):
        self.assertTrue( self.cfg._open() ) #verify tht the file can be opened ok
        os.remove( self.cfg.config_file_name)
        self.assertFalse( self.cfg._open() ) #verify that it can't be open when deleted

    def testGetConfiguration(self):
        #try a couple that should work
        self.assertEqual( OpPyConfig.authorize_url,
                          self.cfg.get_configuration( OpPyConfig.URL_SECTION, OpPyConfig.AUTHORIZE_URL_OPTION ) )
        self.assertEqual( "YOUR_CONSUMER_SECRET",
                          self.cfg.get_configuration( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_SECRET_OPTION ) )

        #and a couple that shouldn't
        #@TODO: why doesn't the below fail?!
        #self.assertRaises(  ConfigParser.NoOptionError,
        #                    self.cfg.get_configuration( OpPyConfig.URL_SECTION, OpPyConfig.CONSUMER_SECRET_OPTION ) )

    def testWriteConfiguration(self):
        self.cfg.save_consumer_key( "12345xyz")
        self.assertEqual( "12345xyz",
                          self.cfg.get_configuration( OpPyConfig.SECRET_SECTION, OpPyConfig.CONSUMER_KEY_OPTION ) )

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