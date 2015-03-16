#!/usr/bin/python
from sortedcontainers import SortedListWithKey
time = 0
query_result = {}
query_reverse_index = {}
class Boost:
    def __init__(self):
        self.boost_type = ''
        self.boost_id = ''
        self.boost_value = 0.0

class Result:
    def __init__(self):
        self.result_id = ''
        self.result_type = ''
        self.result_score = 1.0
        self.result_time = 0

    def __str__(self):
        return "id = %s, type = %s, score = %f, time = %d"%(self.result_id, self.result_type, self.result_score, self.result_time)

    def boost(self, boosts):
        result = Result()
        result.result_type = self.result_type
        result.result_id = self.result_id
        result.result_score = self.result_score
        result.result_time = self.result_time

        for boost in boosts:
            if boost.boost_type == self.result_type:
                result.result_score *= boost.boost_value
            if boost.boost_id == self.result_id:
                result.result_score *= boost.boost_value
        return result

def sort_result(lhs, rhs):
    if lhs.result_score < rhs.result_score:
        return 1
    if lhs.result_score == rhs.result_score and lhs.result_time < rhs.result_time:
        return 1
    return -1


class Node:
    def __init__(self):
        self.items = set()
        #this is the dictionary of character and other nodes
        self.children = {}
        self.reverse_index = {}

    def append_word(self, result, string, start, end):
        node = None

        for i in range(end):
            substring = string[0: i+1]
            if substring not in self.children:
                self.children[substring] = set()
            self.children[substring].add(result)
            if result.result_id not in self.reverse_index:
                self.reverse_index[result.result_id] = []
            self.reverse_index[result.result_id].append(substring)


    def remove_result(self, result):
        if result.result_id in self.reverse_index:
            words = self.reverse_index[result.result_id]
            for word in words:
                for res in self.children[word]:
                    if result.result_id == res.result_id:
                        self.children[word].remove(res)
                        break
            self.reverse_index.pop(result.result_id, None)

    def find(self, string, start, end):
        if string in self.children:
            return self.children[string]
        else:
            return None


class Tree:
    def __init__(self):
        self.root_node = Node()

    def insert(self, result, string):
        self.root_node.append_word(result, string.lower(), 0, len(string))


    def remove(self, result):
        self.root_node.remove_result(result)

    def find(self, tokens, boosts, max_num = 20):
        results = []
        for token in tokens:
            token = token.lower()
            node = self.root_node.find(token, 0, len(token))
            if node is not None:
                results.append(node)
                #result_dict.append(set(node.keys()))


        intersect_results = set.intersection(*results)


        boosted_results = SortedListWithKey(key=lambda val: val.result_score)
        if len(boosts) > 0:
            for each_res in intersect_results:
                boosted_results.append(each_res.boost(boosts))
        else:
            for each_res in intersect_results:
                boosted_results.append(each_res)

        #boosted_results = sorted(boosted_results, cmp=sort_result)
        
        if len(boosted_results) > max_num:
            return boosted_results[0:max_num]
        else:
            return boosted_results

def parse_add_input(string):
    global time
    tokens = string.split()
    if len(tokens) < 5:
        return None, []
    result = Result()
    result.result_type = tokens[1]
    result.result_id = tokens[2]
    result.result_score = float(tokens[3])
    result.result_time = time
    time += 1
    words = tokens[4:]
    return result, words

def parse_delete_input(string):
    tokens = string.split()
    if len(tokens) < 2 or len(tokens) > 2:
        return None
    result = Result()
    result.result_id = tokens[1]
    return result

def parse_query_input(string):
    tokens = string.split()
    if len(tokens) < 3:
        return None, []
    num_results = int(tokens[1])
    words = tokens[2:]
    return num_results, words

def parse_boost(string):
    tokens = string.split(":")
    boost = Boost()
    if tokens[0] in ["topic", "user", "question", "board"]:
        boost.boost_type = tokens[0]
    else:
        boost.boost_id = tokens[0]
    boost.boost_value = float(tokens[1])
    return boost
    
def parse_wquery_input(string):
    tokens = string.split()
    num_results = int(tokens[1])
    num_boosts = int(tokens[2])
    boosts = []
    if num_boosts > 0:
        for token in tokens[3: 3 + num_boosts]:
            boosts.append(parse_boost(token))
    words = tokens[2 + num_boosts + 1 : ] 
    return num_results, boosts, words

if __name__ == "__main__":
    #tree = Tree()
    #result = Result()
    #result.result_id = 1
    #result.result_type = 'ADD'
    #result.result_time = 1
    #result.result_score = 1.0

    #tokens = ["madan", "patil"]

    #for token in tokens:
    #    tree.insert(result, token)
    #result = Result()
    #result.result_id = 2
    #result.result_type = 'ADD'
    #result.result_time = 2
    #result.result_score = 2.0
    #for token in tokens:
    #    tree.insert(result, token)
    #tokens = ["mad", "pat"]
    #results = tree.find(tokens, [], 3)
    #print results
    #tree.remove(result)
    #results = tree.find(tokens, [], 3)
    #print results
    
    tree = Tree()
    num_input = int(raw_input())
    for i in range(num_input):
        string = raw_input()
        if string.startswith("ADD"):
            result, words = parse_add_input(string)
            for word in words:
                tree.insert(result, word)
            print ''

        elif string.startswith("DEL"):
            result = parse_delete_input(string)
            if result:
                tree.remove(result)
            print ''
        
        elif string.startswith("QUERY"):
            num_results, words = parse_query_input(string)
            results = tree.find(words, [], num_results)
            ids = [result.result_id for result in results]
            print ' '.join(ids)

        elif string.startswith("WQUERY"):
            num_results, boosts, words = parse_wquery_input(string)
            results = tree.find(words, boosts, num_results)
            ids = [result.result_id for result in results]
            print ' '.join(ids)
        else:
            print ''
