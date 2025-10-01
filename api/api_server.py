# api/api_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os

# --- Configuration & Data Setup ---
# Use a global variable to hold the in-memory database
# In a real app, this would be a proper DB connection
try:
    with open('examples/json_schemas.json', 'r') as f:
        TRANSACTIONS_LIST = json.load(f)
except FileNotFoundError:
    print("Warning: transactions.json not found. Initializing with empty list.")
    TRANSACTIONS_LIST = []

# Create a dictionary for efficient lookup (for DSA comparison)
TRANSACTIONS_DICT = {t['id']: t for t in TRANSACTIONS_LIST}
NEXT_ID = max(TRANSACTIONS_DICT.keys()) + 1 if TRANSACTIONS_DICT else 1

# Authentication Credentials
# **INSECURE FOR REAL USE** - For assignment purposes only
USER = "admin"
PASS = "secret"
AUTH_STRING = base64.b64encode(f"{USER}:{PASS}".encode()).decode()

# --- Security Function ---
def authenticate(headers):
    """Performs Basic Authentication."""
    auth_header = headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        # auth_value is 'admin:secret' base64 encoded
        client_auth = auth_header.split(' ')[1]
        return client_auth == AUTH_STRING
    return False

# --- API Handler ---
class MoMoAPIHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if not authenticate(self.headers):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return

        if self.path == '/transactions':
            # GET /transactions (List all)
            self._send_response(200, TRANSACTIONS_LIST)
            
        elif self.path.startswith('/transactions/'):
            # GET /transactions/{id} (View one)
            try:
                # Basic path parsing for ID
                trans_id = int(self.path.split('/')[-1])
            except ValueError:
                self._send_response(400, {"error": "Invalid ID format"})
                return

            transaction = TRANSACTIONS_DICT.get(trans_id) # Using fast dictionary lookup
            
            if transaction:
                self._send_response(200, transaction)
            else:
                self._send_response(404, {"error": "Transaction not found"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if not authenticate(self.headers):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return
            
        if self.path == '/transactions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                new_transaction = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON format"})
                return

            global NEXT_ID # Use the global counter
            new_transaction['id'] = NEXT_ID
            
            # Simple validation (ensure required fields exist)
            required_fields = ['type', 'amount', 'sender', 'receiver', 'timestamp']
            if not all(field in new_transaction for field in required_fields):
                 self._send_response(400, {"error": f"Missing required fields: {', '.join(required_fields)}"})
                 return

            TRANSACTIONS_LIST.append(new_transaction)
            TRANSACTIONS_DICT[NEXT_ID] = new_transaction
            NEXT_ID += 1

            self._send_response(201, new_transaction)
        else:
             self._send_response(404, {"error": "Endpoint not found"})

    def do_PUT(self):
        if not authenticate(self.headers):
            # ... (401 Unauthorized block, same as above)
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return
            
        if self.path.startswith('/transactions/'):
            try:
                trans_id = int(self.path.split('/')[-1])
            except ValueError:
                self._send_response(400, {"error": "Invalid ID format"})
                return

            if trans_id not in TRANSACTIONS_DICT:
                self._send_response(404, {"error": "Transaction not found"})
                return

            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            
            try:
                update_data = json.loads(put_data.decode('utf-8'))
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON format"})
                return
            
            # Update the record in both data structures
            current_trans = TRANSACTIONS_DICT[trans_id]
            for key, value in update_data.items():
                if key != 'id': # Prevent ID modification
                    current_trans[key] = value

            # Update the corresponding record in the list (Linear search to find and update)
            for i, transaction in enumerate(TRANSACTIONS_LIST):
                if transaction['id'] == trans_id:
                    TRANSACTIONS_LIST[i] = current_trans
                    break
            
            self._send_response(200, current_trans)
        else:
             self._send_response(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        if not authenticate(self.headers):
            # ... (401 Unauthorized block, same as above)
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return
            
        if self.path.startswith('/transactions/'):
            try:
                trans_id = int(self.path.split('/')[-1])
            except ValueError:
                self._send_response(400, {"error": "Invalid ID format"})
                return

            if trans_id not in TRANSACTIONS_DICT:
                self._send_response(404, {"error": "Transaction not found"})
                return

            # Delete from dictionary
            del TRANSACTIONS_DICT[trans_id]

            # Delete from list (must iterate/filter)
            global TRANSACTIONS_LIST
            TRANSACTIONS_LIST = [t for t in TRANSACTIONS_LIST if t['id'] != trans_id]
            
            self._send_response(204) # No Content
        else:
             self._send_response(404, {"error": "Endpoint not found"})


def run(server_class=HTTPServer, handler_class=MoMoAPIHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting API server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping server.')

if __name__ == '__main__':
    # Ensure you run parser.py first to create transactions.json
    run()



