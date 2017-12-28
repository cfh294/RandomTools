# RandomTools
A repository for scripts and tools with no current home

## toggleGrails
Shell script that allows the user to quickly toggle from their current grails version 
to the one they want. I created this because I'm working on two projects simultaneously that
are using two different versions of grails. 

###Pre-use
Assuming your [$GRAILS_HOME environment variable is set up correctly](https://stackoverflow.com/questions/7413061/setting-environment-variables), you need
to have a symbolic link also set up for this tool to work. Example of how to do this:
```shell
# cd into wherever grails is installed, likely /usr/local or /usr/share
cd /usr/local

# set up link, replace grails-2.3.10 with whatever your installation is
sudo ln -s grails-2.3.10/ grails
```

Once this is done, the script should work. The tool works on the assumption that you use the 
grails installation file-naming convention of grails-version-number-format (i.e. grails-2.4.4).

###Use
To change from your current version to 2.4.4 (if it's installed): 
```shell
sudo sh toggleGrails.sh 2.4.4
```