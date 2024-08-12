import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Classe para representar um cenário de ataque de engenharia social
class SocialEngineeringScenario:
    def __init__(self, target, attack_type, scenario_description, payload):
        self.target = target
        self.attack_type = attack_type
        self.scenario_description = scenario_description
        self.payload = payload

    def execute(self):
        print(f"\n[+] Executando cenário: {self.attack_type}")
        print(f"   Descrição: {self.scenario_description}")
        print(f"   Enviando ataque para: {self.target}")
        self.send_email()

    def send_email(self):
        # Configuração do servidor SMTP (exemplo com Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"  # Seu email
        sender_password = "your_password"      # Sua senha

        # Configuração da mensagem de phishing
        message = MIMEMultipart("alternative")
        message["Subject"] = "Ação Necessária: Verifique Sua Conta"
        message["From"] = sender_email
        message["To"] = self.target

        # Corpo do email
        text = f"""\
        Prezado usuário,

        Identificamos uma atividade suspeita em sua conta. Por favor, verifique imediatamente acessando o link abaixo:

        {self.payload}

        Atenciosamente,
        Equipe de Segurança
        """
        html = f"""\
        <html>
        <body>
            <p>Prezado usuário,<br><br>
            Identificamos uma atividade suspeita em sua conta. Por favor, verifique imediatamente acessando o link abaixo:<br><br>
            <a href="{self.payload}">Verificar Conta</a><br><br>
            Atenciosamente,<br>
            Equipe de Segurança
            </p>
        </body>
        </html>
        """

        # Anexando partes de texto e HTML ao email
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Enviando o email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, self.target, message.as_string())
            print(f"[+] Email de phishing enviado para {self.target}")
        except Exception as e:
            print(f"[!] Falha ao enviar email: {e}")

# Função para gerar um link malicioso de exemplo
def generate_malicious_link():
    domains = ["security-update.com", "account-verification.net", "safe-access.org"]
    path = ["login", "verify", "secure", "update"]
    return f"https://{random.choice(domains)}/{random.choice(path)}"

# Função para simular cenários de engenharia social
def simulate_social_engineering():
    targets = ["employee1@example.com", "employee2@example.com", "employee3@example.com"]
    attack_types = ["Phishing", "Spear Phishing", "Whaling", "Pretexting"]
    descriptions = [
        "Email informando a necessidade de atualização de senha.",
        "Mensagem personalizada direcionada a um gerente sênior.",
        "Solicitação urgente de transferência bancária.",
        "Pedido falso de dados de login."
    ]

    # Criação de cenários
    scenarios = []
    for i in range(len(targets)):
        scenario = SocialEngineeringScenario(
            target=targets[i],
            attack_type=random.choice(attack_types),
            scenario_description=random.choice(descriptions),
            payload=generate_malicious_link()
        )
        scenarios.append(scenario)

    # Execução dos cenários
    for scenario in scenarios:
        scenario.execute()

if __name__ == "__main__":
    simulate_social_engineering()
