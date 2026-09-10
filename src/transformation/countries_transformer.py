def transform_country(country):
    names = country.get("names") or {}
    codes = country.get("codes") or {}
    classification = country.get("classification") or {}
    flag = country.get("flag") or {}
    cars = country.get("cars") or {}

    capitals = country.get("capitals") or []
    capital = capitals[0] if capitals else {}

    capital_coordinates = capital.get("coordinates") or {}

    area = country.get("area") or {}
    coordinates = country.get("coordinates") or {}

    continents = country.get("continents") or []
    timezones = country.get("timezones") or []
    borders = country.get("borders") or []
    calling_codes = country.get("calling_codes") or []
    tlds = country.get("tlds") or []

    return {
        "uuid": country.get("uuid"),

        "country_name": names.get("common"),
        "official_name": names.get("official"),

        "alpha_2": codes.get("alpha_2"),
        "alpha_3": codes.get("alpha_3"),

        "capital": capital.get("name"),
        "capital_latitude": capital_coordinates.get("lat"),
        "capital_longitude": capital_coordinates.get("lng"),

        "region": country.get("region"),
        "subregion": country.get("subregion"),

        "continents": continents,

        "population": country.get("population"),

        "area_km2": area.get("kilometers"),
        "area_miles2": area.get("miles"),

        "latitude": coordinates.get("lat"),
        "longitude": coordinates.get("lng"),

        "landlocked": country.get("landlocked"),

        "currencies": country.get("currencies") or [],
        "languages": country.get("languages") or [],

        "timezones": timezones,
        "borders": borders,

        "calling_codes": calling_codes,
        "tlds": tlds,

        "flag_emoji": flag.get("emoji"),
        "flag_png": flag.get("url_png"),
        "flag_svg": flag.get("url_svg"),

        "driving_side": cars.get("driving_side"),

        "government_type": country.get("government_type"),

        "is_sovereign": classification.get("sovereign"),
        "is_dependency": classification.get("dependency"),
        "is_disputed": classification.get("disputed"),
        "is_un_member": classification.get("un_member"),
    }


def transform_countries(countries):
    return [
        transform_country(country)
        for country in countries
    ]