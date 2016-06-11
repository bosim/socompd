import socketserver

import shlex

from . import funcs, idle_command

class MpdHandler(socketserver.BaseRequestHandler):
    def processCommand(self, cmd, args, command_list=False):
        cmd_found = False

        for (name, func,) in funcs.items():
            if name.lower() == cmd.lower():
                result = func(*args)

                if not command_list:
                    if result:
                        self.request.sendall(bytes(result, "utf-8"))
                        
                    self.request.sendall(bytes("OK\n", "utf-8"))
                                
                cmd_found = True

        return cmd_found

    def handle(self):
        welcome=u"OK MPD 0.12.0\n"
        self.request.sendall(bytes(welcome, "utf-8"))

        while True:
            data = self.request.recv(4096)
            if not data:
                return

            data = data.decode("utf-8").strip()
            command_list = False

            for line in data.split("\n"):
                line = line.replace("\r", "")
                arr = shlex.split(line)
                
                if len(arr) > 0:
                    cmd = arr[0]
                    args = arr[1:]
                    
                    if cmd.lower() == "quit":
                        return

                    elif cmd.lower() == "idle":
                        self.request.settimeout(0.1)

                        idle_command[0](self.request)
                        self.request.sendall(bytes("OK\n", "utf-8"))

                        self.request.settimeout(None)
                    elif cmd.lower() == "command_list_begin":
                        command_list = True
                        continue
                    elif cmd.lower() == "command_list_end":
                        command_list = False
                        self.request.sendall(bytes("OK\n", "utf-8"))
                    else:
                        if not self.processCommand(cmd, args, command_list):
                            error_str = "ACK Command not found %s\n" % cmd
                            self.request.sendall(bytes(error_str, "utf-8"))
                            print("Unknown command %s\n" % cmd)
                    
