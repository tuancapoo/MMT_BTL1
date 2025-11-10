"""
chatapp.py
----------------
Hybrid Chat Application using WeApRous + socket-based P2P
Course: CO3094 - Computer Networks

This program provides:
 - Client–Server functions (register peers, get list)
 - Peer–to–Peer communication (direct chat between peers)
"""

# import threading
# import json
import socket
# import argparse

from daemon.weaprous import WeApRous

PORT = 8000  # Default port

app = WeApRous()

TRACKER_IP = "0.0.0.0"
TRACKER_PORT = 8000
PEER_PORT = 9001   # Each peer can choose its own
peers = {}         # {peer_name: (ip, port)}

app = WeApRous()

# SERVER-SIDE (Client–Server paradigm)

@app.route('/login', methods=['POST'])
def login(headers, body):
    try:
        data = json.loads(body)
        name = data.get('name')
        ip = data.get('ip')
        port = data.get('port')

        if not all([name, ip, port]):
            return {"status": "error", "msg": "Missing name/ip/port"}

        peers[name] = (ip, port)
        print(f"[REGISTER] {name} -> {ip}:{port}")
        return {"status": "ok", "total_peers": len(peers)}

    except Exception as e:
        return {"status": "error", "msg": str(e)}


@app.route('/get-list', methods=['GET'])
def get_list(headers, body):
    # Return list of all registered peers
    return {"peers": peers}


@app.route('/unregister', methods=['POST'])
def unregister(headers, body):
    # Remove a peer from registry
    data = json.loads(body)
    name = data.get("name")
    if name in peers:
        peers.pop(name)
        print(f"[UNREGISTER] {name}")
        return {"status": "ok"}
    return {"status": "not_found"}


# PEER-TO-PEER (Direct Socket Messaging)

def start_peer_listener(my_name, my_ip="0.0.0.0", my_port=PEER_PORT):
    # Start a local peer socket server that listens for incoming messages
    def handle_client(conn, addr):
        try:
            data = conn.recv(1024).decode()
            msg = json.loads(data)
            print(f"\n Message from {msg.get('from')}@{addr}: {msg.get('text')}")
        except Exception as e:
            print(f"Error receiving msg: {e}")
        finally:
            conn.close()

    def server_thread():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((my_ip, my_port))
        s.listen(5)
        print(f"[PEER] {my_name} listening on {my_ip}:{my_port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    threading.Thread(target=server_thread, daemon=True).start()


def send_to_peer(target_ip, target_port, from_name, message):
    # Send a message to another peer directly
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, int(target_port)))
        payload = json.dumps({"from": from_name, "text": message})
        s.send(payload.encode())
        s.close()
        print(f"Sent to {target_ip}:{target_port}")
    except Exception as e:
        print(f"[ERROR] send_to_peer: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hybrid Chat Application")
    parser.add_argument("--mode", choices=["server", "peer"], default="server")
    parser.add_argument("--name", default="peer1")
    parser.add_argument("--ip", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=PEER_PORT)
    args = parser.parse_args()

    if args.mode == "server":
        # Launch centralized tracker (client-server mode)
        print(f"[TRACKER] Running on {TRACKER_IP}:{TRACKER_PORT}")
        app.prepare_address(TRACKER_IP, TRACKER_PORT)
        app.run()

    elif args.mode == "peer":
        # Run as peer process (P2P mode)
        start_peer_listener(args.name, args.ip, args.port)
        print(f"[{args.name}] Ready to chat. Use send_to_peer(ip, port, name, msg)")
        while True:
            cmd = input(">> ").strip()
            if cmd.lower().startswith("send"):
                # Example: send 127.0.0.1 9001 hello world
                parts = cmd.split(" ", 3)
                if len(parts) == 4:
                    _, ip, port, msg = parts
                    send_to_peer(ip, port, args.name, msg)
            elif cmd.lower() == "exit":
                break
