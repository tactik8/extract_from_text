from extractors import \
    email_extractor_regex, \
    url_extractor_ioc_finder,\
    url_extractor_regex,\
    phone_extractor_ioc_finder,\
    qty_extractor_quantulum3,\
    title_extractor,\
    geo_extractor_geograpy3


def main(request = None):

    if request:

        text = ''

    else:

        text = '''
            This is a test that contains several elements like emails john@abcce.com and smith@xyz.com, some urls such as https://www.abc.com some phone numbers such as (514) 222-3345, some geographies like Quebec, Canada or Oslo in Norway, and some quantities like 3 liters or five dollars. 
            '''


    extracted = []

    extracted += email_extractor_regex(text)

    extracted += url_extractor_ioc_finder(text)

    extracted += url_extractor_regex(text)

    extracted += phone_extractor_ioc_finder(text)

    extracted += qty_extractor_quantulum3(text)

    extracted += title_extractor(text)

    extracted += geo_extractor_geograpy3(text)

    for i in extracted:
        print('-')
        print(' ---------- ')
        print(i)


main()