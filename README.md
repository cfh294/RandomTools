# RandomTools
A repository for scripts and tools with no current home

## toggleGrails
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