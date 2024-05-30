from resume.api import get_from_url, get_from_dictionaries, get_currency, get_specialization, get_metro_stations

COUNTRY_CHOICES = get_from_url("/areas/countries")

# Выбор пола
GENDER_CHOICES = get_from_dictionaries("gender")

# Выбор вида связи
TYPES_OF_COMMUNICATION_CHOICES = get_from_dictionaries("preferred_contact_type")

# Выбор уровня образования
EDUCATION_LEVEL_CHOICES = get_from_dictionaries("education_level")

# Выбор возможности переезда
POSSIBILITY_OF_TRANSFER_CHOICES = get_from_dictionaries("relocation_type")

# Выбор готовности к командировкам
BUSINESS_TRIPS_CHOICES = get_from_dictionaries("business_trip_readiness")

# Выбор желаемого время в пути до работы
DESIRED_TIME_CHOICES = get_from_dictionaries("travel_time")

# Занятость
BUSYNESS_CHOICES = get_from_dictionaries("employment")

# Языки
LANGUAGE_CHOICES = get_from_url("/languages")

# Уровень
PROFICIENCY_LEVEL_CHOICES = get_from_dictionaries("language_level")

# Выбор валюты для ЗП
CURRENCY_CHOICES = get_currency()

# Выбор специализации
SPECIALIZATION_CHOICES = get_specialization()

# График работы
WORK_TIME_CHOICES = get_from_dictionaries("schedule")

# Выбор станции метро
STATION_METRO_CHOICES = get_metro_stations(1)

# Выбор города
CITY_CHOICES = (
    ('1', "Москва"),
    ('2', "Санкт-Петербург"),
)

# Выбор категории прав
DRIVING_LISENSE_CHOICES = (
    ('Не указано', "Не указано"),
    ('A', "A"),
    ('B', "B"),
    ('C', "C"),
    ('D', "D"),
    ('E', "E"),
    ('BE', "BE"),
    ('CE', "CE"),
    ('DE', "DE"),
    ('Tm', "Tm"),
    ('Tb', "Tb"),
)

# Выбор локали резюме ???
LOCALE_RESUME_CHOICES = (
    ('ru', "ru"),
    ('en', "en"),
)

