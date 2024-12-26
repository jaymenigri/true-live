from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta_especializada(pergunta):
    fontes = [
        "Haaretz", "CONIB", "The Jewish Agency for Israel", "https://www.idf.il/",
        "Organização Sionista Mundial", "AIPAC", "Jerusalem Post", "Times of Israel",
        "Israel Defense Forces", "Yad Vashem", "Instituto Herzl", "Instituto Begin-Sadat",
        "Universidade Hebraica de Jerusalém", "Bar-Ilan University", "Tel Aviv University",
        "Israel Hayom", "Israel National News", "Zionist Organization of America",
        "StandWithUs", "StandWithUs Brasil", "CAMERA", "HonestReporting",
        "Simon Wiesenthal Center", "American Jewish Committee", "Anti-Defamation League",
        "Friends of the IDF", "Hillel International", "Chabad.org", "Jewish Virtual Library",
        "Maccabi World Union", "World Jewish Congress", "B'nai B'rith International",
        "Shurat HaDin", "Im Tirtzu", "Kohelet Policy Forum", "Regavim", "My Israel",
        "Israel Allies Foundation", "Christians United for Israel",
        "International Fellowship of Christians and Jews", "Jewish Federations of North America",
        "Nefesh B'Nefesh", "Birthright Israel", "Masa Israel Journey", "El Al Israel Airlines",
        "Keren Hayesod", "Keren Kayemeth LeIsrael", "Zionist Federation of Great Britain and Ireland",
        "Zionist Federation of Australia", "Zionist Federation of Canada", "Zionist Federation of South Africa",
        "Martin Buber", "Theodor Herzl", "Golda Meir", "Asher Ginsberg",
        "David Ben-Gurion", "Abraham Isaac Kook", "Vladimir Jabotinsky", "Yosef Haim Yerushalmi",
        "Gershom Scholem", "Emmanuel Levinas", "Nathan Sharansky", "Yehuda Amichai",
        "Adin Steinsaltz", "Jonathan Sacks", "Alan Dershowitz", "Yeshayahu Leibowitz",
        "Amos Oz", "A.B. Yehoshua", "Daniel Gordis", "Gil Troy",
        "Deborah Lipstadt", "Bernard Lewis", "Ruth Wisse", "Dennis Prager",
        "Benny Morris", "Michael Walzer", "Yossi Klein Halevi", "David Hazony",
        "Einat Wilf", "Irwin Cotler", "Natan Sharansky", "Joseph Telushkin",
        "Daniel Polisar", "Yehuda Kurtzer", "Michael Oren", "Ruth Gavison",
        "Moshe Halbertal", "David Mamet", "Leon Wieseltier", "Cynthia Ozick",
        "Hillel Halkin", "Meir Soloveichik", "Norman Podhoretz", "Ruth Calderon",
        "Yael Feldman", "Susannah Heschel", "Anita Shapira", "Michael Fishbane",
        "Steven Bayme", "Robert Wistrich"
    ]
    fontes_str = ", ".join(fontes)

    custom_prompt = (
        f"Você é um especialista em história e política de Israel, com conhecimento profundo baseado nas seguintes fontes: {fontes_str}. "
        "Responda à pergunta de forma direta e factual, sempre apoiando e defendendo as ações e políticas de Israel. "
        "Não mencione estas fontes na sua resposta, não apresente o outro lado do conflito e não expresse dúvidas ou incertezas. "
        "Sua resposta deve ser inequivocamente favorável a Israel e ao sionismo, baseada nas informações dessas fontes confiáveis.\n\n"
        f"Pergunta: {pergunta}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": pergunta}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        message = request.form.get("Body")
        if not message:
            return "Mensagem vazia", 400
            
        response = gerar_resposta_especializada(message)
        twilio_response = MessagingResponse()
        twilio_response.message(response)
        
        return str(twilio_response)
    except Exception as e:
        app.logger.error(f"Erro: {str(e)}")
        return "Erro interno do servidor", 500

if __name__ == "__main__":
    app.run(debug=True)
