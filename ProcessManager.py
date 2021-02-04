
import subprocess
import time
from asynchronousfilereader import AsynchronousFileReader

__version__ = '0.0.1'

class ProcessManager(object):

    def __init__(self):
        self._command = None
        self._process = None
        self._stdout = None
        self._stderr = None

    def start_process(self, command):
        
        self._command = command

        print("start process '%s'" % self._command)

        try:
           
            self._process = subprocess.Popen(self._command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self._stdout = AsynchronousFileReader(self._process.stdout, autostart=True)
            #self._stderr = AsynchronousFileReader(self._process.stderr, autostart=True)

        except Exception:
            print("startup of '%s' failed" % self._command)

    
    def stop_process(self):

        print("stop process '%s'" % self._command)

        self._stdout.join()
        #self._stderr.join()

        self._process.stdout.close()
        #self._process.stderr.close()

    def get_stdout(self):

        lines = []

        while self.is_running():
            try:
                while not self._stdout.eof():
                    for line in self._stdout.readlines():
                        lines.append(line)
                    yield lines
                    lines = []
                    time.sleep(.1)
            except KeyboardInterrupt:
                self.stop_process()

    def is_running(self):
        return self._process.poll() is None
