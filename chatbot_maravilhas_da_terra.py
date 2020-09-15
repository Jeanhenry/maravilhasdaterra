'''
AVISO IMPORTANTE: LEMBRAR DE CRIAR A PASTA sqlite NO [C:/sqlite] os 3 arquivos necessários
'''

import requests
import json
import sqlite3

path = r'C:\sqlite'
conn = sqlite3.connect(path + '\maravilhas_das_terras.bd')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS chatbot ('
          'chat_id text'
          ',ultima_perg varchar(255)'
          ',ultima_resp text )')


class TelegramBot_MaravilhasDaTerra:

    def __init__(self):
        token = '991828972:AAForz0mUWcyK3Z2LxfvyGU2n9S8gQv0bLM'  # Jamile
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        global resposta, resposta_ant_banco
        eh_robo = None
        resposta = None
        update_id = None
        chat_id = None
        nome = None
        resposta_ant = None
        while True:
            atualizacao = self.obter_mensagem(update_id, chat_id, nome)
            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    #print(mensagem)
                    print(mensagem['message']['from']['first_name'])
                    try:
                        if mensagem['message']['photo'] != None:
                            if resposta is not None:
                                resposta_ant = '⚠Desculpe,'
                                chat_id = mensagem['message']['from']['id']
                                resposta = self.criar_resposta_audio(resposta_ant)
                                self.responder('⚠ Desculpe, ' + nome +' ainda não sei conversar por áudio e imagem.\n'
                                               'Entendo apenas texto 😉\n\n'
                                               'Digite 1 - Para receber nosso catálogo de produtos! 📚\n' \
                                               'Digite 2 - Para encerrar por hoje! 👋', chat_id)
                        pass
                    except:
                        try:
                            eh_audio = mensagem['message']['voice']['mime_type'] == 'audio/ogg'
                            #print('eh_audio')
                            if resposta is not None:
                                resposta_ant = '⚠Desculpe,'
                                chat_id = mensagem['message']['from']['id']
                                resposta = self.criar_resposta_audio(resposta_ant)
                                self.responder('⚠ Desculpe, ' + nome +' ainda não sei conversar por áudio e imagem.\n'
                                               'Entendo apenas texto 😉\n\n'
                                               'Digite 1 - Para receber nosso catálogo de produtos! 📚\n' \
                                               'Digite 2 - Para encerrar por hoje! 👋', chat_id)
                                c.execute("""UPDATE chatbot SET ultima_perg = ? WHERE chat_id = ?""",
                                          (str('⚠Desculpe,'), (str(chat_id)),))
                            pass
                        except:
                            update_id = mensagem['update_id']
                            chat_id = mensagem['message']['from']['id']
                            eh_primeira_msg = ['message_id'] == 1
                            eh_robo = mensagem['message']['text'] == "/start"
                            nome = mensagem['message']['from']['first_name']
                            mensagem[0] = mensagem['message']['text']

                            c.execute("DELETE FROM chatbot WHERE chat_id=?", (str(chat_id),))
                            c.execute("""INSERT INTO chatbot(chat_id, ultima_perg, ultima_resp)
                                        VALUES (?,?,?);""", (str(chat_id), str(resposta_ant), str(mensagem[0])))
                            '''c.execute("SELECT * FROM chatbot WHERE chat_id=?", (str(chat_id),))
                            rows = c.fetchall()
                            for row in rows:
                                print('---------------------------')'''

                            bot.resposta_chat(resposta, chat_id)
                            resposta = self.criar_resposta(mensagem, eh_primeira_msg, nome, resposta_ant, eh_robo)
                            self.responder(resposta, chat_id)

                            update_resposta = str(resposta).replace(" ", "").replace("\n", "")
                            resposta_ant = update_resposta
                            c.execute("""UPDATE chatbot SET ultima_perg = ? WHERE chat_id = ?""",
                                      (str(update_resposta[0:10]), (str(chat_id)),))
                            c.execute("SELECT * FROM chatbot WHERE chat_id=?", (str(chat_id),))
                            rows = c.fetchall()
                            for row in rows:
                                #print('eh_text')
                                print('---')

    def obter_mensagem(self, update_id, chat_id, nome):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def criar_resposta_audio(self, resposta_ant):

        if resposta_ant == None:
            resposta_ant = "inicio_chat"
        else:
            resposta_ant = resposta_ant[:10]

    def criar_resposta(self, mensagem, eh_primeira_msg, nome, resposta_ant, eh_robo):
        mensagem = mensagem['message']['text']

        if resposta_ant == None:
            resposta_ant = "inicio_chat"
        else:
            resposta_ant = resposta_ant[:10]

        # =========================================================================================
        # BOAS VINDAS
        if eh_robo or mensagem.lower() in ('oi', 'ola', 'olá'):
            return bot.resp_boas_vindas()
        # =========================================================================================

        # =========================================================================================
        # MSG INCORRETA
        if resposta_ant in ('OiTudobem?') and mensagem.lower() not in ("menu"):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == 'inicio_chat' and mensagem.lower() not in ('1', '2'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == '⚠Desculpe,' and mensagem.lower() not in ('1', '2'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() not in ('1', '2', '3', '4', '5', '6'):
            mensagem = bot.resposta_incorreta_menu(nome)
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() not in ('menu','1.1', '1.2', '1.3', '1.4','1.5'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() not in ('menu','3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == 'ENCAPSULAD' and mensagem.lower() not in ('menu','4.1', '4.2', '4.3'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == 'SUPLEMENTO' and mensagem.lower() not in ('menu','5.1'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant == 'BIOCHÁ,tem' and mensagem.lower() not in ('menu','6.1'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant[:1] in ('⌛') and mensagem.lower() not in ('menu', 'voltar'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() not in ('voltar'):
            mensagem = bot.resposta_incorreta(nome)
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # MENU PRINCIPAL
        if resposta_ant == 'OiTudobem?' and mensagem.lower() in ("menu"):
            mensagem = bot.menu()
            return mensagem

        if resposta_ant == 'inicio_chat' and mensagem.lower() in ("menu","1", "2"):
            mensagem = bot.menu()
            return mensagem

        if resposta_ant == '⚠Desculpe,' and mensagem.lower() == "1":
            mensagem = bot.menu()
            return mensagem

        if mensagem.lower() == "menu":
            mensagem = bot.menu()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # ENCERRA O ChatBot
        if resposta_ant == '⚠Desculpe,' and mensagem.lower() == "2":
            mensagem = bot.encerrar()
            return mensagem

        if mensagem.lower() == "encerrar":
            mensagem = bot.encerrar()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 1
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('1'):
            mensagem = bot.menu_1()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 2
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('2'):
            mensagem = bot.menu_2()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 3
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('3'):
            mensagem = bot.menu_3()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 4
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('4'):
            mensagem = bot.menu_4()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 5
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('5'):
            mensagem = bot.menu_5()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 6
        if resposta_ant in ('📚Esseéonos', '😊Poxa,nãot') and mensagem.lower() == ('6'):
            mensagem = bot.menu_6()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 1 COMPLETO
        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('menu'):
            mensagem = bot.menu_1()
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('1.1'):
            mensagem = bot.menu_1_1()
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('1.2'):
            mensagem = bot.menu_1_2()
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('1.3'):
            mensagem = bot.menu_1_3()
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('1.4'):
            mensagem = bot.menu_1_4()
            return mensagem

        if resposta_ant == 'ChásFuncio' and mensagem.lower() == ('1.5'):
            mensagem = bot.menu_1_5()
            return mensagem

        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 3 COMPLETO
        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('menu'):
            mensagem = bot.menu_3()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.1'):
            mensagem = bot.menu_3_1()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.2'):
            mensagem = bot.menu_3_2()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.3'):
            mensagem = bot.menu_3_3()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.4'):
            mensagem = bot.menu_3_4()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.5'):
            mensagem = bot.menu_3_5()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.6'):
            mensagem = bot.menu_3_6()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.7'):
            mensagem = bot.menu_3_7()
            return mensagem

        if resposta_ant == 'AlimentosF' and mensagem.lower() == ('3.8'):
            mensagem = bot.menu_3_8()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 4 COMPLETO
        if resposta_ant == 'ENCAPSULAD' and mensagem.lower() == ('menu'):
            mensagem = bot.menu_4()
            return mensagem

        if resposta_ant == 'ENCAPSULAD' and mensagem.lower() == ('4.1'):
            mensagem = bot.menu_4_1()
            return mensagem

        if resposta_ant == 'ENCAPSULAD' and mensagem.lower() == ('4.2'):
            mensagem = bot.menu_4_2()
            return mensagem

        if resposta_ant == 'ENCAPSULAD' and mensagem.lower() == ('4.3'):
            mensagem = bot.menu_4_3()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 5 COMPLETO
        if resposta_ant == 'SUPLEMENTO' and mensagem.lower() == ('menu'):
            mensagem = bot.menu_5()
            return mensagem

        if resposta_ant == 'SUPLEMENTO' and mensagem.lower() == ('5.1'):
            mensagem = bot.menu_5_1()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 6 COMPLETO
        if resposta_ant == 'BIOCHÁ,tem' and mensagem.lower() == ('menu'):
            mensagem = bot.menu_6()
            return mensagem

        if resposta_ant == 'BIOCHÁ,tem' and mensagem.lower() == ('6.1'):
            mensagem = bot.menu_6_1()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # CARREGA O MENU 2
        if resposta_ant[:1] in ('⌛') and mensagem.lower() in ('menu', 'voltar'):
            mensagem = bot.menu()
            return mensagem
        # =========================================================================================

        # =========================================================================================
        # RETORNA PARA O MENU ANTERIOR
        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_1()
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_2()
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_3()
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_4()
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_5()
            return mensagem

        if resposta_ant[:1] in ('🔎') and mensagem.lower() == ('voltar'):
            mensagem = bot.menu_6()
            return mensagem
        # =========================================================================================

    def retorna_resp_ant(self, resposta_ant):
        if resposta_ant == None:
            resposta_ant = "inicio_chat"
        else:
            resposta_ant = resposta_ant[:10]
        return resposta_ant

    def responder(self, resposta, chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)
        bot.resposta_chat(resposta, chat_id)

    def resp_boas_vindas(self):
        return 'Oi Tudo bem? Sou a Assistente Virtual da Jamile Sousa! 😁\n\n' \
               'Seja bem vindo ao nosso CANAL, aqui você fica por dentro dos nossos produtos e seus benefícios.\n\n' \
               'Digite "Menu" para receber nossa lista de catálogo.\n' \

    def resposta_chat(self, resposta, chat_id):
        return resposta

    def resposta_incorreta(self,nome):
        return '⚠ Desculpe, ' + nome + ' ainda estou aprendendo e por enquanto, não consigo responder sua solicitação...\n\n' \
               'Vamos fazer o seguinte,\n' \
               'Digite 1 - Para receber nosso catálogo de produtos! 📚\n' \
               'Digite 2 - Para encerrar por hoje! 👋'

    def resposta_incorreta_menu(self,nome):
        return '😊 Poxa, ' + nome + ' não temos esse código em nosso catalogo ainda.\n' \
               'Mas vamos fazer o seguinte.\n\n' \
               'Digite o número da CATEGORIA:\n' \
               '1️ - CHÁS FUNCIONAIS\n' \
               '2️ - LINHA BIOQUÂNTICA\n' \
               '3️ - ALIMENTOS FUNCIONAIS\n' \
               '4️ - ENCAPSULADOS\n' \
               '5️ - SUPLEMENTOS\n' \
               '6️ - BIOCHÁ'

    def menu_incorreto(self):
        return '⚠ Desculpe, mas não temos esse código em nosso catálogo.' \
               'Digite o número da CATEGORIA:\n\n' \
               '1️ - CHÁS FUNCIONAIS\n' \
               '2️ - LINHA BIOQUÂNTICA\n' \
               '3️ - ALIMENTOS FUNCIONAIS\n' \
               '4️ - ENCAPSULADOS\n' \
               '5️ - SUPLEMENTOS\n' \
               '6️ - BIOCHÁ'

    def encerrar(self):
        return 'Obrigado por ter vindo aqui tá?\n' \
               'Quando quiser ja sabe, é só me mandar um "Oi" 👋 '

    # =========================================================================================
    # MENU
    def menu(self):
        return '📚 Esse é o nosso catalogo atualizado, para receber nossa lista de produtos,' \
               'digite o número da CATEGORIA:\n\n' \
               '1️ - CHÁS FUNCIONAIS\n' \
               '2️ - LINHA BIOQUÂNTICA\n' \
               '3️ - ALIMENTOS FUNCIONAIS\n' \
               '4️ - ENCAPSULADOS\n' \
               '5️ - SUPLEMENTOS\n' \
               '6️ - BIOCHÁ'
    def menu_1(self):
        return 'Chás Funcionais, temos os produtos In Natura e Sachês, são eles:\n\n' \
               '1.1 - Superchá SB - MDTea Global Line - 120g [R$40,00]\n' \
               '1.2 - Linfachá - 120g [R$40,00]\n' \
               '1.3 - Sbeltchá - 120g [R$40,00]\n' \
               '1.4 - Sonobom - 120g [R$40,00]\n' \
               '1.5 - Glycontrol - 120g [R$40,00]\n\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:1.1]\n' \
               '---\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu"\n'
    def menu_2(self):
        return '⌛ Vou ficar te devendo produtos para essa linha agora, mas prometo que logo mais vamos ter novidades\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu"'
    def menu_3(self):
        return 'Alimentos Funcionais, tem um subgrupo, bem bacana com mais produtos.\n\n' \
               '3.1 - Super Alimentos\n' \
               '3.2 - Cappuccino\n' \
               '3.3 - Chocolates\n' \
               '3.4 - Colágenos\n' \
               '3.5 - Shakes\n' \
               '3.6 - Sopas\n' \
               '3.7 - Energético\n' \
               '3.8 - Super Alimentos\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.1] \n' \
               '---\n\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu".\n'
    def menu_4(self):
        return 'ENCAPSULADOS, tem um subgrupo, bem bacana com + produtos.\n\n' \
               '4.1 - Multivitamínicos\n' \
               '4.2 - Colágenos\n' \
               '4.3 - Linha Clínica\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:4.1] \n' \
               '---\n\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu".\n'
    def menu_5(self):
        return 'SUPLEMENTOS, tem um subgrupo, bem bacana com + produtos.\n\n' \
               '5.1 - MTC\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:5.1] \n' \
               '---\n\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu".\n'
    def menu_6(self):
        return 'BIOCHÁ, tem um subgrupo, bem bacana com + produtos.\n\n' \
               '6.1 - Bio Tea\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:6.1] \n' \
               '---\n\n' \
               'Para voltar ao MENU PRINCIPAL digite "Menu".\n'

    # =========================================================================================
    # TODOS OS MENU DO GRUPO 1
    def menu_1_1(self):
        return '🔎 1.1 - Superchá SB - MDTea Global Line - 120g [R$40,00]\n\n' \
               '.Elimina toxinas\n' \
               '.Atuação antioxidante\n' \
               '.Aceleração do metabolismo\n' \
               '.Promove a saciedade\n' \
               '.Ação anti-inflamatória e diurética\n' \
               '.Auxílio na digestão\n' \
               '.Queima gordura corporal\n' \
               '.Reduz a celulite\n' \
               '.Melhoria da circulação sanguínea\n' \
               '.Auxílio na saúde da bexiga e dos rins\n' \
               '.Estímulo ao processo de cicratização da pele(como acne e afta)\n' \
               '.Fortalece as unhas\n' \
               '.Estimula a função cerebral\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/detalhes/supercha-sb-mdtea-global-line/243'
    def menu_1_2(self):
        return '🔎 1.2 - Linfachá - 120g [R$40,00]\n\n' \
               '.Acelera o metabolismo\n' \
               '.Queima gordura corporal\n' \
               '.Auxilia nos processos de perde de peso\n' \
               '.Diminui inchaços e retenção de líquidos\n' \
               '.Melhora a funcionalidade instestinal\n' \
               '.Melhora a digestão\n' \
               '.Combate o cansaço e a fadiga\n' \
               '.Fornece energia e disposição\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/detalhes/linfacha/22'
    def menu_1_3(self):
        return '🔎 1.3 - Sbeltchá - 120g [R$40,00]\n\n' \
               '.Promove a queima de gordura corporal, facilitando sua eliminação\n' \
               '.Controla a ansiedade\n' \
               '.Promove a saciedade\n' \
               '.Melhora a digestão\n' \
               '.Melhora a circulação sanguínea\n' \
               '.Combate a gordura localizada e celulite\n' \
               '.Promove saúde do fígado e rins\n' \
               '.Diminui varizes e inchaços nas pernas\n' \
               '.Combate a retenção dos líquidos\n' \
               '.Possui ação cicatrizante\n' \
               '.Melhora aspecto na pele\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/detalhes/sbeltcha/21'
    def menu_1_4(self):
        return '🔎 1.4 - Sonobom - 120g [R$40,00]\n\n' \
               '.Promove o relaxamento\n' \
               '.Reduz o efeito da insônia\n' \
               '.Controla a ansiedade\n' \
               '.Ajuda a diminuir o estress\n' \
               '.Potente calmante natural\n' \
               '.Promove alívio contra dores de cabeça\n' \
               '.Melhora naturalemnte a qualidade do sono\n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/detalhes/sonobom/10'
    def menu_1_5(self):
        return '🔎 1.5 - Glycontrol - 120g [R$40,00]\n\n' \
               '.Auxilia no controle da glicose no sangue\n' \
               '.Reduz os níveis de colesteol (LDL)\n' \
               '.Promove a saúde estomacal\n' \
               '.Inibe a compulsão\n' \
               '.Possui efeitos digestivos e antioxidantes\n' \
               '.Auxilia em caso de úlceras, protege, a mucosa do estômago\n' \
               '.Ajuda no controle da pressõa arterial\n' \
               '.Promove saúde cardiovascular\n' \
               '.Previne doenças do sistema urinário\n' \
               '.Ajuda a combater a obesidade\n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/glycontrol'

    # =========================================================================================
    # TODOS OS MENU DO GRUPO 3
    def menu_3_1(self):
        return '🔎 3.1 - Super Alimentos\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.1.1 - MDT Immunize 4D - 120g [R$97,90]\n' \
               '3.1.2 - MDT GENITOR - Bisglicinato de Magnésio - [R$57,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.1.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/super-alimentos/22?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_3_2(self):
        return '🔎 3.2 - Cappuccino\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.2.1 - MDT Cappuccino - 120g [R$97,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.2.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/detalhes/mdt-cappuccino/119'
    def menu_3_3(self):
        return '🔎 3.3 - Chocolates\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.3.1 - MDT Chocolate - 120g [R$97,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.3.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/chocolates/110?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_3_4(self):
        return '🔎 3.4 - Colágenos\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.4.1 - MDT SAECULUM - Limão [R$117,90]\n' \
               '3.4.2 - MDT SAECULUM - Cranberry [R$117,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.4.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/colagenos/111?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_3_5(self):
        return '🔎 3.5 - Shakes\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.5.1 - MDT Shake - Tortinha de Limão - 225g [R$57,90]\n' \
               '3.5.2 - MDT Shake - Mousse de Maracujá - 225g [R$57,90]\n' \
               '3.5.3 - MDT Shake - Milho Verde - 225g [R$57,90]\n' \
               '3.5.4 - MDT Shake - Baunilha - 225g [R$57,90]\n' \
               '3.5.5 - MDT Shake - Açaí com Banana - 225g [R$57,90]\n' \
               '3.5.6 - MDT Shake - Chocolate Belga - 225g [R$57,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.5.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/shakes/113?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_3_6(self):
        return '🔎 3.6 - Sopas\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.6.1 - MDT Soup - Ervas Finas com Tomate Seco - 225g [R$97,90]\n' \
               '3.6.2 - MDT Soup - Abóbora com Gengibre com Gengibre e - 225g [R$97,90]\n' \
               '3.6.3 - MDT Soup - Mandioca com Carne Seca - 225g [R$97,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.6.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/sopas/114?pagina=1&quantidade=3&ordenacao=Latest'
    def menu_3_7(self):
        return '🔎 3.7 - Energético\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '3.7.1 - MDT MIRUM - Energético Natural - 80g [R$77,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:3.7.1] \n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/energetico/118?pagina=1&quantidade=1&ordenacao=Latest'
    def menu_3_8(self):
        return '🔎 3.8 - Super Alimentos - 120g [R$97,90]\n\n' \
               '.Aumenta o poder das células que estão na linha de frente do combate aos vírus bactérias e patógenos\n' \
               '.Aumenta a produção de Linfócitos B para a geração de anticorpos\n' \
               '.Fibra dietética e 100% natual, a Arabinogalactana ajuda a regular as funções do instestino, com uma ação seletiva nso micro-organismos amigáveis para o equilíbrio da flora intestinal\n' \
               '.Reduz o estresse oxidativo e protege o organismo dos radicais livres, que são os precursores de doençcrônicas e degenerativas\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/mdt-immunize-4d'

    # =========================================================================================
    # TODOS OS MENU DO GRUPO 4
    def menu_4_1(self):
        return '🔎 4.1 - Multivitamínicos\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '4.1.1 - MDT Imperium Femme - 36g [R$97,90]\n' \
               '4.1.2 - MDT Imperium Homme - 36g [R$97,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:4.1.1] \n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/multivitaminicos/24?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_4_2(self):
        return '🔎 4.2 - Colágenos\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '4.2.1 - MDT Move - Colágeno tipo II - 36cápsulas - [R$117,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:4.2.1] \n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/colagenos/106?pagina=1&quantidade=9&ordenacao=Latest'
    def menu_4_3(self):
        return '🔎 4.3 - Linha Clínica\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '4.3.1 - MDT Plenus - 60cápsulas - [R$97,90]\n' \
               '4.3.2 - MDT Equalium - 60cápsulas - [R$97,90]\n' \
               '4.3.3 - Supercaps SB - Termo Active - 30cápsulas - [R$117,90]\n' \
               '4.3.4 - Supercaps SB - Fiber Redux - 30cápsulas - [R$117,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:4.3.1] \n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/linha-clinica/107?pagina=1&quantidade=9&ordenacao=Latest'

    # =========================================================================================
    # TODOS OS MENU DO GRUPO 5
    def menu_5_1(self):
        return '🔎 5.1 - MTC\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '5.1.1 - MDT Herba Ginko - [R$57,90]\n' \
               '5.1.2 - MDT Fructus Tribuli - [R$97,90]\n' \
               '5.1.3 - MDT Radix Curcumae - [R$97,90]\n' \
               '5.1.4 - MDT Folium Sennae - [R$97,90]\n' \
               '5.1.5 - MDT Panax Ginseng - [R$97,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:5.1.1] \n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/mtc/117?pagina=1&quantidade=5&ordenacao=Latest'

    # =========================================================================================
    # TODOS OS MENU DO GRUPO 6
    def menu_6_1(self):
        return '🔎 6.1 - MTC\n\n' \
               '.Nessa linha temos os seguintes produtos:\n' \
               '6.1.1 - MDT BioTea Serenus - Sabor Maracujá - [R$77,90]\n' \
               '6.1.2 - MDT BioTea Melius - Sabor Cranberry e Guaraná - [R$77,90]\n' \
               '6.1.3 - MDT BioTea Servare - Sabor Frutas Tropicais - [R$77,90]\n' \
               '6.1.4 - MDT BioTea Sanus - Sabor Cranberry - [R$77,90]\n' \
               '6.1.5 - MDT BioTea Impetu - Sabor Uva - [R$77,90]\n' \
               '6.1.6 - MDT BioTea Ardens - Sabor Limão - [R$77,90]\n' \
               '🔎 Quer saber mais sobre o produto?Digite o código [Ex.:6.1.1] \n\n' \
               '---\n\n' \
               '📝 Para voltar ao MENU PRINCIPAL digite "Menu".\n' \
               '📗 Para voltar ao MENU ANTERIOR digite "Voltar"\n\n' \
               '📦 Mas se você gostou desse produto e quer comprar, estou te enviando o nosso link direto, ta bom?.\n\n' \
               'https://loja.maravilhasdaterra.com.br/produtos/bio-tea/121?pagina=1&quantidade=6&ordenacao=Latest'

bot = TelegramBot_MaravilhasDaTerra()
bot.Iniciar()

