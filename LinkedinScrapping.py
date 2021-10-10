# importing libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
# importing libraries to plot the wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# Variables
# Linkedin ID and PASSWORD
email = "cxxxxxxxx01@xxxxxxx.com"
password = "xxxxxxx"

# Write here the job position and local for search
#position = "designsync"
#position = "synchronicity"
position = "perforce"

local = "Worldwide"

# example below:
## position = "data scientist"
## local = "brazil"

# formating to linkedin model
position = position.replace(' ', "%20")

options = webdriver.ChromeOptions()
options.add_argument('lang=en')
# options.add_argument('--lang=en') <- Tried this option as well
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

# Open browser
driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)
# Maximizing browser window to avoid hidden elements
driver.set_window_size(2560, 1920)
driver.maximize_window()

# Opening linkedin website
driver.get('https://www.linkedin.com/login')
# waiting load
time.sleep(2)

# Search for login and password inputs, send credentions
driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_id('password').send_keys(Keys.RETURN)

# Opening jobs webpage
#driver.get( f"https://www.linkedin.com/jobs/search/?currentJobId=2662929045&geoId=106057199&keywords={position}&location={local}")
#driver.get( f"https://www.linkedin.com/jobs/search/?f_l=7&geoId=92000000&keywords={position}&location={local}&sortBy=DD")
driver.get(f"https://www.linkedin.com/jobs/search/?f_I=7&geoId=92000000&keywords={position}&location={local}e&sortBy=DD")
# waiting load
time.sleep(3)


# creating a list where the descriptions will be stored
disc_list = []

try:
    pages = driver.find_element_by_xpath(f'//button[@aria-label="Page 1"]')
    pages = driver.find_elements_by_xpath(f'//button[starts-with(@aria-label, "Page ")]')
    max_page = int(pages[-1].text)
except NoSuchElementException:
    # Only one page
    max_page = 1

# each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
# with this knowledge I created a loop that will check how many jobs the page is listing
# linkedin show us 40 jobs pages, then the line below will repeat 40 times
for i in range(1, max_page+1):
    # click button to change the job list
    if i > 1:   # No page element if there is only one page, so skip the 1 page click to avoid error
        driver.find_element_by_xpath(f'//button[@aria-label="Page {i}"]').click()
    # each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
    jobs_list = driver.find_element_by_class_name(
        'jobs-search-results__list')  # here we create a list with jobs
    jobs = jobs_list.find_elements_by_class_name(
        'jobs-search-results__list-item')  # here we select each job to count

    job_rail = driver.find_element_by_class_name('jobs-search__left-rail')

    job_rail.send_keys(Keys.END)
    job_rail.send_keys(Keys.PAGE_DOWN)

    # waiting load
    time.sleep(1)

    # Scroll down to bottom to load all jobs on the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    # the loop below is for the algorithm to click exactly on the number of jobs that is showing in list
    # in order to avoid errors that will stop the automation
    #for job in range(1, len(jobs)+1):
    for job in jobs:
        ## # job click
        ## driver.find_element_by_xpath(
        ##     #f'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div/div[1]/div[2]/div[1]/a').click()
        ##     f'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[1]/div/div/div[1]').click()
        ## # waiting load
        ## time.sleep(1)
        ## # select job description
        ## job_desc = driver.find_element_by_class_name('jobs-search__right-rail')
        ## # get text
        ## soup = BeautifulSoup(job_desc.get_attribute(
        ##     'outerHTML'), 'html.parser')
        ## # add text to list
        ## disc_list.append(soup.text)


        #time.sleep(1)
        job_summary = job.text.split('\n')
        print(job)
        n=1
        while job_summary == [''] and n < 10:
            #time.sleep(1)
            job_summary = job.text.split('\n')
            n += 1
        disc_list.append({'Vacancy':job_summary[0], 'Company': job_summary[1], 'Location': job_summary[2]})

# Creating a Dataframe with list
df = pd.DataFrame(disc_list)

## # deleting useless words
## df = df.replace(['\n',
##                  '^.*?Expect',
##                  '^.*?Qualifications',
##                  '^.*?Required',
##                  '^.*?expected',
##                  '^.*?Responsibilities',
##                  '^.*?Requisitos',
##                  '^.*?Requirements',
##                  '^.*?Qualificações',
##                  '^.*?QualificationsRequired1',
##                  '^.*?você deve ter:',
##                  '^.*?experiência',
##                  '^.*?você:',
##                  '^.*?Desejável',
##                  '^.*?great',
##                  '^.*?Looking For',
##                  '^.*?ll Need',
##                  '^.*?Conhecimento',
##                  '^.*?se:',
##                  '^.*?habilidades',
##                  '^.*?se:',
##                  '^.*?REQUISITOS'
##                  ], '', regex=True)
## 
## 
## # setup wordcloud
## stopwords = set(STOPWORDS)
## # selecting useless words
## badwords = {'gender', 'experience', 'application', 'Apply', 'salary', 'todos', 'os', 'company', 'identity', 'sexual', 'orientation',
##             'de', 'orientação', 'sexual', 'gênero', 'committed', 'toda', 'client', 'conhecimento',
##             'world', 'year', 'save', 'São', 'Paulo', 'information', 'e', 'orientação', 'sexual', 'equal', 'oppotunity', 'ambiente', 'will',
##             'Experiência', 'national origin', 'todas', 'work', 'de', 'da', 'years', 'pessoa', 'clients', 'Plano', 'creating',
##             'employer', 'saúde', 'em', 'working', 'pessoas', 'mais', 'data', 'people', 'dia', 'one', 'knowledges', 'plataforma',
##             'ou', 'benefício', 'para', 'software', 'opportunity', 'tecnologia', 'você', 'mais', 'solution', 'national', 'origin',
##             'trabalhar', 'option', 'negócio', 'empresa', 'o', 'sicence', 'team', 'é', 'veteran', 'status', 'etc', 'raça', 'cor', 'belive',
##             'nossa', 'uma', 'como', 'Scientist', 'ferramenta', 'projeto', 'que', 'job', 'benefícios', 'knowledge', 'toll', 's', 'modelo',
##             'desconto', 'cultura', 'serviço', 'time', 'se', 'solutions', 'mercado', 'das', 'somos', 'problema', 'mundo', 'race', 'color',
##             'vaga', 'pelo', 'ser', 'show', 'Seguro', 'Se', 'um', 'Um', 'tool', 'regard', 'without', 'make', 'ao', 'técnica', 'life',
##             'interested', 'diversidade', 'proud', 'ability', 'sobre', 'options', 'using', 'área', 'nosso', 'na', 'seu', 'product', 'produto',
##             'building', 'skill', 'model', 'religion', 'Share', 'receive', 'consideration', 'Aqui', 'vida', 'ferramentas', 'Vale', 'Refeição',
##             'Strong', 'Pay', 'range', 'available', 'part', 'trabalho', 'Alimentação', 'employment', 'qualified', 'applicants', 'gympass',
##             'está', 'comprometida', 'forma', 'Transporte', 'Yes', 'gente', 'melhor', 'lugar', 'believe', 'moment', 'próximo', 'deasafio',
##             'dos', 'oportunidade', 'idade', 'new', 'Try', 'Premium', 'deficiência', 'sempre', 'criar', 'employee', 'problemas', 'unavailable',
##             'Brasil', 'dado', 'hiring', 'trends', 'equipe', 'recent', 'temos', 'build', 'career', 'nós', 'diferencial', 'ma',
##             'total', 'oferecemos', 'contato', 'tem', 'não', 'free', 'Full'}
## 
## # deleting the useless words on plot
## stopwords.update(badwords)
## 
## # plot parameters
## wordcloud = WordCloud(background_color='black',
##                       stopwords=stopwords,
##                       max_words=100,
##                       max_font_size=50,
##                       random_state=42).generate("".join(df[0]))
## 
## # Plot
## print(wordcloud)
## plt.figure(figsize=(10, 5))
## fig = plt.figure(1)
## plt.imshow(wordcloud)
## plt.axis('off')
## plt.show()

# exporting our dataframe to a csv file
df.to_csv(f'{local}_{position}.csv', sep=';', index=False)
