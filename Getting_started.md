## Firstly you need a local clone of the the project; 
#### Set up a working copy on your computer:
`git clone https://github.com/CodePamoja/heart-rate-monitoring-FHM-.git`

#### Change into the new project’s directory:
`cd heart-rate-monitoring-FHM-`

## Do some work:
The number one rule is to put each piece of work on its own branch. So branch from master:

#### Firstly, ensure you’re on the master branch.
`git checkout master`

#### Sync your local copy with the Original project on git:
`git pull origin master`

## Finally create your new branch. You can name your branch whatever you like:
#### Ensure that you only fix the thing you’re working on!!
`git checkout -b your-branch`
`git branches`

#### Make sure that you commit in logical blocks. Each commit message should be sane:
`git commit -m "I fixed/added this"`

####Push Your new branch:
`git push origin your-branch`

###On Github, create pull request and push to master.

##Subsequent Commits
##Sync project with remote master
###Switch to master branch
`git checkout master`

###Git pull
`git pull`

###Switch to your branch
`git checkout your-branch`


###Merge with master
`git merge master`


##If conflicts (note conflicting files)
###Go to project files (open android studio)
###build project

###Resolve errors by editing the conflicting files

