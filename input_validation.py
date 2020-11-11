import logging

import constants as const



def validate_text_input(input):

    result = const.RC_VALID_INPUT

    if   input == None:
        logging.warning('None received as an extractor input')
        result = const.RC_NONE_INPUT

    elif type(input) == list:

        has_strings     = False
        has_non_strings = False

        for rec in input:
            if rec == None or type(rec) != str:
                has_non_strings = True
            else:
                has_strings = True

        if has_strings and has_non_strings:
            logging.warning(
                'Input list contains both str and non-str parameters.')
            result = const.RC_PARTLY_VALID_LIST_INPUT

        elif has_strings and not has_non_strings:
            logging.debug('Valid input list received.')

            result = const.RC_VALID_INPUT

        elif not has_strings and has_non_strings:
            logging.error(
                'Input list doesnt contain strings.')
            result = const.RC_WRONG_LIST_TYPES_INPUT

        else:
            logging.warning('Input list is empty.')
            result = const.RC_EMPTY_LIST_INPUT

    
    elif type(input) != str:
        logging.error('Input parameter type is not string nor list.')
        result = const.RC_WRONG_TYPE_INPUT
    
    return result


def allow_only_string(func):
    
    def extractor(input):

        rc = validate_text_input(input)
        if rc not in const.VALID_RC_CODES:
            #return {'Result' : 'Failure', 
            #        'Result code' : rc, 
            #        'Reason' : const.RC_TO_TEXT_REASON[rc]}

            return []
        

        return func(input)
    return extractor

