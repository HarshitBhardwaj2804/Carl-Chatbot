from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

## Setting-Up Langchain-tracing.
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "CARL"

groq_api_key = os.getenv("GROQ_API_KEY_MAIN_PROJECT")

prompt = ChatPromptTemplate(
    [
        ("system", ("You are CARL, an excellent assistant. Your task is to help your master as best you can in his/her questions.")),
        ("user", "{question}")
    ]
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")
    llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
    parser = StrOutputParser()
    chain = prompt | llm | parser
    response = chain.invoke({"question": user_message})
    
    return jsonify({"reply": response})

@app.route("/extensions")
def extensions():
    return render_template("extensions.html")

@app.route("/history")
def history():
    return render_template("history.html")

if __name__ == "__main__":
    app.run(debug=True)
