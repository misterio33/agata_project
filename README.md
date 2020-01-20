# COST_Germany

# Setting up Virtual Environment

1. Go to folder where is skeleton project folder located

2. Open terminal at this location

3. To make new virtual environment print the followint at the terminal:
	
	`virtualenv venv` this will create venv folder

4. To activate virtual environment print the followint at the terminal:

	`source venv/bin/activate` this will activate virtual environment, you must see (venv) at your promt 

5. To install all needed libraries print the followint at the terminal:

	`pip install -r requirements.txt` this will install every libriary specified at the requirement.txt document

6. After installing libraries go to skeleton project folder and run skeleton project file

7. To stop wirtual environment print at terminal 

	`deactivate`

# Running agata programm

1. Run virtual environment

2. Go to agata.py folder 

	`cd agata_project_folder/`
	
3. Run folloving command to see details

	`python agata.py --help`

# Running docker-compose.yml file

1. Check the validity of file by command

    `docker-compose config`

2. Run docker-compose.yml file by command

   `docker-compose up -d`

3. Check runnig containers

   `docrker-compose ps`

4. Bring down application by command

   `docker-compose down`
