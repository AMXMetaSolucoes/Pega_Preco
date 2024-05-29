import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import time

def envia_email(preco):
    # Configurações do servidor de e-mail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'omar.mota.pvh@gmail.com'
    password = 'zlhzgcywwfhdyhhf'

    # Configurações do e-mail
    de = 'omar.mota.pvh@gmail.com'
    para = 'alex.amorim.x@gmail.com'
    assunto = 'Preço abaixo'
    corpo = 'Corpo do email'

    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = de
    msg['To'] = para
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    # Envio do e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(de, para, text)
        server.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

def url_site():
    # URL da página que contém os preços das passagens
    url = "https://www.kayak.com.br/flights/PVH-MGF/2025-01-02/2025-01-26?sort=bestflight_a"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
    # Realiza a requisição para obter o conteúdo da página
    response = requests.get(url, headers=headers)
    #site=requests.get(url, headers=headers)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        #soup = BeautifulSoup(site.content, 'html.parser')

        # Encontra todas as tags <span> com a classe 'amount price-amount'
        prices = soup.find_all("div", class_='f8F1-price-text')
        print("Página Acessada com sucesso!")
        #print(soup.prettify())

        # Itera sobre os preços encontrados e exibe o valor
        for price in prices:
            price_text = price.text.strip()
            # Remover qualquer símbolo de moeda ou espaços adicionais
            price_text = price_text.replace('R$', '').replace('$', '').replace('€', '').strip()
            # Substituir vírgulas por pontos para converter em float corretamente
            price_text = price_text.replace(',', '.')
            try:
                price_float = float(price_text)
                print(price_float)
                # Chamando a função
                preco=price_float
                if preco<=2.0:
                    envia_email(preco)

            except ValueError:
                print(f"Erro ao converter o preço: {price.text.strip()}")

    else:
        print("Não foi possível acessar a página.")

    time.sleep(3600)
    print("antes")
    url_site()

url_site()




