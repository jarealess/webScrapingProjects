## EJERCICIOS PARA PRACTICAR EXPRESIONES REGULARES
# https://www.w3resource.com/python-exercises/re/
import re
from tkinter import N

# 1. Write a Python program to check that a string contains only a certain set of characters (in this case a-z, A-Z and 0-9)

def string_check(string):
    return string.isalnum()
        
print(string_check('Lio Messi 10'))
print(string_check('LioMessi10'))
print('\n-------------------------------')


# 3. Write a Python program that matches a string that has an a followed by one or more b's

def match_ab(string):
    pattern = r'([a-zA-Z]*[aA]b+[a-z]*)'
    return re.findall(pattern, string)

print(match_ab('Abreviar, en inglés, es abbreviate'))
print(match_ab('abb'))
print(match_ab('atenbao'))
print('\n-------------------------------')

# 4. Write a Python program that matches a string that has an a followed by zero or one 'b'.
def match_ab_v2(string):
    pattern = r'([a-zA-Z]*[aA]b?)'
    return re.findall(pattern, string)

print(match_ab_v2('Abreviar, en inglés, es abbreviate'))
print(match_ab_v2('abb'))
print(match_ab_v2('atenbao'))
print('\n-------------------------------')

# 5.  Write a Python program that matches a string that has an a followed by three 'b'. 

def match_ab_v3(string):
    pattern = r'([aA]b{3})'
    return re.findall(pattern, string)

print(match_ab_v3('ab'))
print(match_ab_v3('abbb'))
print(match_ab_v3('ac'))
print('\n-------------------------------')

# 7. Write a Python program to find sequences of lowercase letters joined with a underscore. 

def lower_under(string):
    pattern = r'[a-z]_'
    return re.search(pattern, string)

print(lower_under("aac_cbbbc"))
print(lower_under("aab_Abbbc"))
print(lower_under("A_abbbc"))
print('\n-------------------------------')


# 11.Write a Python program that matches a word at the end of string, with optional punctuation.

def matchEndWord(string, word):
    pattern = rf'{word}\.?$'
    return re.search(pattern, string)

print(matchEndWord("The quick brown fox jumps over the lazy dog", 'dog'))
print(matchEndWord("The quick brown fox jumps over the lazy dog.", 'dog'))
print(matchEndWord("The dog is outside", 'dog'))
print(matchEndWord("The dog is outside the box and inside there's a cat.", 'cat'))
print(matchEndWord("The dog is outside the box and inside there's a cat ", 'cat'))  ## pusimos un espacio al final
print('\n-------------------------------')

# 13. Write a Python program that matches a word containing 'z', not at the start or end of the word.

def matchInnerZ(word):
    pattern = r'[a-yA-Y]+[z]+[a-y]+'
    return re.findall(pattern, word)

print(matchInnerZ('Buzby'))
print(matchInnerZ('Buzby, Lucyz, Mazda, Zanahoria, Zzzzzz'))
print(matchInnerZ("The quick brown fox jumps over the lazy dog."))
print('\n-------------------------------')


# 14. Write a Python program to match a string that contains only upper and lowercase letters, numbers, and underscores.


def matchText(text):
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.search(pattern, text)

print(matchText("The quick brown fox jumps over the lazy dog."))
print(matchText("Python_Exercises_1"))
print('\n-------------------------------')


# 16. Write a Python program to remove leading zeros from an IP address.

def remove_zeros(Ip_address):
    pattern = r'([0]+)'
    return re.sub(pattern, '', Ip_address)

print(remove_zeros("216.08.094.196")) 
print(remove_zeros("216.002.094.000196")) 
print('\n-------------------------------')

# 18. Write a Python program to search the numbers (0-9) of length between 1 to 3 in a given string.

def checkNumbers(string):
    pattern = r'\b[0-9]{1,3}\b'
    return re.findall(pattern, string)

print(checkNumbers("Exercises number 1, 12, 13, and 345 are important"))
print(checkNumbers("Exercises number 1, 12, 13, 1059 and 345 are important"))
print('\n-------------------------------')

# 22. Write a Python program to find the occurrence and position of the substrings within a string.

def find_OccurrencePosition(string, searched_word):
    pattern = rf'{searched_word}'
    for m in re.finditer(pattern, string):
        s = m.start()
        e = m.end()
        print(f'{searched_word} encontrada en {s}:{e}') 

find_OccurrencePosition('Python exercises, PHP exercises, C# exercises', 'exercises')
print('\n-------------------------------')

# 24. Write a Python program to extract year, month and date from an url.

url1= "https://www.washingtonpost.com/news/football-insider/wp/2016/09/02/odell-beckhams-fame-rests-on-one-stupid-little-ball-josh-norman-tells-author/"

def extractDate(url):
    pattern = r'([\d]{4}\/[\d]{2}\/[\d]{2})'
    result = re.search(pattern, url)
    print(result[1])

extractDate(url1)
print('\n-------------------------------')

# 25. Write a Python program to convert a date of yyyy-mm-dd format to dd-mm-yyyy format.

def convertDate(date):
    pattern = r'(\d{4})-(\d{2})-(\d{2})'
    result = re.sub(pattern, r'\3-\2-\1', date)
    print(result)

convertDate('2022-04-29')
convertDate('1995-03-14')
print('\n-------------------------------')

# 26. Write a Python program to match if two words from a list of words starting with letter 'P'.

def P_words(list_string):
    pattern = r'[Pp][a-zA-Z]*\s[Pp][a-zA-Z]*'
    
    for string in list_string:
        m = re.match(pattern,string)
        if m is not None:
            print(string)

words = ["Python PHP", "Java JavaScript", "c c++", 'Pedro Perez']
P_words(words)
print('\n-------------------------------')


# 29. Write a Python program to separate and print the numbers and their position of a given string.

def NumberPosition(string):
    pattern = r'\b[0-9]+\b'

    for m in re.finditer(pattern, string):
        s = m.start()
        e = m.end()
        print(f'{string[s:e]} encontrado en {s}:{e}')
    
NumberPosition("Exercises number 1, 12, 13, 1059 and 345 are important")
print('\n-------------------------------')

# 31. Write a Python program to replace all occurrences of space, comma, or dot with a colon.

def replacement(string):
    pattern = r'[., ]'
    print(re.sub(pattern, ':', string))

replacement("Exercises number 1, 12, 13.")
print('\n-------------------------------')


# 32. Write a Python program to replace maximum 2 occurrences of space, comma, or dot with a colon.
text = "Exercises number 1, 12, 13."
print(re.sub(r'[ ,.]', ":", text, 2))                                             # <<<<<<<<<<<<<<<<<<<<<<--------------------
print('\n-------------------------------')


# 34. Write a Python program to find all three, four, five characters long words in a string.
text = 'The quick brown fox jumps over the laziest dog.'
print(re.findall(r'\b[a-zA-Z]{3,5}\b', text))
print('\n-------------------------------')

# 38. Write a Python program to extract values between quotation marks of a string. 
text = '"Python", "PHP", "Java"'
text2 = 'Python es el "mejor" lenguaje de "programacion"'
print(re.findall(r'"([a-zA-Z]*)"', text))
print(re.findall(r'"([a-zA-Z]*)"', text2))
print('\n-------------------------------')

# 41. Write a Python program to remove everything except alphanumeric characters from a string.
text1 = '**//Python Exercises// - 12. '

print(re.sub(r'[^a-zA-Z0-9]*', '', text1))
print('\n-------------------------------')


# 42. Write a Python program to find urls in a string.
text = '<p>Contents :</p><a href="https://w3resource.com">Python Examples</a><a href="http://github.com">Even More Examples</a>'

print(re.findall(r'https?://[a-z0-9]*\.[a-z]*', text))
print('\n-------------------------------')

# 50. Write a Python program to remove the parenthesis area in a string.

Sample_data = ["example (.com)", "w3resource", "github (.com)", "stackoverflow (.com)"]

for data in Sample_data:
    print(re.sub(r'(\(\.\w*\))', '', data))
print('\n-------------------------------')

# 51. Write a Python program to insert spaces between words starting with capital letters.

text = 'NarutoUzumaki, ToshiroHitsugaya, KakashiHatake, HiruzenSarutobi'
print(re.sub(r'([A-Z])', r' \1', text))
print('\n-------------------------------')

# 54. Write a Python program to concatenate the consecutive numbers in a given string. 
text = 'Enter at 1 20 Kearny Street. The security desk can direct you to floor 1 6.'

print(re.sub(r'(\w+) (\w*)', r'\1\2', text))
print('\n-------------------------------')
