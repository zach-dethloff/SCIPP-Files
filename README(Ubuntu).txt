---Ubuntu Set up and Catch Up---

Step 0(Optional):Install python through anaconda. Go to https://www.anaconda.com/products/individual. Having anaconda on your system allows you to use the anaconda powershell
instead of the windows powershell, as well as a host of other directories like numpy, matplotlib, and many more we use consistently in this project. It is not necessary as 
we will be installing docker, a virtual environment with these directories also installed, but for editing scripts and debugging code outside of docker, its very nice
to have python source files on your system.

Step 1:Install Docker desktop. This is the core of our project, so doing this correctly will make a major difference in efficiency. Start by checking which version of windows
10 you have installed (Settings -> System -> About). Follow this link and read what it has to say about docker set up: https://docs.docker.com/docker-for-windows/install/
For Windows 10 Pro, Enterprise, or Education, use that link. For Windows 10 Home: https://docs.docker.com/docker-for-windows/install-windows-home/ (Select the stable download)
Follow the install instructions, and open docker on your desktop. It should lead you to a WSL 2 installation for a Linux distribution. Follow that link and the instructions on
then restart docker

Step 2: Create a docker hub account. Go into the docker desktop app and create an account. The docker hub site also has useful tutorials to help get situated to the virtual
environment.

Step 3: Download necessary files. For our project, we need files containing data sets to compile and create outputs from. These ROOT files can be found at:
https://mhance.scipp.ucsc.edu/vbfsusy/
Download each of them in the same folder, preferably somewhere you can reach easily from Ubuntu, as we will set up our docker image wherever these files are.

Step 4: Install Xming. Xming is the GUI (Graphical user interface) that we will be using to view our ROOT files and their respective histograms. You can download Xming here:
https://sourceforge.net/projects/xming/
Install Xming normally (keep clicking next) until the install manager asks about additional desktop icons, in which it is a good idea to add both Xming and Xlaunch to your
desktop. Xlaunch will allow you to configure how Xming displays our browser windows, so while all you need to do is launch Xming from your desktop icon, you can customize
how that executes through Xlaunch if needed.  

Step 5: Install Ubuntu. Go to your windows store and download Ubuntu. After that, open your Ubuntu application, and let it finish setting up. It will ask you to create a 
Unix username and password (The password may not show up as your typing it, but it is still being input). Go to your docker desktop app and under settings -> Resources ->
WSL integration, make sure Ubuntu is enabled. Apply and restart if not. Then go back to Ubuntu and type 'docker login' in the command line, this will log you in to use docker
commands (do this every time you open up Ubuntu to use docker). You must then make sure your distribution of WSL is WSL 2 and not 1, and you can check that by entering 

'wsl.exe -l -v'

 into your Ubuntu command line. If it shows up as 2, proceed to the next step. If not, go into windows powershell and type:

wsl.exe --set-distribution Ubuntu 2

If this works, then proceed to the next step. If not, you must unpack your WSL 2 distribution. Go to:

https://simplernerd.com/wsl2-uncompressed/

and follow those steps. Try that again afterwords and you should be all set. You must now navigate to the folder in which the files are in. You can
do that by using the cd /mnt. From here things differ slightly, and after every directory change it is recommended to use the ls command to check what is in the directory.
Continue using cd followed by the directory name until you reach the folder with your ROOT files in it (for me its cd /mnt, cd /c, cd/Users, so on and so forth). Before we 
import the image, make sure Xming is up and running. Now in Ubuntu input this command:

docker run --rm -it -e DISPLAY=[ipv4]:0 -v ${PWD}:/data -w /data gitlab-registry.cern.ch/scipp/mario-mapyde/pyplotting:master

and replace the IPV4 with your ip address to export the display to Xming (Save the command once you have your IP address in it, as this will be how you access this docker
image every time you need to). You can find your ip address by using ipconfig in a powershell window, and it will be listed as IPv4 address. This should start a download 
process that may take a minute. This is a good time to open up Docker Desktop and look for the new docker image when its done. Your final output should look something like 
this:

Status: Downloaded newer image for gitlab-registry.cern.ch/scipp/mario-mapyde/pyplotting:master
root@c4963e8731fb:/data#

Step 6: Testing the image. From here you can start inputing commands to the docker image. Try typing in "root" (without the quotation marks). It should show a box in the 
Ubuntu window saying welcome to ROOT with the version number, and a small ROOT graphic should open up for a second and then disappear. Type in "TBrowser b;" into the 
Ubuntu window and this should open a filesystem showing all of your root data. If this works, click around the files and look at the individual folders to familiarize
yourself with their structure and how the data is arranged. 

Step 7: FlatAna.py. At this point its good to familiarize yourself with GitHub. Hopefully you have been asked to create an account by now so that you can be added to the 
GitHub repository. If not make one, and email gstark@cern.ch with your username and that you need to be added to the repository. Go to:

https://gitlab.cern.ch/scipp/mario-mapyde/-/blob/master/scripts/FlatAna.py#L73

and download that script as it will be our code analysis skeleton to run root files through. 

Step 8: First test. Now put it all together and generate a histogram from the root files we have downloaded. In the Ubuntu window containing the docker image, use the
command:

python FlatAna.py --input "input-file" --output "output-file" 

and run it. Make sure both files are ROOT files by having .root at the end of the file names. The output file
should be a file you create with a new file name. This should process a bunch of events, and then create a window showing the root histogram. 

Now you should be all caught up in using Ubuntu and root files, if there's any further questions you can email me at:

zdethlof@ucsc.edu








