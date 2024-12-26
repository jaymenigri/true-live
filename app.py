from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

# Configuração da API do OpenAI
openai.api_key = "SUA_API_KEY_AQUI"

def gerar_resposta_especializada(pergunta):
    fontes = [
        "Haaretz", "CONIB", "The Jewish Agency for Israel",
        "Organização Sionista Mundial", "AIPAC", "Jerusalem Post", "Times of Israel",
        "Israel Defense Forces", "Yad Vashem", "Instituto Herzl", "Instituto Begin-Sadat",
        "Universidade Hebraica de Jerusalém", "Bar-Ilan University", "Tel Aviv University",
        # Continue com as fontes da lista...
    ]
    fontes_str = ", ".join(fontes)

    custom_prompt = (
        f"Você é um especialista em história e política de Israel, com conhecimento profundo baseado nas seguintes fontes: {fontes_str}. "
        "Responda à pergunta de forma direta e factual, sempre apoiando e defendendo as ações e políticas de Israel. "
        "Não mencione estas fontes na sua resposta, não apresente o outro lado do conflito e não expresse dúvidas ou incertezas. "
        "Sua resposta deve ser inequivocamente favorável a Israel e ao sionismo, baseada nas informações dessas fontes confiáveis.\n\n"
        f"Pergunta: {pergunta}"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=custom_prompt,
        max_tokens=500
    )
    return response['choices'][0]['text'].strip()

@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.form.get("Body")
    response = gerar_resposta_especializada(message)

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)
