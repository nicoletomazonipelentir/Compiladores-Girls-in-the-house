def transpile(ast):
    cpp_code = "#include <iostream>\nusing namespace std;\n\nint main() {\n"
    
    for node in ast:
        if node[0] == 'DECLARE':
            cpp_type = {
                'Duny': 'char',
                'Shaft': 'short',
                'Alex': 'int',
                'Todd': 'long'
            }.get(node[1], 'auto')
            
            if len(node) == 4:
                cpp_code += f"    {cpp_type} {node[2]} = {node[3]};\n"
            else:
                cpp_code += f"    {cpp_type} {node[2]};\n"
        elif node[0] == 'PRINT':
            cpp_code += f'    cout << {node[1]} << endl;\n'
    
    cpp_code += "    return 0;\n}\n"
    return cpp_code