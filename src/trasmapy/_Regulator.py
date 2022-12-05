class _BorgSingleton(object):
  _shared_borg_state = {}
   
  def __new__(cls, *args, **kwargs):
    obj = super(BorgSingleton, cls).__new__(cls, *args, **kwargs)
    obj.__dict__ = cls._shared_borg_state
    return obj


class Regulator(_BorgSingleton):
    def __init__(self):
        self.maxEdgeSpeed = Nan
        self.maxEdgeSpeed = Nan
