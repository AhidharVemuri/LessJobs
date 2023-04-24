# LessJobs
Code files and the README to setup the application locally on your system - Open the Docx file for visual aids for the setup.

Please follow the below instructions to install and run this application in your system.
1.	Download and install the latest version of Python. The version should be at least higher than 3.6.
2.	Download and install MySQL workbench.
3.	Select and run the SQL file labelled lessjob_dbschema.sql on your MySQL workbench after setting up your username and password for MySQL workbench connection. This will create the DB for the file with the sample data entered.
4.	Download and install Visual Studio 2022 on your system.
5.	Place the folder labelled as Flask in a drive of your choice.
6.	After installation on the Visual Studio homepage click the button labelled “Open a local folder”. This will open a prompt window which you can use to select the folder labelled Flask from step 4.
7.	Use the CTRL+` keyboard shortcut with the backtick character to show the terminal.
8.	Install the following package dependencies required to run the application,
    
    o	virtualenv – Use command pip install virtualenv in your command line terminal. Once installed run the command .\env\Scripts\activate.bat for windows OR  source env/bin/activate on Macbook or Macintosh. Upon doing this you should be able to see the virtual that the name env appears in before your directory path.
 
    o	flask and flask-sqlalchemy – Use command pip install flask flask-sqlalchemy 
    
    o	sklearn – Use command pip install -U scikit-learn
    
    o	pandas, numpy – Use the command pip install pandas numpy
9.	Environment Variables are needed for the application to run. Please follow the instructions on these links to setup environment variables on Windows or Mac,
    
    o	For Windows – https://phoenixnap.com/kb/windows-set-environment-variable
    
    o	For Mac - https://phoenixnap.com/kb/set-environment-variable-mac
10.	Setup two environment variables labelled MYSQL_username and MYSQL_password and in those variables store your MySQL workbench username and password respectively.
11.	At this point all the dependencies for the project have been installed. You may now run the project using the command python app.py in the developer command terminal.
12.	After this go to a browser of your choice and type in http://localhost:5000/first_page
13.	You should be able to see the Welcome Page for LessJobs website.
 

