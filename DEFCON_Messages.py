################################################################
# DEFCON_Message
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS
################################################################
from DEFCON_Enums import *

################################################################
# Message
################################################################

class DEFCON_Message(object):
  _MsgID = DEFCON_MsgType.NONE
  _From = -1
  _To = -1
  
  ################################################################
  def __init__(self, sender, recipient):
    self._From = sender
    self._To = recipient
  
  ################################################################
  def GetMsgID(self):
    return self._MsgID
    
  ################################################################
  def GetSender(self):
    return self._From
    
  ################################################################
  def GetRecipient(self):
    return self._To
    
################################################################
# Command
################################################################

class DEFCON_Message_Command(DEFCON_Message):
  _CmdType = DEFCON_CmdType.NONE
  
  ################################################################
  def __init__(self, cmdType, sender, recipient):
    DEFCON_Message.__init__(self, sender, recipient)
    self._MsgID = DEFCON_MsgType.COMMAND
    self._CmdType = cmdType
    
  ################################################################
  def GetCmdType(self):
    return self._CmdType