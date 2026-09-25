import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret123"


def authenticate_credentials(auth_header):
    if not auth_header or not auth_header.startswith("Basic "):
        return False
    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD
    except Exception:
        return False


def load_db():
    try:
        with open("api/mock_db.json", "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_db(data):
    with open("api/mock_db.json", "w") as f:
        json.dump(data, f, indent=4)


class RESTApiHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, body):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode("utf-8"))

    def _check_auth(self):
        auth_header = self.headers.get("Authorization")
        if not authenticate_credentials(auth_header):
            self.send_response(401)
            self.send_header(
                "WWW-Authenticate", 'Basic realm="MoMo REST API Protection"'
            )
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "error": "Unauthorized",
                "message": "Invalid or missing Basic Authentication credentials.",
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return False
        return True

    def do_GET(self):
        if not self._check_auth():
            return

        db = load_db()
        path_parts = [p for p in self.path.split("/") if p]

        if len(path_parts) == 1 and path_parts[0] == "transactions":
            self._send_response(200, db)
        elif len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                tx_id = int(path_parts[1])
                record = next((t for t in db if t.get("id") == tx_id), None)
                if record:
                    self._send_response(200, record)
                else:
                    self._send_response(
                        404,
                        {"error": "Not Found", "message": "Transaction not found"},
                    )
            except ValueError:
                self._send_response(
                    400,
                    {"error": "Bad Request", "message": "ID must be an integer"},
                )
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if not self._check_auth():
            return

        if self.path == "/transactions":
            try:
                db = load_db()
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                post_data = json.loads(body) if body else {}

                new_id = max([t.get("id", 0) for t in db], default=0) + 1
                post_data["id"] = new_id
                db.append(post_data)
                save_db(db)

                self._send_response(201, post_data)
            except json.JSONDecodeError:
                self._send_response(
                    400,
                    {"error": "Bad Request", "message": "Invalid JSON payload"},
                )
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_PUT(self):
        if not self._check_auth():
            return

        path_parts = [p for p in self.path.split("/") if p]
        if len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                tx_id = int(path_parts[1])
                db = load_db()
                record = next((t for t in db if t.get("id") == tx_id), None)

                if record:
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length).decode("utf-8")
                    update_data = json.loads(body) if body else {}

                    record.update(update_data)
                    record["id"] = tx_id
                    save_db(db)

                    self._send_response(200, record)
                else:
                    self._send_response(
                        404,
                        {"error": "Not Found", "message": "Transaction not found"},
                    )
            except ValueError:
                self._send_response(
                    400,
                    {"error": "Bad Request", "message": "ID must be an integer"},
                )
            except json.JSONDecodeError:
                self._send_response(
                    400,
                    {"error": "Bad Request", "message": "Invalid JSON payload"},
                )
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        if not self._check_auth():
            return

        path_parts = [p for p in self.path.split("/") if p]
        if len(path_parts) == 2 and path_parts[0] == "transactions":
            try:
                tx_id = int(path_parts[1])
                db = load_db()
                initial_len = len(db)
                db = [t for t in db if t.get("id") != tx_id]

                if len(db) < initial_len:
                    save_db(db)
                    self._send_response(
                        200,
                        {"message": f"Transaction {tx_id} deleted successfully"},
                    )
                else:
                    self._send_response(
                        404,
                        {"error": "Not Found", "message": "Transaction not found"},
                    )
            except ValueError:
                self._send_response(
                    400,
                    {"error": "Bad Request", "message": "ID must be an integer"},
                )
        else:
            self._send_response(404, {"error": "Endpoint not found"})


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RESTApiHandler)
    print(f"Starting MoMo REST API Server on http://localhost:{port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()