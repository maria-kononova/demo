from resume.api import get_from_url, get_from_dictionaries, get_currency, get_specialization

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

# Выбор города
CITY_CHOICES = (
    (1, "Санкт-Петербург"),
    (2, "Москва"),
)

# Выбор станции метро
STATION_METRO_CHOICES = (
    (1, "Сенная"),
    (2, "Адмиралтейская"),
    (3, "Площадь Восстания"),
    (4, "Невский проспект"),
)

# Выбор категории прав
DRIVING_LISENSE_CHOICES = (
    (1, "Не указано"),
    (2, "A"),
    (3, "B"),
    (4, "C"),
    (5, "D"),
    (6, "E"),
    (7, "BE"),
    (8, "CE"),
    (9, "DE"),
    (10, "Tm"),
    (11, "Tb"),
)

# Выбор локали резюме ???
LOCALE_RESUME_CHOICES = (
    (1, "ru"),
    (2, "en"),
)

