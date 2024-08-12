import pyshark

# Função para capturar e analisar pacotes HTTPS
def capture_https_traffic(interface):
    print(f"Iniciando a captura de tráfego HTTPS na interface: {interface}")

    # Inicia a captura ao vivo na interface especificada, filtrando por pacotes HTTPS (porta 443)
    capture = pyshark.LiveCapture(interface=interface, bpf_filter='tcp port 443')
    
    for packet in capture.sniff_continuously():
        process_packet(packet)

# Função para processar pacotes capturados
def process_packet(packet):
    try:
        # Verifica se o pacote contém camada SSL/TLS
        if 'TLS' in packet:
            print("\n[+] Pacote SSL/TLS capturado:")
            tls_layer = packet.tls

            # Exibe informações básicas do pacote TLS
            print(f"  - Versão: {tls_layer.record_version}")
            print(f"  - Ciphersuite: {tls_layer.handshake_ciphersuite}")
            print(f"  - Extensões: {tls_layer.handshake_extensions}")

            # Análise adicional: Verificando se há informações de certificado
            if hasattr(tls_layer, 'x509af_name'):
                print(f"  - Certificado: {tls_layer.x509af_name}")

    except AttributeError as e:
        print(f"[!] Erro ao processar o pacote: {e}")

# Define a interface de captura (exemplo: "eth0" para Linux, "Wi-Fi" para Windows)
interface = "eth0"

if __name__ == "__main__":
    capture_https_traffic(interface)
