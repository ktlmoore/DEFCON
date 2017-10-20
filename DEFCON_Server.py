################################################################
# DEFCON_Server
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS 
################################################################

import DEFCON_Config
import DEFCON_Debugging
from DEFCON_Messages import *

################################################################
# Server class
################################################################

class DEFCON_Server(object):
  
  _ServerShutdown = False
  
  ################################################################   
  def GetShutdown(self):
    return self._ServerShutdown
  
  ################################################################
  def __init__(self):
    self._ServerShutdown = False
    DEFCON_Debugging.Debug(" **SERVER** Loaded!")
  
  ################################################################
  def CheckMessageType(self, objToCheck, expectedType):
    if (not isinstance(objToCheck, expectedType)):
      DEFCON_Debugging.Error(" **SERVER** Rejected message ({!r}) as it was not a {}".format(objToCheck, expectedType))
      return False
    return True
  
  ################################################################
  def HandleMessage(self, message):
    if (not self.CheckMessageType(message, DEFCON_Message)):
      return False
    
    msgId = message.GetMsgID()
    if (msgId == DEFCON_MsgType.NONE):
      DEFCON_Debugging.Error(" **SERVER** Rejected message as it had type NONE")
      return False
    elif (msgId == DEFCON_MsgType.REQUEST):
      return True
    elif (msgId == DEFCON_MsgType.RESPONSE):
      DEFCON_Debugging.Error(" **SERVER** Rejected message as it had type RESPONSE")
      return False
    elif (msgId == DEFCON_MsgType.COMMAND):
      return self.HandleCommand(message)
    else:
      DEFCON_Debugging.Error(" **SERVER** Error, could not handle message with type {:d}".format(msgId))
      return False
      
  ################################################################    
  def HandleCommand(self, command):
    # Check we have a command
    if (not self.CheckMessageType(command, DEFCON_Message_Command)):
      return False
      
    cmdType = command.GetCmdType()
    if (cmdType == DEFCON_CmdType.NONE):
      DEFCON_Debugging.Error(" **SERVER** Rejected command with type NONE")
    elif (cmdType == DEFCON_CmdType.SERVER_SHUTDOWN):
      self._ServerShutdown = True
      DEFCON_Debugging.Debug(" **SERVER** Shutting down...")
      return True
    else:
      DEFCON_Debugging.Error(" **SERVER** Server does not handle command with type {!r}".format(cmdType))
      return False
  