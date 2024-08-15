import requests

def check_subdomains(base_url, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            subdomains = [line.strip() for line in file.readlines()[:20]]

        for subdomain in subdomains:
            url = f"http://{subdomain}.{base_url}"
            try:
                response = requests.get(url)
                print(f"{url} - Status Code: {response.status_code}")
            except requests.RequestException as e:
                print(f"{url} - Request failed: {e}")

    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
base_url = 'example.com'
file_path = 'SecLists/Discovery/DNS/subdomains-top1million-5000.txt'
check_subdomains(base_url, file_path)