################################################################
# DEFCON_Network
# (C) Tom Moore 2017
################################################################

################################################################
# IMPORTS
################################################################
# Python
from collections import deque
import threading

# DEFCON 
import DEFCON_Debugging
from DEFCON_Enums import *
from DEFCON_Messages import *
from DEFCON_Server import DEFCON_Server

################################################################
# Network class
################################################################

class DEFCON_Network(threading.Thread):
  # This
  _Network = None
  
  # Our server entity
  _Server = None
  _Clients = deque([])
  
  # Our message queue
  _MessageQueue = []
  
  ################################################################
  def __init__(self):
    DEFCON_Debugging.Debug("+++NETWORK+++ Initialising...")
    
    threading.Thread.__init__(self)

    self._Server = DEFCON_Server()
    self._MessageQueue = deque([])
    self._Clients = deque([])
    
    DEFCON_Network._Network = self
    
    DEFCON_Debugging.Debug("+++NETWORK+++ Initialised!")
  
  ################################################################
  def run(self):
    DEFCON_Debugging.Debug("+++NETWORK+++ Starting thread " + self.name)
    
    while (not self._Server.GetShutdown()):
      if (len(self._MessageQueue) > 0):
        self.HandleMessage(self._MessageQueue.popleft())
        
    self.Shutdown()
    
    DEFCON_Debugging.Debug("+++NETWORK+++ Shutting down thread " + self.name)
    
  ################################################################
  def Shutdown(self):
    for client in self._Clients:
      msg = DEFCON_Message_Command(DEFCON_CmdType.CLIENT_SHUTDOWN, DEFCON_Ids.SERVER, client.GetId())
      client.HandleMessage(msg)
    
  ################################################################
  def HandleMessage(self, msg):
    # Early out if we haven't been sent a message
    if (not isinstance(msg, DEFCON_Message)):
      return False
      
    recipient = msg.GetRecipient()
    if (recipient == DEFCON_Ids.SERVER):
      return self._Server.HandleMessage(msg)
      
    return False
    
  ################################################################
  # Static Methods
  ################################################################
  @staticmethod
  def ReceiveMessage(msg):
    DEFCON_Network._Network._MessageQueue.append(msg)
    
  @staticmethod
  def RegisterClient(client):
    DEFCON_Network._Network._Clients.append(client)
    
    