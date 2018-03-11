from flask import Flask, request, render_template, redirect
from DB.handler import DBHandler
import mammoth

# from flask_restful import Resource, Api

app = Flask(__name__)
my_db = DBHandler()
my_db.connect()
words_to_bold = []
IS_ADMIN = False


@app.route('/')
def index():
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
    if IS_ADMIN:
        return render_template('admingui.html', data=data, len=len(data), query=query)
    else:
        return render_template('search.html', data=data, len=len(data), query=query)


@app.route('/documents/<int:doc_id>')
def display_document(doc_id):
    with open("E:\Emanuel\storedFiles\{}.docx".format(doc_id), "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        str_res = result.value
        for word in words_to_bold:
            str_res = str_res.replace(word, '<b>{}</b>'.format(word))
        return render_template('resalt.html', text=str_res)


@app.route('/admin')
def show_admin():
    global IS_ADMIN
    IS_ADMIN = True
    return render_template('admingui.html', len=0, message_display="none", message="")


@app.route('/upload', methods=['POST'])
def upload():
    author = request.form["author"]
    subject = request.form["subject"]
    for file in request.files.getlist("file"):
        filename = file.filename
        my_db.load_new_doc(
            "E:\Emanuel\inputFiles\\{}".format(filename),
            title=filename,
            author=author,
            subject=subject
        )
    return render_template('admingui.html', len=0, message_display="block", message="File was uploaded successfully")


@app.route('/build-dict')
def re_index():
    my_db.build_dictionary()
    return render_template('admingui.html', len=0, message_display="block", message="Dictionary was updated!")


@app.route('/delete/<int:doc_id>')
def delete(doc_id):
    my_db.delete(doc_id)
    return render_template('admingui.html', len=0, message_display="block", message="File was delete!")


@app.route('/restore/<int:doc_id>')
def restore(doc_id):
    my_db.restore(doc_id)


@app.route('/logoff')
def log_off():
    global IS_ADMIN
    IS_ADMIN = False
    return redirect('/')


if __name__ == '__main__':
    app.run()
