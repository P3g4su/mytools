import os
import subprocess
import sys
import time
from fpdf import FPDF
import shutil
import matplotlib.pyplot as plt

# Função para verificar se as ferramentas necessárias estão instaladas
def check_tools():
    tools = {
        "Nmap": "nmap",
        "Nikto": "nikto",
        "SQLMap": "sqlmap"
    }
    
    for tool_name, command in tools.items():
        if not shutil.which(command):
            print(f"Erro: {tool_name} não está instalado.")
            sys.exit(1)
    print("Todas as ferramentas necessárias estão instaladas.\n")

# Função para rodar o Nmap
def run_nmap(target):
    print(f"Executando Nmap em {target}...")
    result = subprocess.run(["nmap", "-sV", target], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    print(output)
    save_report("Nmap", output)

# Função para rodar o Nikto
def run_nikto(target):
    print(f"Executando Nikto em {target}...")
    result = subprocess.run(["nikto", "-h", target], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    print(output)
    save_report("Nikto", output)

# Função para rodar o SQLMap
def run_sqlmap(target):
    print(f"Executando SQLMap em {target}...")
    result = subprocess.run(["sqlmap", "-u", target, "--batch"], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    print(output)
    save_report("SQLMap", output)

# Função para salvar os relatórios
def save_report(tool_name, content):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"{tool_name}_report_{timestamp}.txt"
    
    with open(file_name, "w") as file:
        file.write(content)
    
    print(f"Relatório salvo como {file_name}.\n")

# Função para gerar gráficos a partir dos resultados
def generate_graphs():
    labels = ["Nmap", "Nikto", "SQLMap"]
    counts = [120, 45, 80]  # Exemplos de dados; substitua pelos reais
    
    plt.bar(labels, counts)
    plt.xlabel('Ferramentas')
    plt.ylabel('Vulnerabilidades Detectadas')
    plt.title('Resumo de Vulnerabilidades')
    plt.savefig('vulnerabilities_summary.png')
    plt.show()
    print("Gráfico de resumo gerado como vulnerabilities_summary.png.\n")

# Função para gerar o relatório PDF
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Relatório de Testes de Segurança", ln=True, align="C")
    
    tools = ["Nmap", "Nikto", "SQLMap"]
    
    for tool in tools:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"{tool}_report_{timestamp}.txt"
        
        try:
            with open(file_name, "r") as file:
                pdf.ln(10)
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, txt=f"Resultados do {tool}", ln=True)
                pdf.set_font("Arial", size=12)
                for line in file:
                    pdf.multi_cell(0, 10, line)
        except FileNotFoundError:
            print(f"Erro: {file_name} não encontrado.")
    
    pdf.image('vulnerabilities_summary.png', x=10, y=None, w=100)
    
    output_pdf = f"security_report_{timestamp}.pdf"
    pdf.output(output_pdf)
    
    print(f"Relatório PDF gerado como {output_pdf}.\n")

# Função principal que gerencia o fluxo de operações
def main():
    print("Bem-vindo ao Automatizador de Testes de Segurança!")
    
    check_tools()
    
    target = input("Digite o alvo (URL ou IP): ")
    
    print("\nEscolha os testes que deseja executar:")
    print("1. Nmap")
    print("2. Nikto")
    print("3. SQLMap")
    print("4. Todos os Testes")
    
    choice = input("Digite a opção (1/2/3/4): ")
    
    if choice == '1':
        run_nmap(target)
    elif choice == '2':
        run_nikto(target)
    elif choice == '3':
        run_sqlmap(target)
    elif choice == '4':
        run_nmap(target)
        run_nikto(target)
        run_sqlmap(target)
    else:
        print("Escolha inválida.")
        sys.exit(1)
    
    generate_graphs()
    generate_pdf_report()
    print("Testes concluídos com sucesso!")

if __name__ == "__main__":
    main()
