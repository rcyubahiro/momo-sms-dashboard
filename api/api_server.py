from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os
from urllib.parse import urlparse, parse_qs   

# Load Transactions from JSON file 
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'examples', 'json_schemas.json')

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        TRANSACTIONS_LIST = json.load(f)
else:
    TRANSACTIONS_LIST = []

# Dictionary for fast lookup by ID
TRANSACTIONS_DICT = {t['id']: t for t in TRANSACTIONS_LIST}
NEXT_ID = max(TRANSACTIONS_DICT.keys()) + 1 if TRANSACTIONS_DICT else 1


#  Save transactions back to JSON file to persist changes
def save_transactions():
    with open(DATA_FILE, 'w') as f:
        json.dump(TRANSACTIONS_LIST, f, indent=4)


# Basic Authentication 
USERNAME = "admin"
PASSWORD = "secret"
AUTH_STRING = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

def authenticate(headers):
    auth_header = headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Basic '):
        return False
    client_auth = auth_header.split(' ')[1]
    return client_auth == AUTH_STRING


# Request Handler 
class MoMoAPIHandler(BaseHTTPRequestHandler):

    #  Utility to extract ID cleanly from path
    def get_id_from_path(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/')
        if len(parts) == 2 and parts[0] == 'transactions':
            try:
                return int(parts[1])
            except ValueError:
                return None
        return None

    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    def _unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.end_headers()
        self.wfile.write(b'{"error":"Unauthorized"}')


    def do_GET(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        parsed = urlparse(self.path)
        if parsed.path == "/transactions":
            # Optional timestamp filtering using query parameters
            params = parse_qs(parsed.query)
            start = params.get("start", [None])[0]
            end = params.get("end", [None])[0]

            results = TRANSACTIONS_LIST
            if start:
                results = [t for t in results if t['timestamp'] >= start]
            if end:
                results = [t for t in results if t['timestamp'] <= end]

            self._send_response(200, results)
            return

        # GET by ID
        trans_id = self.get_id_from_path()
        if trans_id is not None:
            transaction = TRANSACTIONS_DICT.get(trans_id)
            if transaction:
                self._send_response(200, transaction)
            else:
                self._send_response(404, {"error": "Transaction not found"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

 
    def do_POST(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        if self.path == "/transactions":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            try:
                new_trans = json.loads(body.decode())
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON"})
                return

            global NEXT_ID
            new_trans['id'] = NEXT_ID
            NEXT_ID += 1

            required_fields = ['type', 'amount', 'sender', 'receiver', 'timestamp']
            if not all(field in new_trans for field in required_fields):
                self._send_response(400, {"error": "Missing fields"})
                return

            TRANSACTIONS_LIST.append(new_trans)
            TRANSACTIONS_DICT[new_trans['id']] = new_trans

            save_transactions()   

            self._send_response(201, new_trans)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

   
    def do_PUT(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        trans_id = self.get_id_from_path()
        if trans_id is None:
            self._send_response(400, {"error": "Invalid ID"})
            return

        if trans_id not in TRANSACTIONS_DICT:
            self._send_response(404, {"error": "Transaction not found"})
            return

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            updates = json.loads(body.decode())
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return

        # Update in dict and list
        transaction = TRANSACTIONS_DICT[trans_id]
        for key, value in updates.items():
            if key != 'id':
                transaction[key] = value

        for i, t in enumerate(TRANSACTIONS_LIST):
            if t['id'] == trans_id:
                TRANSACTIONS_LIST[i] = transaction
                break

        save_transactions()  

        self._send_response(200, transaction)

   
    def do_DELETE(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        trans_id = self.get_id_from_path()
        if trans_id is None:
            self._send_response(400, {"error": "Invalid ID"})
            return

        if trans_id not in TRANSACTIONS_DICT:
            self._send_response(404, {"error": "Transaction not found"})
            return

        del TRANSACTIONS_DICT[trans_id]
        global TRANSACTIONS_LIST
        TRANSACTIONS_LIST = [t for t in TRANSACTIONS_LIST if t['id'] != trans_id]

        save_transactions()  
        self._send_response(204)



def run(port=8080):
    server = HTTPServer(('', port), MoMoAPIHandler)
    print(f" Server running on http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
