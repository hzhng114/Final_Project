To run the data collection code:
1. Download the whole repo into a folder.
2. Keep the chromedriver.exe file on the same folder and don't delete it.
3. Run the python file named "Final_Project_Data_Collection.py" on the file's directory
(run 'cd ~/Desktop/file_name' on terminal to locate the working directory), no API key required.
4. You should get three new files in the folder, which are 'game_details_list.db',
'game_list.db', and 'Steam_Top_300_Games.sqlite'. Only the last one is useful for the project.

To run the flask apps:
1. Run either Final_Project_App.py or Final_Project_App2.py on Python and make sure
to adjust working directory first.
2. If you run the first app, you will be directed to a website asking you
to choose from three sorting options and two sorting directions of the top 300 most popular steam games.
Click the submit button after you have made the decision and the result page will pop
out showing sorted steam games by chosen option and sorting direction.
3. If you run the second app, you will be directed to a website asking you
to choose from four grouping options and two sorting directions of the top 300 most popular steam games.
Click the submit button after you have made the decision and the result page will pop
out showing grouped steam games by chosen option and sorting direction.

Note: The initial data collection process will take longer without cache file.