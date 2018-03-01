from docx import Document
import mysql.connector
import os
from mysql.connector import errorcode
from collections import OrderedDict


config = {
    'user': 'root',
    'password': 'Shaked1234',
    'host': '127.0.0.1',
    'database': 'test',
    'raise_on_warnings': True,
}


class DBHandler(object):
    def __init__(self, db_name):
        self._db = None
        self._cur = None
        config['database'] = db_name

    def connect(self):
        try:
            self._db = mysql.connector.connect(**config)
            self._cur = self._db.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Bad username or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print err
        else:
            print "db connected!"

    def close_connection(self):
        self._db.close()

    def insert_to_db(self, table_name, **data):
        print "inserting to: {}".format(table_name, data)

    def __parse_file__(self, document):
        for para in document.paragraphs:
            words = para.text.split()
            for word in words:
                b = "!@#$'/."
                for char in b:
                    word = word.replace(char, "")

    def load_new_doc(self, doc_path):
        print("Emanuel got new file!")
        document = Document(doc_path)
        self.__parse_file__(document)
        document.save("C:\Users\shaked zrihen\Documents\Emanuel\storedFiles\\{}.docx".format(generate_id()()))
        os.remove(doc_path)
        print("File was transferred from inputFiles to storedFiles")

    def search(self, term):
        pass


def generate_id():
    docs_id = [100]

    def new_doc_id():
        docs_id[0] += 1
        return docs_id[0]
    return new_doc_id


if __name__ == '__main__':
    my_db = DBHandler("emanueldb")
    my_db.connect()
    my_db.load_new_doc("C:\Users\shaked zrihen\Documents\Emanuel\inputFiles\\test.docx")


