JOB SEARCH PORTAL
https://www.projectpro.io/article/web-scraping-projects-ideas/475

We already have so many websites like LinkedIn, Indeed, Glassdoor, etc., that host so many job opportunities every day. 
But have you ever noticed that usually, they all contain different jobs? So, how about we scrap the data from these websites 
to build a collective job search portal?

For this project, you should scrap popular job portal websites and obtain information like the date of the job posting, salary details, 
job industry, company name, etc. You can then store and present this information on your website.

For this project implementation, you can use Scrapy, a library in the Python programming language that allows its programmers to scrape 
data from any website. The exciting feature of Scrapy is that it offers an asynchronous networking library so you can move on to the 
following next set of tasks before they are complete




-----------------------------------------------------------------------------------------------------------------------------------------------
>>>>>>  SPIDER JobPortalEE
Se construyó el primer spider para bajar información de la página de ElEmpleo.com
Al ejecutar el spider se deben ingresar 3 parámetros: 
	- jobSearched: trabajo que se quiere buscar
	- MaxResults: cantidad máxima de resultados que se quieren obtener
	- keyWords: Palabras clave para filtrar los títulos, separadas por coma. 

--->>>  scrapy crawl JobPortalEE -a jobSearched=datos -a MaxResults=30 -a keyWords=analista,sql,bi

-----------------------------------------------------------------------------------------------------------------------------------------------
>>>>>>  SPIDER JobPortalCT
Se construyó el segundo spider para bajar información de la página de Computrabajo
Al ejecutar el spider se deben ingresar 3 parámetros: 
	- jobSearched: trabajo que se quiere buscar
	- MaxResults: cantidad máxima de resultados que se quieren obtener
	- keyWords: Palabras clave para filtrar los títulos, separadas por coma. 

--->>>  scrapy crawl JobPortalCT -a jobSearched=datos -a MaxResults=30 -a keyWords=analista,sql,bi

