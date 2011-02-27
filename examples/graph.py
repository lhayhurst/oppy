import yapgvb
import sys
sys.path.append( '..')
from config import OpPyConfig
from UserAPI import UserAPI
from CampaignAPI import CampaignAPI

import argparse

def walk_user_campaigns(campaignAPI, graph, nodes, edges, user ):
    print "navigating user %s" % user.username()
    if user.username() in nodes:
        return
    nodes[user.username()] = graph.add_node( user.username(),
                                             label=user.username(),
                                             fontsize=14, shape= "square",
                                             color=yapgvb.colors.blue )

    for camp in user.campaigns():
        campaign = campaignAPI.fetch(camp.id())
        if campaign.name() in nodes:
            continue
        print "navigating campaign %s" %campaign.name()
        nodes[campaign.name()] = graph.add_node(campaign.name(),
                                                label=campaign.name(),
                                                fontsize=14,
                                                fontcolor = "black")
        
        edges[ user.username() + "~" + campaign.name()] = graph.add_edge(nodes[user.username()],
                                                                         nodes[campaign.name()])
        for nuser in campaign.players():
            walk_user_campaigns( campaignAPI, graph, nodes, edges, nuser )
            if not nuser.username() + "~" + campaign.name() in edges:
                edges[ nuser.username() + "~" + campaign.name()] = graph.add_edge(nodes[campaign.name()],
                                                                                  nodes[nuser.username()])
            
def create_graph( cfg, username ):

    userAPI = UserAPI( cfg )
    campaignAPI = CampaignAPI( cfg )

    user = userAPI.show_by_username( username )

    nodes = {}
    edges = {}
    graph = yapgvb.Digraph(username)
    graph.bgcolor = "transparent"
    walk_user_campaigns(campaignAPI, graph, nodes, edges, user )
    
    return graph


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fetch an access token from Obisidian Portal for OAuth access.')
    parser.add_argument('--config_file', action="store", metavar="PATH TO FILE",
                        help="Config file.  I will create one for you if it does not already exist.")
    parser.add_argument('--user', action="store", metavar="USER TO GRAPH",
                        help="User to build the graph from.  I'll default to Micah if you don't provide one.")

    args = parser.parse_args()
    cfg = OpPyConfig( args.config_file)
    user = args.user or "micah"

    print "Generating user-campaign graph starting with user %s... Ctrl-C to terminate" % user
    graph = create_graph( cfg, user )
    # render!
    print "Rendering ..."
    filename = 'opgraph.gif'

    graph.layout(yapgvb.engines.circo )
    graph.render( filename, "gif" )
