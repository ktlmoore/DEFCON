################################################################
# DEFCON_Client
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS
################################################################
# Python
import getpass
import threading

# DEFCON
import DEFCON_Debugging
from DEFCON_Enums import *
from DEFCON_Network import *
from DEFCON_Messages import *
import DEFCON_UserSystem

################################################################
AssetsFileName = "Assets.txt"
HeaderAssetName = "Header"
HelpAssetName = "Help"

################################################################
# Client class 
################################################################

class DEFCON_Client(threading.Thread):
  _ClientId = -1
  _ClientShutdown = False
  
  _Assets = {}
  
  _OperationBindings = {}
  
  ################################################################
  def __init__(self, clientId):
    DEFCON_Debugging.Debug("  ~CLIENT {}~ Initialising...".format(clientId))
    threading.Thread.__init__(self)
    self._ClientId = clientId
    self.daemon = True
    DEFCON_Network.RegisterClient(self)
    
    self.ReadAssets()
    
    self._OperationBindings["login"] = self.Login
    self._OperationBindings["help"] = self.Help
    self._OperationBindings["exit"] = self.Exit
    
    DEFCON_Debugging.Debug("  ~CLIENT {}~ Initialised!".format(clientId))
    
  ################################################################
  def ReadAssets(self):
    fileReader = open(AssetsFileName, "r")
    
    # Go through the file and create assets marked up by >>>
    reading = False
    asset = ""
    assetName = ""
    for line in fileReader:
      if (not reading):
        # If we're not already reading we should ignore until a line starts with a >>>
        if (line.startswith(">>>")):
          reading = True
          assetName = line[3:-1]
      else:
        # We are reading, do a reading thing
        if (line.startswith(">>>")):
          reading = False
          self._Assets[assetName] = asset
          asset = ""
          assetName = ""
        else:
          asset += line
      
    # If we end a file half way through an asset we should complain and ditch the asset
    fileReader.close()
    
  ################################################################
  def CheckMessageType(self, objToCheck, expectedType):
    if (not isinstance(objToCheck, expectedType)):
      DEFCON_Debugging.Error("  ~CLIENT {}~ Rejected message ({!r}) as it was not a {}".format(self._ClientId, objToCheck, expectedType))
      return False
    return True
    
  ################################################################
  def GetId(self):
    return self._ClientId
    
  ################################################################
  def HandleMessage(self, message):
    if (not self.CheckMessageType(message, DEFCON_Message)):
      return False
    
    msgId = message.GetMsgID()
    if (msgId == DEFCON_MsgType.NONE):
      DEFCON_Debugging.Error("  ~CLIENT {}~ Rejected message as it had type NONE".format(self._ClientId))
      return False
    elif (msgId == DEFCON_MsgType.REQUEST):
      DEFCON_Debugging.Error("  ~CLIENT {}~ Rejected message as it had type REQUEST".format(self._ClientId))
      return False
    elif (msgId == DEFCON_MsgType.RESPONSE):
      return True
    elif (msgId == DEFCON_MsgType.COMMAND):
      return self.HandleCommand(message)
    else:
      DEFCON_Debugging.Error("  ~CLIENT {}~ Error, could not handle message with type {:d}".format(self._ClientId, msgId))
      return False
      
  ################################################################    
  def HandleCommand(self, command):
    # Check we have a command
    if (not self.CheckMessageType(command, DEFCON_Message_Command)):
      return False
      
    cmdType = command.GetCmdType()
    if (cmdType == DEFCON_CmdType.NONE):
      DEFCON_Debugging.Error("  ~CLIENT {}~ Rejected command with type NONE".format(self._ClientId))
    elif (cmdType == DEFCON_CmdType.CLIENT_SHUTDOWN):
      self._ClientShutdown = True
      DEFCON_Debugging.Debug("  ~CLIENT {}~ Shutting down...".format(self._ClientId))
      return True
    else:
      DEFCON_Debugging.Error("  ~CLIENT {}~ Client does not handle command with type {!r}".format(self._ClientId, cmdType))
      return False
      
  ################################################################
  def PrintAsset(self, assetName):
    if (assetName != "" and self._Assets[assetName]):
      self.Print(self._Assets[assetName])
    else:
      self.Print("")
      
  ################################################################
  def Print(self, text):
    print "+------------------------------------------+"
    if (text != ""):
      if (text[-1:] != '\n'):
        print text
      else:
        print text,
    print "+------------------------------------------+"
    
  ################################################################
  def Help(self):
    self.PrintAsset(HelpAssetName)
    
  ################################################################
  def Login(self):
    self.Print("")
    username = raw_input("@ Username: ")
    passkey = raw_input("@ Pass key: ")
    if (DEFCON_UserSystem.DoLogin(username, passkey)):
      self.Print("Welcome, {}".format(DEFCON_UserSystem.GetCurrentUsername()))
    else:
      self.Print("INCORRECT LOGIN")
  
  ################################################################    
  def Exit(self):
    msg = DEFCON_Message_Command(DEFCON_CmdType.SERVER_SHUTDOWN, self._ClientId, DEFCON_Ids.SERVER)
    DEFCON_Network.ReceiveMessage(msg)
    self._ClientShutdown = True
    
  ################################################################
  def WhoAmI(self):
    self.Print("You are {}".format(DEFCON_UserSystem.GetCurrentUsername()))
  
  ################################################################
  def run(self):
    DEFCON_Debugging.Debug("  ~CLIENT {}~ Starting thread {}".format(self._ClientId, self.name))
    
    self.PrintAsset(HeaderAssetName)
      
    while (not self._ClientShutdown):
      x = raw_input("@ {}: ".format(DEFCON_UserSystem.GetCurrentUsername()))
      x = x.lower()
      
      if (x in self._OperationBindings):
        self._OperationBindings[x]()
        
                
    DEFCON_Debugging.Debug("  ~CLIENT {}~ Exiting thread {}".format(self._ClientId, self.name))

