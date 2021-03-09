import subprocess
import threading
from typing import Callable


class ProcessCommunication:
    """
    A class for abstracting away sending commands to and receiving output from the server
    """
    def __init__(self, command, cwd=".", on_output=lambda line: print(line, end=""), on_close=lambda: print("process communication ended")):
        """
        :param command: the command to start the process
        :param cwd: the working directory for the process
        :param on_output: called with the line as only argument on console output
        :param on_close: called when the subprocess ended
        """
        self.command: str = command
        self.cwd: str = cwd
        self.process: subprocess.Popen = None
        self.on_output: Callable = on_output
        self.on_close: Callable = on_close
        self.running: bool = False

    def begin(self) -> None:
        """
        starts the subprocess
        """
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=self.cwd)
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()

    def run(self) -> None:
        """
        calls the on_output callback for every line on the processes output while it's running
        """
        for line in iter(self.process.stdout.readline, ""):
            if self.process.poll() is not None:
                break
            if line:
                self.on_output(line.decode())
        self.running = False
        self.on_close()

    def write_stdin(self, cmd) -> None:
        """
        writes a line to process stdin and flushes it
        :param cmd: the command to send
        """
        if not self.running:
            return
        self.process.stdin.write(cmd.encode("ascii") + b'\n')
        self.process.stdin.flush()
