def transpile(ast):
    cpp_code = "#include <iostream>\nusing namespace std;\n\n"
    
    for node in ast:
        if node[0] == 'DECLARE':
            if node[1] == 'Duny FR':
                cpp_type = 'char'
            elif node[1] == 'Alex M2':
                cpp_type = 'int'
            # ... outros tipos
            
            if len(node) == 4:
                cpp_code += f"{cpp_type} {node[2]} = {node[3]};\n"
            else:
                cpp_code += f"{cpp_type} {node[2]};\n"
    
    return cpp_code