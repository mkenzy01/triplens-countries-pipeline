select
    uuid,
    country_name,
    official_name,
    alpha_2,
    alpha_3,

    capital,
    region,
    subregion,
    continents,

    population,
    area_km2,
    latitude,
    longitude,
    landlocked,

    currencies,
    languages,
    timezones,
    borders,
    calling_codes,
    tlds,

    array_to_string(
        transform(currencies, x -> x:name::string),
        ', '
    ) as currency_text,

    array_to_string(
        transform(languages, x -> x:name::string),
        ', '
    ) as language_text,

    array_to_string(
        timezones,
        ', '
    ) as timezone_text,

    array_to_string(
        borders,
        ', '
    ) as borders_text,

    driving_side,
    government_type,

    is_sovereign,
    is_dependency,
    is_disputed,
    is_un_member

from {{ source('silver', 'countries') }}