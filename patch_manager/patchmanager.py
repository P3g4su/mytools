import os
import subprocess
import json
import requests
from datetime import datetime

# Classe para gerenciamento de patches
class PatchManager:
    def __init__(self, servers):
        self.servers = servers
        self.patch_history = {}

    def check_updates(self, server):
        print(f"[+] Verificando atualizações em {server['host']}")
        result = subprocess.run(["ssh", f"{server['user']}@{server['host']}", "sudo apt-get update"], capture_output=True, text=True)
        updates = result.stdout
        return updates

    def apply_patches(self, server):
        print(f"[+] Aplicando patches em {server['host']}")
        result = subprocess.run(["ssh", f"{server['user']}@{server['host']}", "sudo apt-get upgrade -y"], capture_output=True, text=True)
        patches_applied = result.stdout
        self.log_patch(server, patches_applied)
        return patches_applied

    def log_patch(self, server, patches_applied):
        log_entry = {
            "server": server['host'],
            "user": server['user'],
            "timestamp": datetime.now().isoformat(),
            "patches": patches_applied
        }
        if server['host'] not in self.patch_history:
            self.patch_history[server['host']] = []
        self.patch_history[server['host']].append(log_entry)
        self.save_log()

    def save_log(self):
        with open("patch_history.json", "w") as log_file:
            json.dump(self.patch_history, log_file, indent=4)

    def download_patches(self, server):
        print(f"[+] Baixando patches para {server['host']}")
        result = subprocess.run(["ssh", f"{server['user']}@{server['host']}", "sudo apt-get -d upgrade"], capture_output=True, text=True)
        download_output = result.stdout
        return download_output

    def verify_patches(self, server):
        print(f"[+] Verificando a integridade dos patches em {server['host']}")
        # Exemplo de verificação de integridade dos patches (simplificado)
        result = subprocess.run(["ssh", f"{server['user']}@{server['host']}", "sudo debsums -s"], capture_output=True, text=True)
        integrity_check = result.stdout
        if not integrity_check:
            print(f"[+] Todos os patches em {server['host']} foram aplicados corretamente.")
        else:
            print(f"[!] Problemas encontrados nos patches em {server['host']}:")
            print(integrity_check)

    def manage_patches(self):
        for server in self.servers:
            updates = self.check_updates(server)
            if "upgradable" in updates:
                print(f"[+] Patches disponíveis para {server['host']}")
                self.download_patches(server)
                self.apply_patches(server)
                self.verify_patches(server)
            else:
                print(f"[+] Nenhum patch disponível para {server['host']}")

# Lista de servidores para gerenciamento de patches
servers = [
    {"host": "192.168.1.10", "user": "admin"},
    {"host": "192.168.1.20", "user": "admin"},
    {"host": "192.168.1.30", "user": "admin"}
]

# Execução da ferramenta de gerenciamento de patches
if __name__ == "__main__":
    manager = PatchManager(servers)
    manager.manage_patches()
