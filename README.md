# COST_Germany

# Setting up Virtual Environment

1. Open terminal

2. Go to project root folder 
	
	`cd  app/` this command  will move you to root project folder

3. To make new virtual environment print the following at the terminal:
	
	`virtualenv venv` this command will create venv folder

4. To activate virtual environment print the following in the terminal:

	`source venv/bin/activate` this command will activate virtual environment, you must see (venv) at your promt 

5. To install all needed libraries run the following command:

	`pip install -r requirements.txt` this command will install all libraries

6. After installing libraries go to agata_project_folder and run help for agata.py file

	`cd app/` this will move you to program folder
	
	`python agata.py --help` this will show you existing comands 

7. To stop wirtual environment print at terminal 

	`deactivate`

# Running agata program

1. Run virtual environment

2. Check libraries at virtual environment using command:

	`pip install -r requirements.txt`

3. Go to agata.py folder 

	`cd agata_project_folder/`
	
4. Run folloving command to see details

	`python agata.py --help` this command will show you all available commands
	
	`python agata.py convert --help` will show you information about convert command
	
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

   `docker-compose ps`

4. Bring down application by command

   `docker-compose down`
   
 # Running Dockerfile
 
 1. Open terminal at project root folder
 
 2. Create docker image by using command:
 
    `docker build -t agatatest .`
    
 3. Run docker image by using command:
 
    `docker run -ti --rm agatatest`
 
 4. For info about convert function run the following:
 
    `docker run -ti --rm agatatest convert --help`
    
 5. To run converter use command:
 
    `docker run -ti --rm -v <absolute_path_to_local_dicom_folder>:/dicom -v  <absolute_path_to_local_images_folder>:/images agatatest convert --dicom_path /dicom --output_path /images`
 
# Running converter at server

 1. To connect to server use command (you must be at the same wifi netwokr as server, now this is `eduoroam`):
 
    `ssh your_login@10.100.2.119`
 
 2. To authorize at docker use command at server terminal (this command will authorize you at docker system and povode to you ability ability to pull docker images from your coworkers):
 
    `docker login`
    
 3. To pull docker image with converet use command at server terminal (this command will instal docker image with converter to server):
 
    `docker pull alinanechyporenko/wildau_charme_2020:latest`
    
 4. To check docker image use command at server terminal (this command will show you info about program):
  
    `docker run -ti --rm alinanechyporenko/wildau_charme_2020` 
    
 5. To load files from local machine to remote server you must open terminal at local machine and use command:
 
    `scp -r /absolute/path/to/input/folder/at/local/machine/  user_name_at_server@10.100.2.119:/absolute/path/to/input/folder/at/server/`
    
    Example:
    
    `scp -r /home/pasha/COST_Germany/agata_project/dicom/  ponoprienko@10.100.2.119:/home/ponoprienko/CA15110_COST_Project/input`
    
  6. To start converter use command at server terminal:
  
     `docker run -ti --rm -v /absolute/path/to/input/folder/at/server:/dicom -v /absolute/path/to/output/folder/at/server:/images alinanechyporenko/wildau_charme_2020 convert --dicom_path /dicom --output_path /images`
     
     Example:
    
    `docker run -ti --rm -v /home/ponoprienko/CA15110_COST_Project/input/segmentation:/dicom -v /home/ponoprienko/CA15110_COST_Project/png:/images alinanechyporenko/wildau_charme_2020 convert --dicom_path /dicom --output_path /images`
    
  7. To download converted images from server to local machine use command at local machine terimal:
  
     `scp -r user_name_at_server@10.100.2.119:/absolute/path/to/output/folder/at/server /absolute/path/to/output/folder/at/local/machine`
     
     Example:
     
     `scp -r ponoprienko@10.100.2.119:/home/ponoprienko/CA15110_COST_Project/png /home/pasha/COST_Germany/agata_project/output`
