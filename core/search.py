class DocumentSearch:

    def __init__(self):
        # receive database connection
        pass

    def add(self, document_search_graph, word, id):
        self.document_search_graph = document_search_graph

        document_id = document['id']
        words = document.lower().split(" ")
        
        for word in words:
            self.document_search_graph[word].append(document_id)

    def search(self, search_string):
        all_occurrences = []
        search_string = search_string.split(" ")

        for string in search_string:
            if string in self.document_search_graph:
                all_occurrences.append(self.document_search_graph[string])
        print(f'all_occurrences is {all_occurrences}')
        
        result_id = set().union(*all_occurrences)
        print(f'result_id is {result_id}')
        
        return result_id or []

    def delete(self, word):
        # this is not the add to filter function. This is the
        # main delete that gets called once in a month
        pass