

class Dictionary(object):
    def __init__(self):
        self._dictionary = {}
        self.stop_list = ["i", "and", "a", "an", "the", "to", "for", "no", "yes"]
        self.operators = {
            '&': '%26',
            '|': '%7c',
            '!': '%21',
            '"': '%22',
            '(': '%28',
            ')': '%28'
        }
        self._doc_list = set()
        self._hidden_docs = []

    def build_dictionary_from_table(self, table):
        self._dictionary = {}
        for row in table:
            term = row[0]
            doc = row[1]
            self.add_to_dictionary(term, doc)
            self._doc_list.add(doc)

    def get_dictionary(self):
        return self._dictionary

    def add_to_dictionary(self, key, value):
        if key in self._dictionary:
            self._dictionary[key].append(value)
        else:
            self._dictionary[key] = [value]

    def find_in_dictionary(self, word):
        try:
            return filter(lambda doc: doc not in self._hidden_docs, self._dictionary[word])
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
        self._hidden_docs.append(doc_id)

    def un_hide_doc(self, doc_id):
        self._hidden_docs.remove(doc_id)