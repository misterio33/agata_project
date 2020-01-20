# COST_Germany

# Setting up Virtual Environment

1. Open terminal

2. Go to project root folder 
	
	`cd agata_project/` this command  will move you to root project folder

3. To make new virtual environment print the following at the terminal:
	
	`virtualenv venv` this command will create venv folder

4. To activate virtual environment print the followint at the terminal:

	`source venv/bin/activate` this command will activate virtual environment, you must see (venv) at your promt 

5. To install all needed libraries via printing the followint command:

	`pip install -r requirements.txt` this command will install every libriary specified at the requirement.txt document

6. After installing libraries go to agata_project_folder and run help for agata.py file

	`cd agata_project_folder/` this will move you to program folder
	
	`python agata.py --help` this will show you existing comands 

7. To stop wirtual environment print at terminal 

	`deactivate`

# Running agata programm

1. Run virtual environment

2. Check libraries at virtual environment using command:

	`pip install -r requirements.txt`

3. Go to agata.py folder 

	`cd agata_project_folder/`
	
4. Run folloving command to see details

	`python agata.py --help`
	
5. To run dicom to png converter use next command:

	`python agata.py convert --dicompath /path/to/dicom --outputpath /path/output/folder`
	
	Do not forget to put '/' in the beginning of paths
	
6. Example of running converter:
	
	`python agata.py convert --dicompath /home/pasha/DICOM_TEST --outputpath /home/pasha/PNG_TEST`

# Running docker-compose.yml file

1. Check the validity of file by command

    `docker-compose config`

2. Run docker-compose.yml file by command

   `docker-compose up -d`

3. Check runnig containers

   `docrker-compose ps`

4. Bring down application by command

   `docker-compose down`
