# serve_visualizer.py
import os
import sys
import socket
import webbrowser
import http.server
import socketserver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def find_available_port(start_port=8080):
    port = start_port
    while port < 8200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1
    return 8080

def main():
    port = find_available_port(8080)
    url = f"http://localhost:{port}/visualizer.html"
    
    handler = http.server.SimpleHTTPRequestHandler
    
    print("=" * 70)
    print("  Avian 3D Acoustic Explorer - Bird Voice Frequency Visualizer")
    print(f"  Dataset: Western Mediterranean Wetlands (Zenodo 7505820)")
    print(f"  Server running at: {url}")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 70)

    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Note: Could not automatically open browser ({e}). Please open {url} manually.")

    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")

if __name__ == '__main__':
    main()
