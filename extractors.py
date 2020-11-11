import re
import nltk
import logging
import datetime
import phonenumbers

import geograpy
import country_converter
import pycountry

from ioc_finder import find_iocs
from quantulum3 import parser
from find_job_titles import FinderAcora


import constants as const

from input_validation import allow_only_string

@allow_only_string
def email_extractor_regex(input): 

    result = list()  

    emails_list = list()

    if type(input) == str:
        input = [input]

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        emails_list.extend(re.findall(const.EMAIL_PATTERN, string))


    emails_list = list(dict.fromkeys(emails_list))

    current_date_time = datetime.datetime.now()

    for em in emails_list:
        result.append(
            {
             const.TYPE          : const.EMAIL_SCHEMA_TYPE,
             const.EMAIL_SCHEMA  : em,
             const.KRK_EXTRACTOR : const.EMAIL_EXTRACTOR_NAME,
             const.KRK_DATE      : str(current_date_time)
            }
        )

    return result


@allow_only_string
def url_extractor_ioc_finder(input):

    result = list()  

    urls_list = list()

    if type(input) == str:
        input = [input]

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        urls_list.extend(find_iocs(string)['urls'])

    urls_list = list(dict.fromkeys(urls_list))

    current_date_time = datetime.datetime.now()

    for url in urls_list:
        result.append(
         {
          const.TYPE          : const.URL_SCHEMA_TYPE,
          const.URL_SCHEMA    : url,
          const.KRK_EXTRACTOR : const.URL_IOC_EXTRACTOR_NAME,
          const.KRK_DATE      : str(current_date_time)
         }
        )

    return result


@allow_only_string
def url_extractor_regex(input):

    result = list()  

    urls_list = list()

    if type(input) == str:
        input = [input]

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        urls_list.extend(re.findall(const.URL_PATTERN, string))

    urls_list = list(dict.fromkeys(urls_list))

    current_date_time = datetime.datetime.now()

    for url in urls_list:
        result.append(
         {
          const.TYPE          : const.URL_SCHEMA_TYPE,
          const.URL_SCHEMA    : url,
          const.KRK_EXTRACTOR : const.URL_RE_EXTRACTOR_NAME,
          const.KRK_DATE      : str(current_date_time)
         }
        )

    return result


@allow_only_string
def phone_extractor_ioc_finder(input):
    
    result = list()  

    phones_list = list()

    if type(input) == str:
        input = [input]

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        phones_list.extend(find_iocs(string)['phone_numbers'])

    phones_list = list(dict.fromkeys(phones_list))

    current_date_time = datetime.datetime.now()

    for phone in phones_list:
        
        phone_obj = None

        schema_to_use = const.PHONE_SCHEMA

        try:
            phone_obj = phonenumbers.parse(phone, None)
        except:
            schema_to_use = const.NAME_SCHEMA

        else:
            phone = phonenumbers.format_number(
                phone_obj, 
                phonenumbers.PhoneNumberFormat.E164)

        result.append(
            {
                const.TYPE          : const.PHONE_SCHEMA_TYPE,
                schema_to_use       : phone,
                const.KRK_EXTRACTOR : const.PHONE_EXTRACTOR_NAME,
                const.KRK_DATE      : str(current_date_time)
            }
        )

    return result


@allow_only_string
def geo_extractor_geograpy3(input):

    # === Below code checks (and downloads if needed) =========== #
    # === text packages needed for the extractor ================ #
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    # =========================================================== #

    result = list()      

    countries_list = list()
    regions_list   = list()
    cities_list    = list()
    other_list     = list()

    if type(input) == str:
        input = [input]

    places = None

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        places = geograpy.get_geoPlace_context(text = string)

        countries_list.extend(places.countries)
        regions_list.  extend(places.regions)
        cities_list.   extend(places.cities)
        other_list.    extend(places.other)

    countries_list = list(dict.fromkeys(countries_list))
    regions_list   = list(dict.fromkeys(regions_list))
    cities_list    = list(dict.fromkeys(cities_list))
    other_list     = list(dict.fromkeys(other_list))

    address_locality_list = list()
    unconvertable_list    = list()

    # Convert country to ISO
    for name in countries_list:
        c_name = country_converter.convert(names = name, to='ISO2')

        if c_name != const.COUNTRY_CONVERTED_FAIL:
            address_locality_list.append(c_name)
        
        else:
            unconvertable_list.append(name)

    # Convert subdivisions/regions to ISO
    divs_names_to_iso_dict = dict()
    for div in pycountry.subdivisions:
        divs_names_to_iso_dict[div.name] = div.code  

    for name in regions_list:
        if name in divs_names_to_iso_dict:
            address_locality_list.append(divs_names_to_iso_dict[name])
        
        else:
            unconvertable_list.append(name)

    converted_list = cities_list + address_locality_list

    unconvertable_list.extend(other_list)

    unconvertable_list = list(dict.fromkeys(unconvertable_list))
    converted_list     = list(dict.fromkeys(converted_list))


    schema_to_data_list = {
                               const.NAME_SCHEMA : unconvertable_list,
                               const.GEOGRAPHY_SCHEMA : converted_list,
                          }

    current_date_time = datetime.datetime.now()

    for schema, data_list in schema_to_data_list.items():
        for data in data_list:            
    
            result.append(
                {
                    const.TYPE          : const.GEOGRAPHY_SCHEMA_TYPE,
                    schema              : data,
                    const.KRK_EXTRACTOR : const.GEOGRAPHY_EXTRACTOR_NAME,
                    const.KRK_DATE      : str(current_date_time)
                }
            )

    return result

@allow_only_string
def title_extractor(input):
    result = list()  

    titles_list = list()

    if type(input) == str:
        input = [input]    

    for in_str in input:

        if type(in_str) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        finder=FinderAcora()
        matches = finder.findall(in_str)

        titles_list.extend(matches)

    titles_list = list(dict.fromkeys(titles_list))

    current_date_time = datetime.datetime.now()

    for tittle_rec in titles_list:
        
        result.append(
            {
                const.TYPE              : const.JOB_TITTLE_SCHEMA_TYPE,
                const.JOB_TITTLE_SCHEMA : tittle_rec.match,
                const.KRK_EXTRACTOR     : const.JOB_TITTLE_EXTRACTOR_NAME,
                const.KRK_DATE          : str(current_date_time)
            }
        )

    return result


@allow_only_string
def qty_extractor_quantulum3(input):
    result = list()  

    q_list = list()

    if type(input) == str:
        input = [input]

    for string in input:

        if type(string) != str: 
            logging.warning('Non string received as an input. Skipping...')
            continue

        q_list.extend(parser.parse(string))

    current_date_time = datetime.datetime.now()

    for quant in q_list:

        result.append(
            {
                const.TYPE            : const.QUANTITY_SCHEMA_TYPE,
                const.QUANTITY_SCHEMA : f'{str(quant.value)} {str(quant.unit)}',
                const.KRK_EXTRACTOR   : const.QUANTITY_EXTRACTOR_NAME,
                const.KRK_DATE        : str(current_date_time)
            }
        )

    return result
