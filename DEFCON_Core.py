################################################################
# DEFCON_GM_Server
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS
################################################################
# Python
#import json

# DEFCON
from DEFCON_Client import DEFCON_Client
from DEFCON_Network import DEFCON_Network
import DEFCON_UserSystem

################################################################
# Global variables
################################################################
network = None
client = None
  
################################################################
# Main loop
################################################################

def main():
  DEFCON_UserSystem.PopulateUserDatabase()
  
  network = DEFCON_Network()
  network.start()
  
  client = DEFCON_Client(1)
  client.start()
  
  
main()