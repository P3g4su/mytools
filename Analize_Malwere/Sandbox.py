import os
import subprocess
import json
import tempfile
from datetime import datetime

class MalwareSandbox:
    def __init__(self, malware_path):
        self.malware_path = malware_path
        self.execution_log = {}

    def create_sandbox(self):
        print("[+] Criando ambiente sandbox...")
        self.sandbox_dir = tempfile.mkdtemp(prefix="sandbox_")
        subprocess.run(["cp", self.malware_path, self.sandbox_dir])

    def execute_malware(self):
        print(f"[+] Executando malware em sandbox: {self.sandbox_dir}")
        malware_exec_path = os.path.join(self.sandbox_dir, os.path.basename(self.malware_path))
        start_time = datetime.now().isoformat()
        result = subprocess.run([malware_exec_path], capture_output=True, text=True)
        end_time = datetime.now().isoformat()

        self.execution_log = {
            "start_time": start_time,
            "end_time": end_time,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
        self.save_log()

    def monitor_behavior(self):
        print(f"[+] Monitorando comportamento de {self.malware_path}")
        # Captura tráfego de rede (exemplo básico)
        pcap_file = os.path.join(self.sandbox_dir, "traffic.pcap")
        subprocess.run(["tcpdump", "-w", pcap_file, "-i", "any", "-G", "30", "-W", "1", "tcp"])

        # Verifica modificações no sistema de arquivos
        modified_files = subprocess.run(["find", self.sandbox_dir, "-type", "f", "-mmin", "-1"], capture_output=True, text=True).stdout
        self.execution_log["modified_files"] = modified_files

    def save_log(self):
        log_file = os.path.join(self.sandbox_dir, "execution_log.json")
        with open(log_file, "w") as f:
            json.dump(self.execution_log, f, indent=4)

    def clean_up(self):
        print("[+] Limpando ambiente sandbox...")
        subprocess.run(["rm", "-rf", self.sandbox_dir])

    def run(self):
        self.create_sandbox()
        self.execute_malware()
        self.monitor_behavior()
        self.clean_up()

# Execução da sandbox
if __name__ == "__main__":
    malware_path = "/caminho/para/malware"
    sandbox = MalwareSandbox(malware_path)
    sandbox.run()
