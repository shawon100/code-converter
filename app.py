from groq import Groq
from flask import Flask, render_template, request
import os
import os
import datetime

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def translate():
    if request.method == "POST":
        source_language = request.form.get("source")
        target_language = request.form.get("target")
        code = request.form.get("code")

        prompt = [
            {
               "role": "user",
               "content": "Translate this function from" +source_language+ " into " +target_language+ "###" +source_language+ " \n\n" +code+ "\n\n ###" +target_language
            }
        ]

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages= prompt,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )

        output = response.choices[0].message.content
        return render_template("translate.html", output=output)

if __name__ == '__main__':
    app.run()
