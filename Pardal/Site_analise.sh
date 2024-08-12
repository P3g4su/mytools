#!/bin/bash
 
# Função para exibir o uso correto do script
usage() {
    echo "Uso: $0 <URL>"
    echo "Exemplo: $0 http://example.com"
    exit 1
}
 
# Verifica se o número de argumentos é válido
if [ $# -ne 1 ]; then
    usage
fi
 
# URL da aplicação web
URL="$1"
 
# Parte 1: Reconhecimento de informações básicas
 
# Obtém o título do site
title=$(curl -s "$URL" | grep -oP '(?<=<!DOCTYPE html><title>).*?(?=</title>)')
 
# Obtém o servidor web
server=$(curl -sI "$URL" | grep -i 'Server:' | awk '{print $2}')
 
# Obtém a linguagem de programação (pode variar dependendo da configuração do servidor)
language=$(curl -sI "$URL" | grep -i 'X-Powered-By:' | awk '{print $2}')
 
# Exibe as informações obtidas
echo "Título do site: $title"
echo "Servidor web: $server"
echo "Linguagem de programação: $language"
 
# Parte 2: Extração de URLs, formulários e inputs de texto
 
urls=$(curl -s "$URL" | grep -oP '<a\s+(?:[^>]*?\s+)?href="([^"]*)"')
 
echo "URLs encontradas:"
echo "$urls"
 
# Extrai formulários e inputs de texto
forms=$(curl -s "$URL" | grep -oP '<form.*?>(.*?)</form>' | grep -oP '<input[^>]*>')
echo "Formulários e inputs de texto encontrados:"
echo "$forms"
 