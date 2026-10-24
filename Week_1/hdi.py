''' Program for calculating HDI '''
from math import log, cbrt

# Health
MIN_EXPECT = 20
MAX_EXPECT = 85

# Education
MAX_SCHOOL_YEARS = 18
MAX_MEAN_SCHOOL = 15

# GNI
MIN_GNI = 100
MAX_GNI = 75000


country = input("Enter name of your country: ")

life_expect = float(input(f'Enter life expentancy in {country}: '))

# Education
school_years = float(input(f'Enter how much schooling years in {country}: '))
mean_school_years = float(input(f'Enter mean of schooling years in {country}: '))

gni_value = float(input(f'Enter GNI per capita in {country}: '))


health_index = (life_expect - MIN_EXPECT)/(MAX_EXPECT - MIN_EXPECT)

# Education
expect_years_index = school_years / MAX_SCHOOL_YEARS
mean_years_index = mean_school_years / MAX_MEAN_SCHOOL
education_index = (expect_years_index + mean_years_index) / 2

gni_index = (log(gni_value)- log(MIN_GNI)) / (log(MAX_GNI) - log(MIN_GNI))


worst_index = min(health_index, education_index, gni_index)

hdi_index = cbrt(health_index * education_index * gni_index)


print(f'Life expectancy index for {country} is {health_index:.4f}.')
print(f'Education index for {country} is {education_index:.4f}.')
print(f'GNI index for {country} is {gni_index:.4f}.')
print(f'HDI for {country} is {hdi_index:.3f}.')
print(f'HDI for {country} is high: {0.7<=hdi_index}.')
print(f'The worst index for {country} is {worst_index:.4f}.')
