#!/usr/bin/python3
import re

def match_pattern(string, pattern, m):
    res = pattern.match(string)
    if res is not None:
        first, last = res.span()
        if last - first == m:
            return True

    return False
    
def count_num_occur(string, n, pattern, m):
    count = 0
    i = 0
    regex = re.compile(pattern)
    for i in range(len(string) - m + 1):
        substr = string[i: i + m]
        print(substr)
        if match_pattern(substr, regex, m):
            count += 1
    return count

if __name__ == "__main__":
    input_1 = input()
    tokens = input_1.strip().split()
    n, m = int(tokens[0]), int(tokens[1])
    input_str = input()
    pattern = input()
    pattern = pattern.replace("*", ".*")

    print(count_num_occur(str(input_str), n, str(pattern), m))

