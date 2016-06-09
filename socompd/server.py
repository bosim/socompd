import socketserver
import shlex

from . import funcs

class MpdHandler(socketserver.BaseRequestHandler):
    allow_reuse_address = True

    def handle(self):

        while True:
            data = self.request.recv(1024)
            if not data:
                return

            data = data.decode("utf-8").strip()
            data = data.replace("\r", "").replace("\n", "")

            arr = shlex.split(data)
            
            if len(arr) > 0:
                cmd = arr[0]
                args = arr[1:]

                if cmd.lower() == "quit":
                    return

                for (name, func,) in funcs.items():
                    if name.lower() == cmd.lower():
                        result = func(*args)
                        if result:
                            self.request.sendall(bytes(result, "utf-8"))

                        self.request.sendall(bytes("OK\n", "utf-8"))

                
