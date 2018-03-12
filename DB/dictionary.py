from collections import Counter, OrderedDict
from math import log

class Dictionary(object):
    def __init__(self):
        self._dictionary = {}
        self.stop_list = ["i", "and", "a", "an", "the", "to", "am"]
        self.operators = {
            '&': '%26',
            '|': '%7c',
            '!': '%21',
            '"': '%22',
            '(': '%28',
            ')': '%28'
        }
        self._doc_list = set()
        self.hidden_docs = []

    def build_dictionary_from_table(self, table):
        self._dictionary = {}
        for row in table:
            term = row[0]
            doc = (row[1], row[2])
            self.add_to_dictionary(term, doc)
            self._doc_list.add(doc)

    def get_dictionary(self):
        return self._dictionary

    def add_to_dictionary(self, key, value):
        if key in self._dictionary:
            self._dictionary[key].append(value)
        else:
            self._dictionary[key] = [value]

    def get_wildcard_words(self, word):
        word = word.replace("*", "")
        return [key for key in self._dictionary if key.find(word) != -1]

    def find_in_dictionary(self, word):
        try:
            global words
            result = []
            if word.find('*') != -1:
                words = self.get_wildcard_words(word)
            else:
                words = [word]
            for a_word in words:
                for doc in self._dictionary[a_word]:
                    if word not in self.stop_list:
                        result.append(doc[0])
            return result
        except KeyError:
            return []

    def execute_and(self, right_operand, left_operand):
        result = list(set(right_operand) & set(left_operand))
        return result

    def execute_or(self, right_operand, left_operand):
        result = list(set(right_operand) | set(left_operand))
        return list(result)

    def execute_not(self, right_operand):
        result = [doc for doc in self._doc_list if doc not in right_operand]
        if len(result) < 1:
            return [[]]
        return result

    def hide_doc(self, doc_id):
        self.hidden_docs.append(doc_id)
        print self.hidden_docs

    def un_hide_doc(self, doc_id):
        self.hidden_docs.remove(doc_id)

    def __tf_tag__(self, tf):
        return 1 + log(tf, 10)

    def __idf__(self, docs_number, shows):
        return log(docs_number / shows, 10)

    def tf_idf(self, tf, idf):
        return tf * idf

    def calc_doc_value(self, doc, query):
        weight = 0
        for word in query:
            if word in self._dictionary:
                docs_contains_word = self._dictionary[word]
                temp_doc = None
                for docs in docs_contains_word:
                    if docs[0] == doc:
                        temp_doc = docs
                        break
                if temp_doc:
                    tf = self.__tf_tag__(temp_doc[1])
                    idf = self.__idf__(docs_number=len(self._doc_list), shows=len(self._dictionary[word]))
                    weight += self.tf_idf(tf, idf)
        return weight

    def sort(self, docs_list, query):
        # sort by ranking
        temp_list = {}
        for doc in docs_list:
            temp_list[doc] = self.calc_doc_value(doc, query)
        sorted_dict = sorted(temp_list.items(), key=lambda x: x[1])
        sorted_dict.reverse()
        sorted_list = []
        for key in sorted_dict:
            if key[0] in docs_list:
                sorted_list.append(key[0])
        return sorted_list

    def __sort_by_number_of_words(self, docs_list, query):
        temp_list = []
        for word in query:
            if word in self._dictionary:
                for doc in self._dictionary[word]:
                    temp_list.append(doc[0])
        sorted_dict = Counter(temp_list)
        sorted_dict = sorted(sorted_dict.items(), key=lambda x: x[1])
        sorted_dict.reverse()
        sorted_list = []
        for key in sorted_dict:
            if key[0] in docs_list:
                sorted_list.append(key[0])
        return sorted_list

