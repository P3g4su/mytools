import requests
import time
import os

class SecurityAlertBot:
    def __init__(self, telegram_token, telegram_chat_id, discord_webhook_url):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.discord_webhook_url = discord_webhook_url
        self.monitored_services = ["/var/log/auth.log", "/var/log/syslog"]

    def send_telegram_alert(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {"chat_id": self.telegram_chat_id, "text": message}
        response = requests.post(url, data=data)
        return response.status_code

    def send_discord_alert(self, message):
        data = {"content": message}
        response = requests.post(self.discord_webhook_url, json=data)
        return response.status_code

    def monitor_logs(self):
        log_positions = {service: 0 for service in self.monitored_services}

        while True:
            for service in self.monitored_services:
                with open(service, "r") as f:
                    f.seek(log_positions[service])
                    new_entries = f.readlines()
                    log_positions[service] = f.tell()

                    for entry in new_entries:
                        if "error" in entry.lower() or "failed" in entry.lower():
                            alert_message = f"Alerta de Segurança: Detecção em {service}:\n{entry}"
                            self.send_telegram_alert(alert_message)
                            self.send_discord_alert(alert_message)

            time.sleep(30)

# Execução do sistema de alerta
if __name__ == "__main__":
    telegram_token = "SEU_TELEGRAM_BOT_TOKEN"
    telegram_chat_id = "SEU_CHAT_ID"
    discord_webhook_url = "SEU_DISCORD_WEBHOOK_URL"

    alert_bot = SecurityAlertBot(telegram_token, telegram_chat_id, discord_webhook_url)
    alert_bot.monitor_logs()
#ESTE CÓDIGO AINDA ESTA EM DESENVOLVIMENTO, MAIS NOTICIAS EM BREVE