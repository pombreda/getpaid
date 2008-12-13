from AccessControl.User import SimpleUser
from AccessControl.SecurityManagement import getSecurityManager, newSecurityManager

class UserAsManager(SimpleUser):
   """Give the current user manager role
   """
   def __init__(self, user):
       self.name = user.getUserName()
       self.__ = "wrongPass"
       self.domains = user.getDomains()
       roles = list(user.getRoles())
       roles.append('Manager')
       self.roles = tuple(roles)

def invokeFunctionAsManager(request, function, *args, **kwargs):
    user = getSecurityManager().getUser()
    manager = UserAsManager(user)
    newSecurityManager(request, manager)
    apply(function, args, kwargs)
    newSecurityManager(request, user)
