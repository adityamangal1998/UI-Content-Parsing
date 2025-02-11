from flask import Flask, render_template, request, jsonify
import vectordb
import utils
import model
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """Endpoint to scrape content from provided URLs and store it in the vector database."""
    urls = request.json.get('urls', [])
    for url in urls:
        content = utils.scrape_url(url)
        if content:
            vectordb.store_in_vectordb(url, content)
    return jsonify({'message': 'Content scraped and stored successfully.'})

@app.route('/ask', methods=['POST'])
def ask():
    """Endpoint to handle user questions and provide answers based on the scraped content."""
    data = request.json
    question = data.get('question')
    urls = data.get('urls', [])
    if not urls:
        return jsonify({'answer': 'No relevant content found.'})
    if question:
        relevant_content = vectordb.query_vectordb(question, urls)
        if relevant_content:
            prompt = f"""
            You are an AI assistant that answers queries strictly based on the given context. 
            If the answer is not found in the context, respond with "Not relevant."
            Context:
            {relevant_content}
            Question: {question}
            Answer concisely and accurately, using only the provided context.
            """
            answer = model.invoke_model_api(prompt)
            return jsonify({'answer': answer})
        else:
            return jsonify({'answer': 'No relevant content found.'})
    else:
        return jsonify({'answer': 'No relevant content found.'})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
