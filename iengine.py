import sys
from truth_table_checking_dp import truth_table_check


def parse_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    try:
        kb_content, query = content.split('ASK')
        kb_clauses = kb_content.split('TELL')[1].strip().split(';')
    except IndexError:
        print("Error: File content is not properly formatted. Please include 'TELL' and 'ASK' sections.")
        sys.exit(1)

    kb_clauses = [clause.strip() for clause in kb_clauses if clause.strip()]
    query = query.strip()
    
    if not kb_clauses or not query:
        print("Error: Knowledge base or query is empty after parsing.")
        sys.exit(1)
    
    return kb_clauses, query

def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py <filename> <method>")
        return
    
    filename, method = sys.argv[1], sys.argv[2].upper()
    kb, query = parse_file(filename)
    
    print("Initial Knowledge Base:")
    for clause in kb:
        print(clause)
    print("Query:")
    print(query)
    
    if method == 'TT':
        result = truth_table_check(kb, query)
    else:
        print("Invalid method")
        return
    
    print(result)

if __name__ == "__main__":
    main()
