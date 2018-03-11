from flask import Flask, request, render_template
from DB.handler import DBHandler
import mammoth

# from flask_restful import Resource, Api

app = Flask(__name__)
my_db = DBHandler()
my_db.connect()
words_to_bold = []

@app.route('/')
def index():
    # my_db.load_new_doc("E:\Emanuel\inputFiles\\All You Need Is Love.docx", title="All You Need Is Love", author="The Beatles", subject="Song")
    # my_db.load_new_doc("E:\Emanuel\inputFiles\\Come Together.docx", title="Come Together", author="The Beatles", subject="Song")
    # my_db.load_new_doc("E:\Emanuel\inputFiles\\For No One.docx", title="For No One", author="The Beatles", subject="Song")
    # my_db.load_new_doc("E:\Emanuel\inputFiles\\Strawberry Fields Forever.docx", title="Strawberry Fields Forever", author="The Beatles", subject="Song")
    my_db.build_dictionary()
    return render_template('index.html', data=None)


@app.route('/search')
def search():
    global words_to_bold
    query = request.query_string
    query = query.replace("query=", "")
    data, words_to_bold = my_db.search(query)
    query = query.replace("+", " ")
    query = query.replace("%29", ")")
    query = query.replace("%7C", "|")
    query = query.replace("%26", "&")
    query = query.replace("%28", "(")
    query = query.replace("%21", "!")
    query = query.replace("%22", '"')
    return render_template('search.html', data=data, len=len(data), query=query)


@app.route('/documents/<int:doc_id>')
def display_document(doc_id):
    with open("E:\Emanuel\storedFiles\{}.docx".format(doc_id), "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        str_res = result.value
        for word in words_to_bold:
            str_res = str_res.replace(word, '<b>{}</b>'.format(word))

        return render_template('resalt.html', text=str_res)


if __name__ == '__main__':
    app.run()
