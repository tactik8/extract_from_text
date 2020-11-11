# === Validation result codes =============================================== #
RC_NONE_INPUT              = 0
RC_WRONG_TYPE_INPUT        = 1
RC_VALID_INPUT             = 2
RC_PARTLY_VALID_LIST_INPUT = 3
RC_WRONG_LIST_TYPES_INPUT  = 4
RC_EMPTY_LIST_INPUT        = 5

RC_TO_TEXT_REASON =\
{
    RC_NONE_INPUT              : 'None value received as input.',
    RC_WRONG_TYPE_INPUT        : 'Wrong input type received.',
    RC_VALID_INPUT             : 'Valid input received',
    RC_PARTLY_VALID_LIST_INPUT : 'List with some valid inputs received',
    RC_WRONG_LIST_TYPES_INPUT  : 'List without strings received.',
    RC_EMPTY_LIST_INPUT        : 'Empty list received.',
}


VALID_RC_CODES = [RC_VALID_INPUT, RC_PARTLY_VALID_LIST_INPUT]
# =========================================================================== #

EMAIL_PATTERN = r"[\w\.-]+@[\w\.-]+\.\w+"

URL_PATTERN   = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"

COUNTRY_CONVERTED_FAIL = 'not found'


# === Output constants ====================================================== #
# === Common === #
TYPE          = '@type'
KRK_EXTRACTOR = 'kraken:extractor'
KRK_DATE      = 'kraken:extracteddate'

CONTACT_POINT_SCHEMA_TYPE = 'schema:contactpoint'
NAME_SCHEMA               = 'schema:name'
# ============== #

# === Email extractor === #
EMAIL_EXTRACTOR_NAME = 'extract_from_text-email_extractor_regex'
EMAIL_SCHEMA_TYPE    = CONTACT_POINT_SCHEMA_TYPE
EMAIL_SCHEMA         = 'schema:email'
# ======================= #

# === URL Extractors === #
URL_IOC_EXTRACTOR_NAME = 'extract_from_text-url_extractor_ioc_finder'
URL_RE_EXTRACTOR_NAME  = 'extract_from_text-url_extractor_regex'
URL_SCHEMA_TYPE        = 'schema:WebPage'
URL_SCHEMA             = 'schema:url'
# ====================== #

# === Phone extractor === #
PHONE_EXTRACTOR_NAME = 'extract_from_text-phone_extractor_ioc_finder'
PHONE_SCHEMA_TYPE    = CONTACT_POINT_SCHEMA_TYPE
PHONE_SCHEMA         = 'schema:telephone'
# ======================= #

# === Quantity extractor === #
QUANTITY_EXTRACTOR_NAME = 'extract_from_text-qty_extractor_quantulum3'
QUANTITY_SCHEMA_TYPE    = 'schema:quantity'
QUANTITY_SCHEMA         = 'schema:quantity'
# ========================== #

# === Job Title extractor === #
JOB_TITTLE_EXTRACTOR_NAME = 'extract_from_text-title_extractor'
JOB_TITTLE_SCHEMA_TYPE    = 'schema:jobTitle'
JOB_TITTLE_SCHEMA         = 'schema:name'
# =========================== #

# === Geography extractor === #
GEOGRAPHY_EXTRACTOR_NAME = 'extract_from_text-geo_extractor_geograpy3'
GEOGRAPHY_SCHEMA_TYPE    = 'schema:PostalAddress'
GEOGRAPHY_SCHEMA         = 'schema:addressLocality'
# =========================== #
# =========================================================================== #
