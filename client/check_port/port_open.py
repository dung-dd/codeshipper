import os, subprocess, logging, re

logger = logging.getLogger(__file__)
FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.NOTSET)

PROGRAM = "netstat"
cmd_and_args = ["netstat", "-tpln"]

class TCPPorts(object):
	"""Check Opening Ports."""

	def __init__(self):
		super(TCPPorts, self).__init__()

	def _check_cmd(self, program):
		check = subprocess.Popen(program, stdout=subprocess.PIPE)
		__ = check.communicate()[0]
		return (check.returncode, __)

	def get_full_command(self, pid):
		cmd = ""
		check = subprocess.Popen(["ps", pid], stdout=subprocess.PIPE, shell=False)
		output = check.communicate()
		if check.returncode:
			return ""

		output = output[0].decode("utf-8")
		output = output.split("PID TTY      STAT   TIME COMMAND")

		if output[1].strip() == "":
			return ""

		output = output[1].strip().split()
		cmd = " ".join(output[4:])
		return cmd

	def parse_output(self, output):
# =================

# tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1211/nginx: master
# tcp        0      0 127.0.0.1:5939          0.0.0.0:*               LISTEN      1943/teamviewerd
# tcp        0      0 0.0.0.0:8084            0.0.0.0:*               LISTEN      1279/mono
# tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      785/systemd-resolve
# tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1185/sshd
# tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      905/cupsd
# tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      1211/nginx: master
# tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      16971/python3
# tcp6       0      0 127.0.0.1:9614          :::*                    LISTEN      2522/java
# tcp6       0      0 :::80                   :::*                    LISTEN      1211/nginx: master
# tcp6       0      0 :::22                   :::*                    LISTEN      1185/sshd
# tcp6       0      0 ::1:631                 :::*                    LISTEN      905/cupsd

# =================

		output = output.split("Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name")
		output = output[1].split("\n")

		ports = []
		for line in output:
			if not re.match("^tcp", line):
				continue
			parts = line.split()
			address = parts[3]
			pid_processName = parts[6]
			try:
				pid, processName = pid_processName.split("/", 1)
			except:
				pid, processName = "", ""

			ports.append({
				"address": address,
				"pid": pid,
				"process_name": processName,
			})
		return ports


	def run(self):
		check_cmd = self._check_cmd(PROGRAM)
		if check_cmd[0]:
			return check_cmd[1]

		logger.info("Running process ...")
		cmd_process = subprocess.Popen(cmd_and_args, stdout=subprocess.PIPE, shell=False)
		output = cmd_process.communicate()[0].decode("utf-8")

		processes = self.parse_output(output)
		for pr in processes:
			if pr["pid"]:
				pr["cmd"] = self.get_full_command(pr["pid"])

		return processes


def run():
	tcp_ports = TCPPorts()
	return tcp_ports.run()
