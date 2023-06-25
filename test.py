import json
import random
import string
import subprocess

# Helper function to generate a random alphanumeric string
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Helper function to generate a random JSON file
def generate_random_json_file():
    data = {}
    for _ in range(random.randint(1, 5)):
        key = generate_random_string(random.randint(3, 8))
        value = generate_random_string(random.randint(3, 8))
        data[key] = value
    return json.dumps(data)

# Helper function to execute the command and get the output
def execute_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    output, error = process.communicate()
    return output.decode('utf-8')

# Automated testing
def run_tests():
    num_tests = 10
    passed_tests = 0

    for i in range(num_tests):
        # Generate a random JSON file
        json_file = f'test{i}.json'
        json_data = generate_random_json_file()
        with open(json_file, 'w') as file:
            file.write(json_data)

        # Generate random commands
        commands = []
        for _ in range(random.randint(5, 10)):
            op = random.choice(['del', '='])
            key = generate_random_string(random.randint(3, 8))
            value = generate_random_string(random.randint(3, 8))
            command = f'{op} {key} {value}'
            commands.append(command)

        # Apply commands to the JSON file
        for command in commands:
            execute_command(f'python your_program.py {json_file} {command}')

        # Check if modifications were executed correctly
        with open(json_file, 'r') as file:
            modified_json_data = file.read()
            modified_json_obj = json.loads(modified_json_data)

            expected_json_obj = json.loads(json_data)
            for command in commands:
                parts = command.split(' ', 2)
                op = parts[0]
                key = parts[1]
                value = parts[2]

                if op == 'del':
                    if key in expected_json_obj:
                        del expected_json_obj[key]
                elif op == '=':
                    expected_json_obj[key] = value

            if modified_json_obj == expected_json_obj:
                passed_tests += 1
                print(f'Test {i+1}: PASSED')
            else:
                print(f'Test {i+1}: FAILED')

    print(f'Passed {passed_tests}/{num_tests} tests')

if __name__ == '__main__':
    run_tests()
