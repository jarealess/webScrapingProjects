# Using WebMD’s database, you can build a drug recommendation system. The website has authentic content for medical news and the drug 
# components of several medicines you can scrape to realize this project’s solution.

#Using Python’s web scraping framework, Scrapy, you can download the website’s content for one of the most interesting web scraping 
# with python projects.


# PAGE: https://www.webmd.com/drugs/2/alpha/l
# Page spanish: https://medlineplus.gov/spanish/druginfo/drug_Aa.html

import pandas as pd

## ---------------------------------  reading drugs information  -----------------------------------------------------------

df = pd.read_csv('DrugRecommendSystem\DrugsInformation.csv', sep=";", encoding="latin-1")


## --------------------------------- getting list of symptons ------------------------------------------------------------------

print("")
symptons = input("Ingrese síntomas, separados por coma si son más de uno: ")
symptonsList = symptons.split(',')


## --------------------------------- filtering dataframe ------------------------------------------------------------------
FilterDrugs = df.loc[df.Sintomas.str.contains(symptonsList[0], case=False, regex=True)==True]
for sympton in symptonsList:
    FilterDrugs = FilterDrugs.loc[FilterDrugs.Sintomas.str.contains(sympton, case=False, regex=True)==True]


## --------------------------------- printing -----------------------------------------------------------------------------------

if FilterDrugs.empty:
    print("""
            ---> No hay medicamentos en la base que ataquen todos los síntomas
            ---> Intente con otras palabras u otra combinación de síntomas
            
            """)
else:
    print(""" 
              Listado de medicamentos acontinuación. 
              Se recomienda ir al enlace para consultar contraindicaciones.

            """)
    print(FilterDrugs.loc[:, ['Medicamento', 'Enlace']].to_string(index=False))  




