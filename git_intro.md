# Git/Github notes

### Frequent used commands
- Setup remote repo (one-time)
Visit Github repo and fork to my account
```
git clone https://github.com/<username>/<repo>.git
```

- On-going commit push/pull
```
git add .
## local commit
git commit 
## sync w/ remote repo
git push 
```

- Update .gitignore and files on track
```
git rm -r --cached .
```

### Remote repo url
```
## list remote repo
git remote -v 
## change remote repo
git remote set-url origin https://github.com/<username>/<repo_other>.git 
```
