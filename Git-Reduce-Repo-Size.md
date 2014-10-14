Note: Originally copied from the [Zuha](https://github.com/zuha/Zuha/wiki/Git-Reduce-Repo-Size) wiki.

- - - - - - - - - -

When you first start working with git you typically pay no attention to the size of the repo.  You commit anything and everything.  Then at some point you start to realize that your repo is huge.  (One was pushing 2 gigabytes)

In order to reduce it at this future point, and keep the history here is the simplest way.  Noting that we only want to keep a single branch - the master - in our case.  No tags, no remote or local branches, and when we're done every one who wants to collaborate will need to delete their local repos and pull a new clone. 

Therefore, this should only be done when all branches are synced, so that they can be reduced to a single master branch on both the remote repo and locally.  There should be no tags.

# Sync and clean
1. `git clone <GIT REPO URL> <DIRECTORY>`  Clone a clean version of the repository.  
1. `git merge <BRANCH>`  Merge all of the branches you want to keep into master. 
1. `git push <REMOTE NAME> :<BRANCH NAME>` ex. `git push origin :dev`  Delete all remote branches except master.  
1. `git branch -d <BRANCH NAME>` ex. `git branch -d dev`  Delete all local branches except master.

# Find large files
1. `git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -g | tail -5` Checks for the largest files.
1. `git rev-list --objects --all | grep a0d770a97ff0fac0be1d777b32cc67fe69eb9a98` Returns the file name for the specified key.

# Get rid of large files
1. `git filter-branch --index-filter 'git rm --cached --ignore-unmatch <FILE NAME>'` Removes the file from all revisions.
    * ex. `git filter-branch --index-filter 'git rm --cached --ignore-unmatch **/subdirectory/*'` All subdirectories that appears in multiple directories
    * ex. `git filter-branch --index-filter 'git rm --cached --ignore-unmatch /subdirectory/*.jpg'` All jpg files in this subdirectory.
    * ex. `git filter-branch --index-filter 'git rm --cached --ignore-unmatch /subdirectory/*'` All files in this subdirectory and consequently this subdirectory because git doesn't support empty directories.
    * ex. `git filter-branch --index-filter 'git rm --cached --ignore-unmatch subdirectory/**/subdirectory2/*'` All subdirectory2 which are contained within the subdirectory

1. `rm -rf .git/refs/original/` Remove git's backup.
+ `git reflog expire --expire=now --all` Expires all the loose objects.
+ `git fsck --full --unreachable` Checks if there are any loose objects.
+ `git repack -A -d` Repacks the pack.
+ `git gc --aggressive --prune=now`  Finally removes those objects.
+ `git push --force [remote] master`  You will need to do a force push, because the remote will sort of think you went back in time, so just make sure you've pulled before you started all of this. 
