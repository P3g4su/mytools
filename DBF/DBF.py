import hashlib
import itertools
import threading

class DistributedBruteForce:
    def __init__(self, hash_target, charset, max_length, nodes):
        self.hash_target = hash_target
        self.charset = charset
        self.max_length = max_length
        self.nodes = nodes
        self.found = False

    def generate_combinations(self, length):
        return itertools.product(self.charset, repeat=length)

    def hash_and_compare(self, attempt):
        attempt_str = ''.join(attempt)
        attempt_hash = hashlib.sha256(attempt_str.encode()).hexdigest()
        if attempt_hash == self.hash_target:
            print(f"[+] Senha encontrada: {attempt_str}")
            self.found = True

    def brute_force_worker(self, length):
        for combination in self.generate_combinations(length):
            if self.found:
                break
            self.hash_and_compare(combination)

    def distribute_load(self):
        for length in range(1, self.max_length + 1):
            if self.found:
                break
            threads = []
            for node in self.nodes:
                t = threading.Thread(target=self.brute_force_worker, args=(length,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

# Execução da ferramenta de força bruta distribuída
if __name__ == "__main__":
    hash_target = "b59c67bf196a4758191e42f76670ceba"  # hash SHA-256 de "password"
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    max_length = 6
    nodes = ["node1", "node2", "node3"]

    brute_force_tool = DistributedBruteForce(hash_target, charset, max_length, nodes)
    brute_force_tool.distribute_load()
