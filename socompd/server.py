import socketserver

import shlex

from . import funcs, idle_command

class MpdHandler(socketserver.BaseRequestHandler):
    def handle(self):
        welcome=u"OK MPD 0.16.0\n"
        self.request.sendall(bytes(welcome, "utf-8"))

        while True:
            data = self.request.recv(1024)
            if not data:
                return

            print("Read data %s" % data)

            data = data.decode("utf-8").strip()
            data = data.replace("\r", "").replace("\n", "")

            arr = shlex.split(data)
            
            if len(arr) > 0:
                cmd = arr[0]
                args = arr[1:]

                if cmd.lower() == "quit":
                    return

                if cmd.lower() == "idle":
                    import pdb; pdb.set_trace()
                    self.request.settimeout(0.1)

                    idle_command(self.request)
                    self.request.sendall(bytes("OK\n", "utf-8"))

                    self.request.settimeout(None)

                cmd_found = False

                for (name, func,) in funcs.items():
                    if name.lower() == cmd.lower():
                        result = func(*args)
                        if result:
                            self.request.sendall(bytes(result, "utf-8"))

                        self.request.sendall(bytes("OK\n", "utf-8"))

                        cmd_found = True

                if not cmd_found:
                    error_str = "ACK Command not found %s\n" % cmd
                    self.request.sendall(bytes(error_str, "utf-8"))
                    print("Unknown command %s\n" % cmd)
                    
