################################################################
# DEFCON_UserSystem
# (C) Tom Moore 2017
################################################################

# Static
_CurrentUsername = "Client"
_UserDatabase = {}

def GetCurrentUsername():
  return _CurrentUsername

def DoLogin(username, passkey):
  global _CurrentUsername
  
  if (username in _UserDatabase and _UserDatabase[username] == passkey):
    _CurrentUsername = username
    return True
  return False

def PopulateUserDatabase():
  _UserDatabase["fred"] = "123"
  _UserDatabase["stanley"] = "456"