def display_top_10_passwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            passwords = file.readlines()
            for i in range(10):
                print(passwords[i].strip())
    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
file_path = 'SecLists/Passwords/darkweb2017-top100.txt'
display_top_10_passwords(file_path)