from functions.get_file_content import get_file_content


lorem_ipsum_test = get_file_content('calculator', 'lorem.txt')
print('Lorem Ipsum Truncated:', lorem_ipsum_test.find('truncated') != -1)

print(get_file_content('calculator', 'main.py'))

print(get_file_content('calculator', 'pkg/calculator.py'))

print(get_file_content('calculator', '/bin/cat'))

print(get_file_content('calculator', 'pkg/does_not_exist.py'))