import json
class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        
        # Convert objects to a dictionary of their representation
        d = { '__class__':obj.__class__.__name__,
              '__module__':obj.__module__,
              }
        d.update(obj.__dict__)
        return d
