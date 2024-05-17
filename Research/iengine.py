import sys
from truth_table_check import truth_table_check
from forward_chaining import forward_chaining
from backward_chaining import backward_chaining

def parse_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    kb_content, query = content.split('ASK')
    kb_clauses = kb_content.split('TELL')[1].strip().split(';')
    kb_clauses = [clause.strip() for clause in kb_clauses if clause.strip()]
    query = query.strip()
    
    return kb_clauses, query

def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py <filename> <method>")
        return
    
    filename, method = sys.argv[1], sys.argv[2].upper()
    kb, query = parse_file(filename)
    
    if method == 'TT':
        result = truth_table_check(kb, query)
    elif method == 'FC':
        result = forward_chaining(kb, query)
    elif method == 'BC':
        result = backward_chaining(kb, query)
    else:
        print("Invalid method")
        return
    
    print(result)

if __name__ == "__main__":
    main()