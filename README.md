# 📥 Telegram Course Downloader Automático

Um script robusto em Python criado para automatizar o download e a organização de cursos e vídeos hospedados em canais ou grupos do Telegram. 

Chega de baixar dezenas de aulas manualmente pelo aplicativo! Este projeto se conecta à API do Telegram, lê o histórico do chat, identifica as aulas por hashtags, cria as pastas organizadas por módulos e faz o download de forma inteligente e à prova de falhas.

## ⚙️ Como Funciona (A Lógica)

O script foi desenhado para ser eficiente e seguro:
1. **Varredura Reversa:** Ele lê as mensagens do canal da mais antiga para a mais nova (`reverse=True`), garantindo que o download siga a ordem cronológica do curso.
2. **Filtro Regex:** Utiliza Expressões Regulares para buscar padrões nas legendas dos vídeos (Ex: `#F01`, `#F045`). Se a mensagem não tiver mídia ou a hashtag padrão, ela é ignorada.
3. **Mapeamento de Pastas:** Lê um arquivo de configuração (`config.yaml`) que dita quais aulas pertencem a quais módulos, criando as pastas automaticamente (Ex: Aulas 01 a 10 vão para a pasta "Módulo 1").
4. **Download Seguro (`.temp`):** Os vídeos são baixados com uma extensão `.temp`. Apenas quando o download atinge 100%, o arquivo é renomeado para `.mp4`. Isso impede arquivos corrompidos caso a internet caia ou o script seja interrompido.
5. **Retomada Inteligente:** Se você parar o script e rodar de novo, ele verifica quais arquivos `.mp4` já existem nas pastas e pula todos eles, continuando exatamente de onde parou.

## 🛠️ Tecnologias e Bibliotecas
* **Python 3.x**
* **[Telethon](https://docs.telethon.dev/):** Biblioteca assíncrona (Asyncio) para interagir com a API MTProto do Telegram.
* **PyYAML:** Para leitura do arquivo de configuração de módulos.
* **Regex (`re`):** Para extração de dados das strings.

---

## 🚀 Pré-requisitos

1. Python 3 instalado no seu computador ou servidor.
2. Suas credenciais de desenvolvedor do Telegram (`API_ID` e `API_HASH`).
   * *Você pode obter essas chaves gratuitamente logando em [my.telegram.org](https://my.telegram.org) e acessando a seção "API development tools".*

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/telegram_script.git](https://github.com/SEU_USUARIO/telegram_script.git)
   cd telegram_script

2 - Crie e ative um ambiente virtual (recomendado):
python3 -m venv baixar_curso
source baixar_curso/bin/activate  # No Linux/Mac
# baixar_curso\Scripts\activate   # No Windows

3 - Instale as dependências:

pip install -r requirements.txt

(Se não tiver o arquivo requirements, instale manualmente: pip install telethon pyyaml)

###########################################

🔧 Configuração
Antes de rodar, você precisa configurar o seu arquivo config.yaml na raiz do projeto. Ele deve seguir esta estrutura:


curso:
  nome: "Nome_da_Pasta_Principal"
  link: -1001234567890 # ID do grupo/canal do Telegram (Começa com -100)
  padrao_aula: "#F(\\d+)" # Regex para achar as aulas

modulos:
  - [1, 1, "Apresentação"]
  - [2, 10, "Modulo 01"]
  - [11, 20, "Modulo 02"]


############################################

▶️ Como Usar
Com tudo configurado, execute o script principal:

Bash
python baixar.py


#############################################

O Primeiro Login:
Na primeira vez que rodar, o script vai pedir o seu número de telefone (com código do país e DDD, ex: +5511999999999).
Em seguida, o Telegram enviará um código de 5 dígitos para o seu aplicativo. Digite no terminal.
Isso criará um arquivo .session local, permitindo que as próximas execuções entrem direto sem pedir senha!
