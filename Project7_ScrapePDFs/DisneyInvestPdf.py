# Equity Research involves thorough analysis and understanding of a company’s financial documents like balance sheet, profit and loss statement, 
# cash flow statements, etc., of the past few years. That helps portfolio managers to be sure of the investments in a company of their interest.

# Most companies have an Investor Relation section on their website with their annual financial statements. For this project, you can refer to 
# Walt Disney’s Investor Relation webpage and scrape the PDFs available to understand how the company is evolving financially.

# For this project, we recommend the popular package of Python’s programming language, Beautiful Soup. Additionally, since you must extract 
# content from the PDFs, you will have to use another package, PyPDF2, that has the PdfFileReader class.

# pdf descargado de: https://thewaltdisneycompany.com/investor-relations/


import pdfplumber
import pandas as pd


# leemos el PDF
pdf = pdfplumber.open('2020-Annual-Report.pdf')


# extraemos el texto de una página
texto = pdf.pages[33].extract_text(x_tolerance=3, y_tolerance=3, layout=False, x_density=7.25, y_density=13)


# pdfPlumber no reconoce las tablas del archivo como tablas (extract_tables no funciona). 
# Utilizo la alternativa de extraer el rango de líneas que conforman la tabla y las muestro en pantalla en el formato requerido.


table1 = []
for i in range(4,11):
    listDit = []
    for word in texto.split('\n')[i].split(' '):
        listDit.append(word)
    
    table1.append(listDit)

print('tabla PDF 1, página 33')
print(pd.DataFrame(table1[1::], columns=table1[0]))
print('\n', '\n')



# pdf 2  -- Probamos nuevamente con un PDF en donde la tabla esté adecuadamente definida
# descargado de: https://www.ciriondo.com/PDFs/17%20Tablas%20de%20conversion/Tablas%20de%20Conversion.pdf


pdf2 = pdfplumber.open('TablasConversion.pdf')
table2 = pdf2.pages[0].extract_tables()[0]

print('tabla PDF 2, página 1')
print(pd.DataFrame(table2[1::], columns=table2[0]))  ## Sí imprime cada tabla del archivo










