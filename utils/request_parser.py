from flask import jsonify

"""Parse request payloads
"""

class Parser:
    def __init__(self, payload):
        self.payload = payload
        self.items = {}
        self.errors = {}
        self.valid = True

    
    def add_item(self, item, required=False, help=None):
        """Add an item to be parsed
        """
        if required:
            # If a required item was not sent with the request body invalidate the payload
            if self.payload.get(item) is None:
                self.errors[item] = help
                self.valid = False
                return
            
        self.items[item] = self.payload.get(item)

    
    def get_items(self):
        """Retrieve all payload items
        """
        return self.items
    

    def generate_errors(self, message, status_code):
        """Generate errors in a http response to the client
        """
        return jsonify({
            'message': message,
            'status': False,
            'errors': self.errors
        }), status_code
            
