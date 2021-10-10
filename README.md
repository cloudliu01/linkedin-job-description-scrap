# linkedin-job-description-scrap

This project is part of my study about data science, in this project we can select a position job, the script will get the job description on linkedin pages, and will plot a word cloud with most relevants requirements about the previous position selected.

the datais about how the script runs is documented in:
link.medium.com/RqNR7YocWib 

If you have any corrections, suggestions, or information about this topic, feel free to contact me:
saulodetp@gmail.com


#Lizhuang Liu on Oct10,2021
1, updated to work with the latest Linkedin webpage
2, only save index info ( no detail )
3, while scraping the page ( running the program, user needs to actively scroll the 'jobs-search__left_rail' widget; otherwise the program will go into section below which will sometimes cause the whole program fail ( workaround is to set a breakpoint at line
   job_summary = job.text.split('\n')