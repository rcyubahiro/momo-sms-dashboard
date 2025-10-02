# api/api_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os


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

    # -------------------- get method --------------------
    def do_GET(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        if self.path == "/transactions":
            self._send_response(200, TRANSACTIONS_LIST)
        elif self.path.startswith("/transactions/"):
            try:
                trans_id = int(self.path.split("/")[-1])
            except ValueError:
                self._send_response(400, {"error": "Invalid ID"})
                return

            transaction = TRANSACTIONS_DICT.get(trans_id)
            if transaction:
                self._send_response(200, transaction)
            else:
                self._send_response(404, {"error": "Transaction not found"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    #post method 
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

            self._send_response(201, new_trans)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    # PUT
    def do_PUT(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        if self.path.startswith("/transactions/"):
            try:
                trans_id = int(self.path.split("/")[-1])
            except ValueError:
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

            self._send_response(200, transaction)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    # -------------------- DELETE --------------------
    def do_DELETE(self):
        if not authenticate(self.headers):
            self._unauthorized()
            return

        if self.path.startswith("/transactions/"):
            try:
                trans_id = int(self.path.split("/")[-1])
            except ValueError:
                self._send_response(400, {"error": "Invalid ID"})
                return

            if trans_id not in TRANSACTIONS_DICT:
                self._send_response(404, {"error": "Transaction not found"})
                return

            del TRANSACTIONS_DICT[trans_id]
            global TRANSACTIONS_LIST
            TRANSACTIONS_LIST = [t for t in TRANSACTIONS_LIST if t['id'] != trans_id]

            self._send_response(204)
        else:
            self._send_response(404, {"error": "Endpoint not found"})


# Start Server

def run(port=8080):
    server = HTTPServer(('', port), MoMoAPIHandler)
    print(f" Server running on http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
