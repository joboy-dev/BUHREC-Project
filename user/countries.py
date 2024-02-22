from country_list import countries_for_language

def get_all_countries():
    all_countries = countries_for_language('en')
    countries = [country for country in all_countries]
    
    return countries