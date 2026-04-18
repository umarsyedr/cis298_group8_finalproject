To run this install:

1. (INSERT DEPENDENCIES HERE)
2. python(3) main.py

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
10. If time build a frontend - UMAR

LOG:

1. Commits 1,2,3: Umar, 2 hours - I brainstormed features for the app, assigned tasks to everyone, and made a timeline for completion. Also added a custom list csv file for testing.
2. Commits 4,5: Dijon, 35 minutes - Compiled a list of social studies vocabulary in social_studies_list.csv
3. Commits 6: Mohammad, 45 minutes - Compiled a list of medical vocabulary in medical_list.csv.
4. Commits 10-11: Dijon, 5 minutes - I saw and fixed time for Readme, and saw that list definition should be blank and added some more words
5. 
