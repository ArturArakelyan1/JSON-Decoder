def parse_json(json_str):
    stack = []
    current_obj = {}
    current_key = None
    in_string = False
    escape_next = False

    for char in json_str:
        if escape_next:
            if in_string:
                current_obj[current_key] += char
            escape_next = False
        elif char == '\\':
            escape_next = True
        elif char == '"':
            in_string = not in_string
            if not in_string:
                if current_key is None:
                    stack.append(current_obj)
                else:
                    current_key = None
        elif not in_string:
            if char in ['{', '[']:
                if current_key is not None:
                    stack.append(current_obj)
                current_obj = {}
                current_key = None
            elif char in ['}', ']']:
                if stack:
                    prev_obj = stack.pop()
                    if isinstance(prev_obj, list):
                        prev_obj.append(current_obj)
                        current_obj = prev_obj
                        current_key = None
                    elif isinstance(prev_obj, dict):
                        prev_obj[current_key] = current_obj
                        current_obj = prev_obj
                        current_key = None
                else:
                    return current_obj
            elif char == ':':
                current_key = ''
            elif char == ',':
                if isinstance(current_obj, list):
                    current_obj.append(None)
                elif isinstance(current_obj, dict):
                    current_key = None
            elif char not in [' ', '\n', '\r', '\t']:
                if current_key is None:
                    current_key = char
                else:
                    current_key += char

        elif in_string:
            if current_key is None:
                current_key = char
            else:
                current_key += char

    return current_obj


def update_json(json_obj, key, value):
    keys = key.split('.')
    current_obj = json_obj

    for k in keys[:-1]:
        if k not in current_obj:
            return False
        current_obj = current_obj[k]

    if isinstance(current_obj, dict):
        current_obj[keys[-1]] = value
    else:
        return False

    return True


def delete_json(json_obj, key):
    keys = key.split('.')
    current_obj = json_obj

    for k in keys[:-1]:
        if k not in current_obj:
            return False
        current_obj = current_obj[k]

    if isinstance(current_obj, dict) and keys[-1] in current_obj:
        del current_obj[keys[-1]]
    else:
        return False

    return True


def get_user_input(prompt):
    try:
        # For Python 2.x, use 'raw_input' instead of 'input'
        return input(prompt)
    except KeyboardInterrupt:
        return None


def main():
    json_file = get_user_input("Enter the path to the JSON file: ")
    if not json_file:
        print("Invalid input. Exiting...")
        return

    try:
        with open(json_file, 'r') as file:
            json_str = file.read()
            json_obj = parse_json(json_str)
    except IOError:
        print("Error reading JSON file. Exiting...")
        return

    print("JSON file contents:")
    print(json_str)
    print("")

    while True:
        command = get_user_input("Enter a command ('del key' or 'key = value'): ")
        if not command:
            print("Invalid input. Exiting...")
            return

        parts = command.split(' ', 2)
        if len(parts) != 3:
            print("Invalid command. Please follow the format 'del key' or 'key = value'.")
            continue

        op = parts[0]
        key = parts[1]
        value = parts[2]

        if op == 'del':
            if delete_json(json_obj, key):
                print("Field '{}' deleted.".format(key))
            else:
                print("Field '{}' not found or cannot be deleted.".format(key))
        elif op == '=':
            if update_json(json_obj, key, value):
                print("Field '{}' updated with value '{}'.".format(key, value))
            else:
                print("Field '{}' not found or cannot be updated.".format(key))
        else:
            print("Invalid operation. Please use 'del' or '='.")

        print("")
        print("Updated JSON:")
        print(json_obj)

if __name__ == '__main__':
    main()
