
class Wiki:

    def __init__(self, pages = [] ):
        self.wiki_pages = []
        for page in pages:
            parsed_page = WikiPage( page )
            self.wiki_pages.append( parsed_page )

    def pages(self):
        return self.wiki_pages

    def adventure_log(self):
        for p in self.wiki_pages:
            if p.page_type() == "Post":
                return p

class WikiPage:

    def __init__( self, dictionary = {} ):
        self.page_data = dictionary
        self.camp = Campaign( dictionary['campaign'])

    def campaign(self):
        return self.camp

    def name(self):
        return self.page_data['name']

    def id(self):
        return self.page_data['id']

    def id(self):
        return self.page_data['id']

    def slug(self):
        return self.page_data['slug']

    def page_type(self):
        return self.page_data['type']

    def wiki_page_url(self):
        return self.page_data['wiki_page_url']

    def body(self):
        return self.page_data['body']

    def body_html(self):
        return self.page_data['body_html']

    def game_master_info(self):
        return self.page_data['game_master_info']

    def game_master_info_html(self):
        return self.page_data['game_master_info_html']

    def is_game_master_only(self):
        return self.page_data['is_game_master_only']

    def tags(self):
        return self.page_data['tags']
    


class Character:

    def __init__(self, dictionary= {} ):
        self.character           = dictionary
        self.character_campaign  = Campaign( dictionary['campaign'])
        self.character_author    = User( dictionary['author'] )
        self.template            = DynamicSheetTemplate( dictionary['dynamic_sheet_template'])

    def campaign(self):
        return self.campaign

    #this stuff is mostly boilerplate.  @todo: dynamically generate

    def author(self): return self.character_author
    def campaign(self): return self.character_campaign
    def dynamic_sheet_template(self): return self.template


    def name(self): return self.character['name']
    def slug(self): return self.character['slug']
    def id(self): return self.character['id']
    def is_game_master_only(self): return self.character['is_game_master_only']
    def is_player_character(self): return self.character['is_player_character']
    def avatar_url(self): return self.character['avatar_url']
    def bio(self): return self.character['bio']
    def bio_html(self): return self.character['bio_html']
    def created_at(self): return self.character['created_at']
    def updated_at(self): return self.character['updated_at']
    def description(self): return self.character['description']
    def description_html(self): return self.character['description_html']
    def dynamic_sheet(self): return self.character['dynamic_sheet']
    def game_master_info(self): return self.character['game_master_info']
    def game_master_info_html(self): return self.character['game_master_info_html']
    def created_at(self): return self.character['created_at']

class DynamicSheetTemplate:

    def __init__(self, dictionary = {} ):
        self.template = dictionary

    def id(self): return self.template['id']
    def name(self): return self.template['name']
    def slug(self): return self.template['slug']


class User:

    def __init__(self, dictionary={}):
        self.userinfo = dictionary

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
        if 'campaigns' in self.userinfo:
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

class Campaign:
    def __init__(self, dictionary={}):
        self.campaign_info = dictionary

    def print_campaign(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint( self.campaign_info)

    #id - identifier - An identifier for the campaign. This will never change.
    def id(self): return self.campaign_info['id']

    def name(self): return self.campaign_info['name']

    #slug - string - A URL-friendly slug for the campaign. The user can change this.
    def slug(self): return self.campaign_info['slug']

    #campaign_url - string - The URL to the campaign homepage.
    def campaign_url(self): return self.campaign_info['campaign_url']

    #visibility - string - The visibility of the campaign. Can be 'public', 'friends', or 'private'
    def visibility(self): return self.campaign_info['visibility']

    #created_at - timestamp - Indicates when the user first created their account. ISO-8601 timestamp.
    def created_at(self): return self.campaign_info['created_at']

    #updated_at - timestamp - Indicates when the user first created their account. ISO-8601 timestamp
    def updated_at(self): return self.campaign_info['updated_at']

    def play_status(self): return self.campaign_info['play_status']

    def name(self): return self.campaign_info['name']

    def looking_for_players(self): return self.campaign_info['looking_for_players']

    def _convert_to_user(self, key):
        ret = []
        for v in self.campaign_info[key]:
            ret.append(User(v))
        return ret

    def players(self):
        return self._convert_to_user( 'players' )

    def fans(self):
        return self._convert_to_user( 'fans' )

    def game_master(self):
        return User( self.campaign_info[ 'game_master' ] )

    #@todo: returns a Location data structure here, not a dicts
    def location(self): return self.campaign_info['location']

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
