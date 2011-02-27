import unittest
import json
from config import OpPyConfig
from UserAPI import UserAPI
from OPThings import Campaign
from OPOAuthConnection import OPOAuthConnection

#from http://help.obsidianportal.com/kb/api/api-users
class CampaignAPI:

    requestUrl = 'http://api.obsidianportal.com/v1/campaigns/'

    #assumes the existence of a valid local configuration file
    def __init__(self, config):
        self.connection = OPOAuthConnection(config)

    def get(self, campaignID):

        campaign_url = CampaignAPI.requestUrl + campaignID + ".json"
        content = self.connection.get( campaign_url)
        campaign = Campaign( json.loads( content ))
        return campaign



class TestCampaignAPI( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.user_info = UserAPI(self.config)

    def testFetch(self):
        #first use the user info api to grab the campaigns
        user = self.user_info.get_me()
        self.assertTrue(user.campaigns() != None )
        campaigns = user.campaigns()

        #then iterate through the campaigns and do some basic sanity checking on 'em
        for campaign in campaigns:
            campAPI = CampaignAPI( self.config )
            camp =  campAPI.get( campaign.id())
            #capi.print_campaign()

            self.assertEqual( campaign.id(), camp.id() )
            self.assertTrue( type(camp.id()).__name__ == 'unicode' )

            self.assertEqual( campaign.slug(), camp.slug() )
            self.assertTrue( type(camp.slug()).__name__ == 'unicode' )

            self.assertEqual( campaign.campaign_url(), camp.campaign_url() )
            self.assertTrue( type(camp.campaign_url()).__name__ == 'unicode' )

            self.assertEqual( campaign.visibility(), camp.visibility() )
            self.assertTrue( type(camp.visibility()).__name__ == 'unicode' )

            #self.assertTrue(  capi.play_status() != None )
            #self.assertTrue( type(capi.play_status()).__name__ == 'unicode' )

            self.assertTrue(  camp.name() != None )
            self.assertTrue( type(camp.name()).__name__ == 'unicode' )

            self.assertTrue(  camp.looking_for_players() != None )
            self.assertTrue( type(camp.looking_for_players()).__name__ == 'bool' )

            self.assertTrue(  camp.players() != None )
            self.assertTrue( type(camp.players()).__name__ == 'list' )
            self.assertTrue( type(camp.players()[0]).__name__ == 'instance' )

            self.assertTrue(  camp.fans() != None )
            self.assertTrue( type(camp.fans()).__name__ == 'list' )

            self.assertTrue(  camp.game_master() != None )
            self.assertTrue( type(camp.game_master()).__name__ == 'instance' )

            self.assertTrue(  camp.location() != None )
            self.assertTrue( type(camp.location()).__name__ == 'dict' )

if __name__ == '__main__':
    unittest.main()







