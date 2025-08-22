import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Flask application setup
app = Flask(__name__)
CORS(app)

# Configuration
GOOGLE_API_KEY = 'AIzaSyBkXCSIbrHo6o5cnF4AyQCsQAvlKhIky_Q'  # Set your Google API Key here
model_name = "gemini-pro"

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)

# Load PDF and create the vector store
def create_vector_store(pdf_path):
    pdf_loader = PyPDFLoader(pdf_path)
    pages = pdf_loader.load_and_split()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(p.page_content) for p in pages)
    texts = text_splitter.split_text(context)
    
    # Generate embeddings using Google Generative AI
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    
    # Create FAISS vector store from texts and embeddings
    vector_store = FAISS.from_texts(texts, embeddings)
    
    return vector_store

# Create the vector store from the PDF
pdf_path = os.path.join('documents', 'Vision_Park_Chatbot_Training_Data.pdf')
vector_index = create_vector_store(pdf_path)

# Set up the QA chain
template = """Answer all questions either from Google or the provided PDF also you can generate yourself related to my pdf and answer the greeting question in good manner sticking with our web visionpark.If you didn't find the question related to vision park topic on pdf but you can responde it in a polite manner like sorry for the inconvenience i can't answer it, you can ask me other things like this way, don't tell you didn't find in pdf, stick with the vision park. if you didn't find the answer you can generate it if that qn is like how are you or any other good conversation things.Be little bit concise.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vector_index.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

@app.route('/')
def index():
    return render_template('index.html')  # This will look for index.html in the templates folder

@app.route('/chat', methods=['POST'])
def chat():
    user_question = request.json.get('message')  # Ensure the key matches what the client sends
    result = qa_chain({"query": user_question})
    return jsonify({'response': result["result"]})

if __name__ == "__main__":
    app.run(port=5000)
    # app.run(host="0.0.0.0",port=5000, debug=True)
    app.debug = False
    
