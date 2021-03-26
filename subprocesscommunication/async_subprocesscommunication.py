import subprocess
import threading
import asyncio


class AsyncServerCommunication:
    """
    A class for abstracting away sending commands to and receiving output from the server
    """
    def __init__(self, loop, command, on_output, on_stderr, on_close, cwd="."):
        """
        :param loop: asyncio event loop
        :param command: the command to start the server with
        :param cwd: the working directory for the server
        :param on_output: called with the line as only argument on server console output
        :param on_close: called when the server closed
        """
        self.loop = loop
        self.command = command
        self.cwd = cwd
        self.process = None
        self.on_output = on_output
        self.on_close = on_close
        self.running = False
        self.on_stderr = on_stderr

    async def begin(self) -> None:
        """
        starts the server
        """
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=self.cwd, stderr=subprocess.PIPE)
        self.running = True
        # pass on_close only to one watcher to prevent double calling
        AsyncStreamWatcher(self.loop, self.process.stdout, self.process, self.on_output, self.on_close).start()
        AsyncStreamWatcher(self.loop, self.process.stdout, self.process, self.on_stderr, None).start()

    async def write_stdin(self, cmd) -> None:
        """
        writes a command to server stdin and flushes it
        :param cmd: the command to send
        """
        if not self.running:
            return
        self.process.stdin.write(cmd.encode("ascii") + b'\n')
        self.process.stdin.flush()


class AsyncStreamWatcher(threading.Thread):
    """
    watches an filestream for new lines and calls callback for each line
    """
    def __init__(self, loop, stream, proc, on_out, on_close):
        """
        :param loop: event loop to run callbacks in
        :param stream: file steam to watch
        :param proc: the process the stream is from
        :param on_out: callback for each line
        :param on_close: callback on close, can be None
        """
        super(AsyncStreamWatcher, self).__init__()
        self.loop = loop
        self.stream = stream
        self.proc = proc
        self.on_close = on_close
        self.on_out = on_out

    def run(self) -> None:
        """
        iterates over output lines and runs callbacks
        """
        for line in iter(self.stream.readline, ""):
            if self.proc.poll() is not None:
                break
            if line:
                asyncio.run_coroutine_threadsafe(self.on_out(line.decode()), self.loop)
        if self.on_close is not None:
            asyncio.run_coroutine_threadsafe(self.on_close(), self.loop)
