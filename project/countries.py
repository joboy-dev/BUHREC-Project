from country_list import countries_for_language

countries = countries_for_language('en')  # Get countries in English

countries = [country for country in countries]

print(countries)