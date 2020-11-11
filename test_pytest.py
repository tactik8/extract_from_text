import pytest

import constants as const

from extractors import \
    email_extractor_regex, \
    url_extractor_ioc_finder,\
    url_extractor_regex,\
    phone_extractor_ioc_finder,\
    qty_extractor_quantulum3,\
    title_extractor,\
    geo_extractor_geograpy3

class Test_Validation:
    '''
    Since all extractors share common validation mechanism - all tests are NOT
    repeated for each extractor, but rather distributed between them.
    '''
    def test_negative_none_input(self):
        assert email_extractor_regex(None) == list()

    def test_negative_faulty_type_input(self):
        assert url_extractor_ioc_finder(65) == list()

    def test_empty_str_input(self):
        assert url_extractor_regex('') == list()

    def test_empty_list_input(self):
        assert url_extractor_regex(list()) == list()

    def test_negative_not_str_list_input(self):
        assert phone_extractor_ioc_finder([12, None]) == list()

    def test_negative_partial_str_list_input(self):
        '''
        Input list has one argument of a type string, second argument has None
        type.
        Outpus should contain one record.
        '''
        TEST_EMAIL = 't@t.t'

        real_output = email_extractor_regex([TEST_EMAIL, None])

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.EMAIL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.EMAIL_SCHEMA]== TEST_EMAIL)
            
            pytest.assume(
              real_output[0][const.KRK_EXTRACTOR] == const.EMAIL_EXTRACTOR_NAME)


class Test_Positive_Email:
    'Contains positive scenarios TCs for the email extractor.'

    def test_str_input_one_valid_val(self):
        TEST_EMAIL = 't@t.t'
        INPUT_TEXT = f'Hi! Here is my email: {TEST_EMAIL}'

        real_output = email_extractor_regex(INPUT_TEXT)

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.EMAIL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.EMAIL_SCHEMA]== TEST_EMAIL)
            
            pytest.assume(
              real_output[0][const.KRK_EXTRACTOR] == const.EMAIL_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals(self):
        TEST_EMAIL_1 = 't@t.t'
        TEST_EMAIL_2 = 'test@testing.this'
        TEST_EMAIL_3 = 'john@doe.lorem'

        output_emails = [TEST_EMAIL_1, TEST_EMAIL_2, TEST_EMAIL_3]

        INPUT_TEXT = f'Hi! Here is my email: {TEST_EMAIL_1}, ' \
                   + f'a 2nd one: {TEST_EMAIL_2}, and the 3rd: {TEST_EMAIL_3}'

        real_output = email_extractor_regex(INPUT_TEXT)

        pytest.assume(len(real_output) == len(output_emails))

        for p in range(0, len(output_emails)):

            pytest.assume(
                real_output[p][const.TYPE] == const.EMAIL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[p][const.EMAIL_SCHEMA]== output_emails[p])
            
            pytest.assume(
              real_output[p][const.KRK_EXTRACTOR] == const.EMAIL_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals(self):
        INPUT_TEXT = f'Hi! I have no email...'

        real_output = email_extractor_regex(INPUT_TEXT)

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        TEST_EMAIL_1 = 't@t.t'
        TEST_EMAIL_2 = 'test@testing.this'
        TEST_EMAIL_3 = 'john@doe.lorem'
        TEST_EMAIL_4 = 'ipsum@doe.lorem'

        output_emails = [TEST_EMAIL_1, TEST_EMAIL_2, TEST_EMAIL_3, TEST_EMAIL_4]

        INPUT_LIST = [f'Hi! Here is my emails: {TEST_EMAIL_1}, {TEST_EMAIL_2}',
                      f'also those: {TEST_EMAIL_3}, and {TEST_EMAIL_4}']

        real_output = email_extractor_regex(INPUT_LIST)

        pytest.assume(len(real_output) == len(output_emails))

        for p in range(0, len(output_emails)):

            pytest.assume(
                real_output[p][const.TYPE] == const.EMAIL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[p][const.EMAIL_SCHEMA]== output_emails[p])
            
            pytest.assume(
              real_output[p][const.KRK_EXTRACTOR] == const.EMAIL_EXTRACTOR_NAME)


class Test_Positive_URL_Ioc:
    'Contains positive scenarios TCs for the URL_IOC extractor.'

    def test_str_input_one_valid_val(self):
        TEST_INPUT = 'https://www.hi.com/'
        INPUT_TEXT = f'Hi! Here is my site: {TEST_INPUT}'

        real_output = url_extractor_ioc_finder(INPUT_TEXT)

        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')
        
        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.URL_SCHEMA] == TEST_INPUT)
            
            pytest.assume(
                real_output[0][const.KRK_EXTRACTOR]\
                  == \
                const.URL_IOC_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals(self):
        TEST_INPUT_1 = 'https://www.this.de'
        TEST_INPUT_2 = 'http://fun.us'
        TEST_INPUT_3 = 'https://schema.org/url'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3]

        INPUT_TEXT = f'Hi! Here is my site: {TEST_INPUT_1}, ' \
                   + f'a 2nd one: {TEST_INPUT_3} and the 3rd: {TEST_INPUT_2}'

        real_output = url_extractor_ioc_finder(INPUT_TEXT)

        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            real_val = real_output[p][const.URL_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.URL_IOC_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals(self):
        INPUT_TEXT = f'Hi! I have no site...'

        real_output = url_extractor_ioc_finder(INPUT_TEXT)

        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        TEST_INPUT_1 = 'https://www.this.de'
        TEST_INPUT_2 = 'http://fun.us'
        TEST_INPUT_3 = 'https://schema.org/url'
        TEST_INPUT_4 = 'http://schema.org/email'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3, TEST_INPUT_4]

        INPUT_LIST = [f'Hi! My urls: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']

        real_output = url_extractor_ioc_finder(INPUT_LIST)

        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            real_val = real_output[p][const.URL_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.URL_IOC_EXTRACTOR_NAME)


class Test_Positive_URL_RE:
    'Contains positive scenarios TCs for the URL regex extractor.'

    def test_str_input_one_valid_val(self):
        # Preparations
        TEST_INPUT = 'www.hi.com/'
        INPUT_TEXT = f'Hi! Here is my site: {TEST_INPUT}'

        # Test Execution
        real_output = url_extractor_regex(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.URL_SCHEMA] == TEST_INPUT)
            
            pytest.assume(
                real_output[0][const.KRK_EXTRACTOR]\
                  == \
                const.URL_RE_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'https://www.this.de'
        TEST_INPUT_2 = 'www.fun.us'
        TEST_INPUT_3 = 'https://schema.org/url/'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3]

        INPUT_TEXT = f'Hi! Here is my site: {TEST_INPUT_1} ' \
                   + f'a 2nd one: {TEST_INPUT_3} and the 3rd: {TEST_INPUT_2}'

        # Test Execution
        real_output = url_extractor_regex(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            real_val = real_output[p][const.URL_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.URL_RE_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals(self):
        # Preparations
        INPUT_TEXT = f'Hi! I have no site...'

        # Test Execution
        real_output = url_extractor_regex(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'https://www.this.de'
        TEST_INPUT_2 = 'http://fun.us'
        TEST_INPUT_3 = 'https://schema.org/url'
        TEST_INPUT_4 = 'http://schema.org/email'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3, TEST_INPUT_4]

        INPUT_LIST = [f'Hi! My urls: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']
                      
        # Test Execution
        real_output = url_extractor_regex(INPUT_LIST)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.URL_SCHEMA_TYPE)
    
            real_val = real_output[p][const.URL_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.URL_RE_EXTRACTOR_NAME)


class Test_Positive_Phone_Ioc:
    'Contains positive scenarios TCs for the PhoneIOC extractor.'

    def test_str_input_one_valid_val(self):
        # Preparations
        TEST_INPUT = '(123) 456 7890'
        INPUT_TEXT = f'Hi! Here is my number: {TEST_INPUT}'

        # Test Execution
        real_output = phone_extractor_ioc_finder(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.PHONE_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.NAME_SCHEMA] == TEST_INPUT)
            
            pytest.assume(
                real_output[0][const.KRK_EXTRACTOR]\
                  == \
                const.PHONE_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = '(123) 456 7890'
        TEST_INPUT_2 = '(123).123.4567'
        TEST_INPUT_3 = '(123)-123-4567'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3]

        INPUT_TEXT = f'Hi! Here are my phones: {TEST_INPUT_1} ' \
                   + f'a 2nd one: {TEST_INPUT_3} and the 3rd: {TEST_INPUT_2}'

        # Test Execution
        real_output = phone_extractor_ioc_finder(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.PHONE_SCHEMA_TYPE)
    
            real_val = real_output[p][const.NAME_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.PHONE_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals(self):
        # Preparations
        INPUT_TEXT = f'Hi! I have no number...'

        # Test Execution
        real_output = phone_extractor_ioc_finder(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = '(123) 456 7890'
        TEST_INPUT_2 = '(123).123.4567'
        TEST_INPUT_3 = '123 4567'
        TEST_INPUT_4 = '123 - 456 - 7890'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3, TEST_INPUT_4]

        INPUT_LIST = [f'Hi! My phones: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']
                      
        # Test Execution
        real_output = phone_extractor_ioc_finder(INPUT_LIST)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')
   
        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.PHONE_SCHEMA_TYPE)
    
            real_val = real_output[p][const.NAME_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.PHONE_EXTRACTOR_NAME)


class Test_Positive_Quantities:
    'Contains positive scenarios TCs for the quantities extractor.'

    def test_str_input_one_valid_val_quant(self):
        # Preparations
        TEST_INPUT = 'one year'
        EXPECTED_OUTPUT = '1.0 year'
        INPUT_TEXT = f'Hi! I work for : {TEST_INPUT}'

        # Test Execution
        real_output = qty_extractor_quantulum3(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.QUANTITY_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.QUANTITY_SCHEMA] == EXPECTED_OUTPUT)
            
            pytest.assume(
                real_output[0][const.KRK_EXTRACTOR]\
                  == \
                const.QUANTITY_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals_quant(self):
        # Preparations
        TEST_INPUT_1 = 'a gallon of beer'
        TEST_INPUT_2 = 'nine litres'
        TEST_INPUT_3 = '7 dollars'

        output_vals = ['1.0 gallon', '9.0 cubic decimetre', '7.0 dollar']

        INPUT_TEXT = f'Lets talk about {TEST_INPUT_1} ' \
                   + f'and  {TEST_INPUT_3}. Also about {TEST_INPUT_2}'

        # Test Execution
        real_output = qty_extractor_quantulum3(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.QUANTITY_SCHEMA_TYPE)
    
            real_val = real_output[p][const.QUANTITY_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.QUANTITY_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals_quant(self):
        # Preparations
        INPUT_TEXT = f'Hi! I have no number...'

        # Test Execution
        real_output = qty_extractor_quantulum3(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals_quant(self):
        # Preparations
        TEST_INPUT_1 = 'a gallon of beer'
        TEST_INPUT_2 = 'nine litres'
        TEST_INPUT_3 = '10 days'
        TEST_INPUT_4 = '7 dollars'

        output_vals = ['1.0 gallon', 
                       '9.0 cubic decimetre', 
                       '7.0 dollar', 
                       '10.0 day']

        INPUT_LIST = [f'Hi! My phones: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']
                      
        # Test Execution
        real_output = qty_extractor_quantulum3(INPUT_LIST)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')
   
        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.QUANTITY_SCHEMA_TYPE)
    
            real_val = real_output[p][const.QUANTITY_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.QUANTITY_EXTRACTOR_NAME)


class Test_Positive_Job_Titles:
    'Contains positive scenarios TCs for the Job Titles extractor.'

    def test_str_input_one_valid_val(self):
        # Preparations
        TEST_INPUT = 'Software Developer'
        INPUT_TEXT = f'Hi! I am a {TEST_INPUT}'

        # Test Execution
        real_output = title_extractor(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 1)

        if len(real_output) > 0:
            pytest.assume(
                real_output[0][const.TYPE] == const.JOB_TITTLE_SCHEMA_TYPE)
    
            pytest.assume(
                real_output[0][const.JOB_TITTLE_SCHEMA] == TEST_INPUT)
            
            pytest.assume(
                real_output[0][const.KRK_EXTRACTOR]\
                  == \
                const.JOB_TITTLE_EXTRACTOR_NAME)

    def test_str_input_three_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'Junior Software Developer'
        TEST_INPUT_2 = 'CTO'
        TEST_INPUT_3 = 'Marketing Coordinator'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3]

        INPUT_TEXT = f'Hi! HI was a : {TEST_INPUT_1} ' \
                   + f', {TEST_INPUT_3} and  {TEST_INPUT_2}'

        # Test Execution
        real_output = title_extractor(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.JOB_TITTLE_SCHEMA_TYPE)
    
            real_val = real_output[p][const.JOB_TITTLE_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.JOB_TITTLE_EXTRACTOR_NAME)
    
    def test_str_no_valid_vals(self):
        # Preparations
        INPUT_TEXT = f'Hi! I have no titles...'

        # Test Execution
        real_output = title_extractor(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'Medical Assistant'
        TEST_INPUT_2 = 'Web Designer'
        TEST_INPUT_3 = 'Dog Trainer'
        TEST_INPUT_4 = 'President'

        output_vals = [TEST_INPUT_1, TEST_INPUT_2, TEST_INPUT_3, TEST_INPUT_4]

        INPUT_LIST = [f'Hi! I want to be: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']
                      
        # Test Execution
        real_output = title_extractor(INPUT_LIST)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == len(output_vals))

        for p in range(0, len(output_vals)):

            pytest.assume(
                real_output[p][const.TYPE] == const.JOB_TITTLE_SCHEMA_TYPE)
    
            real_val = real_output[p][const.JOB_TITTLE_SCHEMA]

            print (f'\n    Curr output to validate:   {str(real_val)}')
            print (f'    Input vals left:           {str(output_vals)}')

            pytest.assume(real_val in output_vals)

            if real_val in output_vals:
                output_vals.remove(real_val)
            else:
                print('        Assumption failed...')
            
            pytest.assume(
                real_output[p][const.KRK_EXTRACTOR] \
                  == \
                const.JOB_TITTLE_EXTRACTOR_NAME)


class Test_Positive_Geography:
    'Contains positive scenarios TCs for the Geography extractor.'

    def _validate_output(self, exp_len, exp_schema_to_exp_val, real_output):

        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        print(
            f'\n    Expected output lenght: {str(exp_len)}') 

        print(
            f'\n    Actual output lenght:   {str(len(real_output))}')

        pytest.assume(len(real_output) == exp_len)

        for output in real_output:
            pytest.assume(
                output[const.TYPE] == const.GEOGRAPHY_SCHEMA_TYPE)

            pytest.assume(
                output[const.KRK_EXTRACTOR]\
                  == \
                const.GEOGRAPHY_EXTRACTOR_NAME)

            is_name_schema = const.NAME_SCHEMA in output 
            is_geo_schema  = const.GEOGRAPHY_SCHEMA in output
            

            expected_schema = is_name_schema or is_geo_schema

            pytest.assume(expected_schema)

            if expected_schema:
                value  = None
                schema = None
                
                if   is_name_schema: schema = const.NAME_SCHEMA
                elif is_geo_schema:  schema = const.GEOGRAPHY_SCHEMA

                print(f'\n  Scheme is {schema}')

                value = output.get(schema)

                expected_value = value in exp_schema_to_exp_val[schema]

                outpus_as_str = str(exp_schema_to_exp_val[schema])

                print (f'    Curr output to validate:   {str(value)}')
                print (f'    Input vals left:           {outpus_as_str}')

                pytest.assume(expected_value)

                if expected_value:
                    exp_schema_to_exp_val[schema].remove(value)
                else:
                    print('        Assumption failed...')

    def test_str_input_one_valid_val(self):
        # Preparations
        TEST_INPUT = 'Ukraine'
        
        EXPECTED_SCHEMA_TO_EXP_VALUE = \
        {
            const.NAME_SCHEMA      : ['Ukraine'],
            const.GEOGRAPHY_SCHEMA : ['UA']
        }

        EXPECTED_OUTPUT_LENGHT = 2

        INPUT_TEXT = f'I am a from {TEST_INPUT}'

        # Test Execution
        real_output = geo_extractor_geograpy3(INPUT_TEXT)

        # Result Validation
        self._validate_output(EXPECTED_OUTPUT_LENGHT, 
                              EXPECTED_SCHEMA_TO_EXP_VALUE,
                              real_output)

    def test_str_input_three_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'United States'
        TEST_INPUT_2 = 'Canada'
        TEST_INPUT_3 = 'USA'        

        EXPECTED_SCHEMA_TO_EXP_VALUE = \
        {
            const.NAME_SCHEMA      : ['Canada', 'United States'],
            const.GEOGRAPHY_SCHEMA : ['Canada', 'CA', 'US', 'ES']
        }

        EXPECTED_OUTPUT_LENGHT = 6

        INPUT_TEXT = f'I was in : {TEST_INPUT_1} ' \
                   + f', {TEST_INPUT_3} and  {TEST_INPUT_2}'

        # Test Execution
        real_output = geo_extractor_geograpy3(INPUT_TEXT)

        # Result Validation
        self._validate_output(EXPECTED_OUTPUT_LENGHT, 
                              EXPECTED_SCHEMA_TO_EXP_VALUE,
                              real_output)

    def test_str_no_valid_vals(self):
        # Preparations
        INPUT_TEXT = f' I have nothing to say...'

        # Test Execution
        real_output = geo_extractor_geograpy3(INPUT_TEXT)

        # Result Validation
        if len(real_output) == 0:
            print(f'\n    Real output: {str(real_output)}')
        else:
            print(f'\n    Real output:')

            for rec in real_output:
                print(f'        {str(rec)}')

        pytest.assume(len(real_output) == 0)

    def test_list_input_four_valid_vals(self):
        # Preparations
        TEST_INPUT_1 = 'Germany'
        TEST_INPUT_2 = 'London'
        TEST_INPUT_3 = 'Kingdom of Denmark'
        TEST_INPUT_4 = 'France'

        EXPECTED_SCHEMA_TO_EXP_VALUE = \
        {
            const.NAME_SCHEMA      : ['Germany', 'France', 'Denmark', 'London'],
            const.GEOGRAPHY_SCHEMA : 
                ['London', 
                 'Denmark', 
                 'DE', 
                 'FR', 
                 'DK', 
                 'AU', 
                 'GB', 
                 'US',
                 'CA']
        }

        EXPECTED_OUTPUT_LENGHT = 13


        INPUT_LIST = [f'I was in: {TEST_INPUT_1} and {TEST_INPUT_4} ',
                      f'also: {TEST_INPUT_3} and : {TEST_INPUT_2}']
                      
        # Test Execution
        real_output = geo_extractor_geograpy3(INPUT_LIST)

        # Result Validation
        self._validate_output(EXPECTED_OUTPUT_LENGHT, 
                              EXPECTED_SCHEMA_TO_EXP_VALUE,
                              real_output)