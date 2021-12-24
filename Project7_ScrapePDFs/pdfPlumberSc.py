

# library: https://pypi.org/project/pdfplumber/
import pdfplumber
import pandas as pd


pdf = pdfplumber.open('pdftest.pdf')

# tables
table1 = pdf.pages[0].extract_tables()[0]
table2 = pdf.pages[0].extract_tables()[1]
table3 = pdf.pages[1].extract_tables()[0]

# dataframes
df1 = pd.DataFrame(table1[1::], columns=table1[0])
df2 = pd.DataFrame(table2[1::], columns=table2[0])
df3 = pd.DataFrame(table3[1::], columns=table3[0])

# imprimimos
print('table 1, page 1 \n', df1)
print('')
print('table 2, page 1 \n', df2)
print('')
print('table 1, page 2 \n', df3)
print('')

## Propiedades
print('Propiedades')
print('# Página:', pdf.pages[1].page_number)
print('Ancho página:', pdf.pages[1].width)
print('Alto página:', pdf.pages[1].height)
print('Líneas:', pdf.pages[1].lines)
## print('# Objetos:', pdf.pages[1].objects)
print('# Imágenes:', pdf.pages[1].images)
print('')

# Métodos
# words = pdf.pages[1].extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, horizontal_ltr=True, vertical_ttb=True, extra_attrs=[])
# for dicto in words:
#     print(dicto['text'])

texto = pdf.pages[1].extract_text(x_tolerance=3, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
print(texto)













