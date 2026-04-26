To run this install:

1. To create a virtual enviornment (on mac), run

- python3 -m venv venv
- source venv/bin/activate

2. Requests, (INSERT MORE DEPENDENCIES HERE)
3. python(3) main.py

Idea: we are building a vocabulary memorization app, where the user inputs a list of words they want to memorize, and we display their definitions one by one and have the user guess it wordle style. They will get 5 attempts to guess the word through its definition. An alternative to this is to study one of our preselected lists:

- Common medical vocabulary
- Common social studies vocabulary

How we are going to build this:

1. Build example custom list. - UMAR
2. Build the lists for common medical vocabulary (goal: be able to describe better when you go to the doctor, so like joints and basic anatomy is good here) - MOHAMMAD
3. Build the list for common social studies vocabulary (government branches and stuff) - DIJON
4. Build the data loader for the user generated lists (from a csv file of just words) - MOHAMMAD
   Note all of these lists should be words, not definitions. When we first study this word, we fetch the definition from the dictionary API, later we can cache the definitions within the files.
5. Build the function for fetching the definition of all the words one by one and storing them in an array: [Word: definition] - UMAR
6. Build the word checking function. - DIJON
7. Build the quizzing interface in terminal - MOHAMMAD
   When the user hits play, display 3 options: 1=custom, 2=medical, 3=social studies
   On choosing a number: display something like: ready to start? Lets do it or something motivational
   Display something like Question 1: [DEFINITION]: \_ \_ \_ \_ \_ (dashes indicating the length of the word)
   When the user submits a word, check which letters are correct and their indexes. Then in terminal display the correct letters in green if their index is correct, yellow if letter correct and index wrong, and nothing if letter and index are wrong.
   Repeat till word found or fail.
   Repeat with each word in the list, enter QUIT to quit.
8. Build caching for the definitions so that we don’t hit the API every time, can store in the csv file. - UMAR
9. Build player vs player: the adjustment here is that we ask for player number in the terminal before everything and increment a point every time they get an answer correct. - DIJON
10. Convert Backend to Django - UMAR

To run the Django Server:

1. Install dependencies by running pip install django djangorestframework
2. Run python manage.py runserver

LOG:

1. Commits 1,2,3: Umar, 2 hours - I brainstormed features for the app, assigned tasks to everyone, and made a timeline for completion. Also added a custom list csv file for testing.
2. Commits 4,5: Dijon, 35 minutes - Compiled a list of social studies vocabulary in social_studies_list.csv
3. Commits 6-9: Mohammad, 45 minutes - Compiled a list of medical vocabulary in medical_list.csv.
4. Commits 10-12: Dijon, 5 minutes - I saw and fixed the time for Readme, and saw that the list definition should be blank, and added some more words
5. Commits 13-14: Umar: 50 minutes - Found and integrated the definitions api within the get definitions function. Added a gitignore for the venv and .idea, and added documentation for creating a virtual environment.
6. Commits 15-16: Mohammad, 2½ hours - Made a csv loader function in loader.py, tested our dictionary api integration, verified some error handling within csv files, and corrected issues with the medical list.
7. Commits 17-18: DiJon, 1 1/2 hours - Made word checker, also made a basic display so i could check to see if working properly. Saw that keeps asking for guesses even after getting word will fix later.
8. Commits 19-20: Umar 2 hours - Learned about and implemented caching. Fixed bugs that came from caching related changes. Tested the caching in game. Note: the api will only take 29 requests at a time before it blocks us from sending. Might want to cut down our lists.
9. Commits 21-22: Mohammad 4 hours - Built a menu interface incorporating list options, definition display, game logic, attempt plus score tracking, error handling, and also explored the colorama library.
10. Commits 23-24: DiJon 2 1/2 hours - Built mode menu, made PvP mode, made PvP have personal quit so won't show total correct could add if requested. Note: I saw that the definitions for social studies had the wrong definitions attached will make definitions for them again.
11. Commits 24-26: Umar 30 minutes - updated readme, created basic django scaffolding. Referenced: https://www.youtube.com/watch?v=NoLF7Dlu5mc
12. Commits 26-28: Umar 3 Hours - learned and implemented 3 Django REST API endpoints for possible frontend. Tested using Postman 2.
13. Commits 29-31: DiJon 2 hours - learned and implemented a function to test if real words are used, for the now it only checks to see if its an english word. Also fixed the social studies definitions.
