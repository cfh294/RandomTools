# RandomTools
A repository for scripts and tools with no current home

## db2domain
Python command line tool that allows you to reverse engineer an Oracle database table and output a Grails domain class.

### Note
Grails 2+ has a reverse engineer plugin but it's completely overcomplicated in my opinion and I needed something more like
Django's "inspectdb" command.

### Usage
```shell
python db2domain.py <jdbc connection string> <password> <domain class name> <table owner> <table name>
```
Optional arguments:
+ -vf: The name of the version column
+ -i:  The name of the id column
+ -pf: A column name prefix that you want your grails class to ignore when creating field names
+ -pkg: The name of the package that you want your domain class to belong to

### Dependencies
+ Python 3
+ cx Oracle and related Oracle installation requirements

## toggleGrails

### NOTE: [SDKMAN does this](http://sdkman.io/usage.html#default)! I wrote this out of neccessity because sdkman was not working on my computer at the time! While this script is no longer needed, it was still a good exercise in basic bash programming!

Shell script that allows the user to quickly toggle from their current grails version 
to the one they want on Unix systems. I created this because I'm working on two projects simultaneously that
are using two different versions of grails. 

### Pre-use
Assuming your GRAILS_HOME environment variable is set to /usr/local/grails (or /usr/share/grails if that's where you have grails installed), you need
to have a symbolic link also set up for this tool to work. Example of how to do this:
```shell
# cd into wherever grails is installed, likely /usr/local or /usr/share
cd /usr/local

# set up link, replace grails-2.3.10 with whatever your installation is
sudo ln -s grails-2.3.10/ grails
```

[More info on this here.](https://128bit.io/2011/03/31/install-groovy-and-grails-on-mac-os-x/)

Once this is done, the script should work. The tool works on the assumption that you use the 
grails installation file-naming convention of grails-version.number.format (i.e. grails-2.4.4).

### Use
To change from your current version to 2.4.4 (if it's installed): 
```shell
sudo sh toggleGrails.sh 2.4.4
```

### Tip
As a shortcut, paste the script into your home directory. Then use your favorite text editor to edit your .bash_profile to include: 
```shell
alias tg="sudo sh ${HOME}/toggleGrails.sh"
```
Now, on the terminal, you can quickly use the tool by simply typing something like: 
```shell
tg 2.3.3
```

### Warning
If you have grails installed somewhere other than /usr/local, you have to make a minor edit to the script.
Change the line:
```shell
cd /usr/local
```
to...
```shell
cd directory/that/houses/grails
```
