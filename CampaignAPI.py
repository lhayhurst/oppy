import unittest
import json
from config import OpPyConfig
from UserAPI import UserAPI
from OPThings import Campaign
from OPOAuthConnection import OPOAuthConnection

#from http://help.obsidianportal.com/kb/api/api-campaigns
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

    def get_by_slug( self, slug ):
        campaign_url = CampaignAPI.requestUrl + slug + ".json"
        content = self.connection.get( campaign_url,  { 'use_slug': 'true' }  )
        campaign = Campaign( json.loads( content ))
        return campaign


class TestCampaignAPI( unittest.TestCase ):
    def setUp( self ):
        self.config = OpPyConfig( '' )
        self.user_info = UserAPI(self.config)
        self.campaign  = CampaignAPI( self.config )

    def test_get(self):
        campaignID = 'af7946b642a111e0bbb240403656340d'
        campaign = self.campaign.get( campaignID )
        self.campaign_asserts( campaign )

    def test_get_by_user(self):
        #first use the user info api to grab the campaigns
        user = self.user_info.get_me()
        self.assertTrue(user.campaigns() != None )
        campaigns = user.campaigns()

        #then iterate through the campaigns and do some basic sanity checking on 'em
        campAPI = CampaignAPI( self.config )
        for campaign in campaigns:
            camp = campAPI.get(campaign.id())
            self.assertEqual(campaign.id(), camp.id())
            self.assertEqual(campaign.slug(), camp.slug())
            self.assertEqual(campaign.campaign_url(), camp.campaign_url())
            self.assertEqual(campaign.visibility(), camp.visibility())
            self.campaign_asserts( camp )

    def test_get_by_slug(self):
        campaign = self.campaign.get_by_slug( "oppy")
        self.campaign_asserts( campaign )
        
    def campaign_asserts(self, camp ):

        self.assertTrue(type(camp.id()).__name__ == 'unicode')
        self.assertTrue(type(camp.slug()).__name__ == 'unicode')
        self.assertTrue(type(camp.campaign_url()).__name__ == 'unicode')
        self.assertTrue(type(camp.visibility()).__name__ == 'unicode')
        #self.assertTrue(  capi.play_status() != None )
        #self.assertTrue( type(capi.play_status()).__name__ == 'unicode' )
        self.assertTrue(camp.name() != None)
        self.assertTrue(type(camp.name()).__name__ == 'unicode')
        self.assertTrue(camp.looking_for_players() != None)
        self.assertTrue(type(camp.looking_for_players()).__name__ == 'bool')
        self.assertTrue(camp.players() != None)
        self.assertTrue(type(camp.players()).__name__ == 'list')
        self.assertTrue(camp.fans() != None)
        self.assertTrue(type(camp.fans()).__name__ == 'list')
        self.assertTrue(camp.game_master() != None)
        self.assertTrue(type(camp.game_master()).__name__ == 'instance')
        self.assertTrue(camp.location() != None)
        self.assertTrue(type(camp.location()).__name__ == 'dict')

if __name__ == '__main__':
    unittest.main()







