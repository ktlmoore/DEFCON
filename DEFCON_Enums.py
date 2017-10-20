################################################################
# DEFCON_Enums
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS
################################################################
# Python
from enum import IntEnum

################################################################
# ENUMS 
################################################################
# MsgType
class DEFCON_MsgType(IntEnum):
  NONE     = 0 # A good HandleMessage function should be upset by NONE messages
  REQUEST  = 1 # Requests sent from the client to the server
  RESPONSE = 2 # Responses sent from the server to the client
  COMMAND  = 3 # Commands sent from the server to the client
  
# CmdType
class DEFCON_CmdType(IntEnum):
  NONE            = 0 # A good HandleMessage function should be upset by NONE commands
  SERVER_SHUTDOWN = 1 # Only the server should handle this message
  CLIENT_SHUTDOWN = 2 # Only the client should handle this message
  
# Reserved IDs
class DEFCON_Ids(IntEnum):
  SERVER = 0
  FIRST_CLIENT = 1000