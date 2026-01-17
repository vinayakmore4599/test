# Git Commands Guide - Working with Remote Repositories

This guide covers all essential git commands for working with remote repositories.

## Prerequisites

- Git installed on your machine
- A GitHub/GitLab account
- SSH key or HTTPS credentials configured

## Step 1: Initial Setup (First Time Only)

### Configure Git Identity

Set your name and email globally:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Or set it locally for the current repository:
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Verify Configuration

```bash
git config --list
```

## Step 2: Clone a Repository

Clone an existing remote repository to your local machine:

```bash
# Clone via HTTPS (simpler, but requires credentials each time)
git clone https://github.com/username/repository.git

# Clone via SSH (requires SSH key setup, more secure)
git clone git@github.com:username/repository.git

# Clone into a specific directory
git clone https://github.com/username/repository.git my-folder
```

## Step 3: Initialize and Add Remote (New Repository)

If you have a local project and want to push it to a new remote:

### Initialize Git
```bash
cd your-project-folder
git init
```

### Add Remote Repository

```bash
# Add a new remote named 'origin' (standard convention)
git remote add origin https://github.com/username/repository.git

# Or using SSH
git remote add origin git@github.com:username/repository.git
```

### Verify Remote
```bash
git remote -v
```

Expected output:
```
origin  https://github.com/username/repository.git (fetch)
origin  https://github.com/username/repository.git (push)
```

## Step 4: Stage and Commit Changes

### Check Status
```bash
git status
```

Shows which files are modified, staged, or untracked.

### Stage Files

Stage all changes:
```bash
git add .
```

Stage specific file:
```bash
git add filename.txt
```

Stage multiple files:
```bash
git add file1.txt file2.txt
```

### Commit Changes

```bash
git commit -m "Your commit message"
```

Best practices for commit messages:
```bash
# Bad
git commit -m "fix"

# Good
git commit -m "Fix: Add error handling to user authentication"
git commit -m "Feat: Implement Docker deployment"
git commit -m "Docs: Update README with deployment steps"
```

## Step 5: Push to Remote

Push committed changes to the remote repository:

### Push to Default Branch (main/master)

```bash
git push origin main
```

Or if your branch is named differently:
```bash
git push origin master
```

### Push Specific Branch

```bash
git push origin branch-name
```

### Push All Branches

```bash
git push origin --all
```

### Force Push (USE WITH CAUTION)

Only if you need to overwrite remote history:
```bash
git push origin main --force
```

## Step 6: Pull from Remote

Get latest changes from remote repository:

### Pull Latest Changes

```bash
git pull origin main
```

Equivalent to:
```bash
git fetch origin
git merge origin/main
```

### Pull Specific Branch

```bash
git pull origin branch-name
```

## Step 7: Working with Branches

### List Branches

Local branches:
```bash
git branch
```

All branches (local + remote):
```bash
git branch -a
```

Remote branches:
```bash
git branch -r
```

### Create New Branch

```bash
# Create branch locally
git branch new-branch-name

# Create and switch to new branch
git checkout -b new-branch-name

# Modern way (Git 2.23+)
git switch -c new-branch-name
```

### Switch Between Branches

```bash
# Switch to existing branch
git checkout branch-name

# Modern way
git switch branch-name
```

### Push New Branch to Remote

```bash
git push origin new-branch-name
```

Set upstream tracking (automatic for future pushes):
```bash
git push -u origin new-branch-name
```

### Delete Branch

Delete local branch:
```bash
git branch -d branch-name
```

Force delete local branch:
```bash
git branch -D branch-name
```

Delete remote branch:
```bash
git push origin --delete branch-name
```

## Step 8: Synchronize with Remote

### Fetch Latest Changes (without merging)

```bash
git fetch origin
```

This updates your local copy of remote branches but doesn't merge.

### Pull with Rebase (Cleaner History)

Instead of merge commit, rebase your changes:
```bash
git pull --rebase origin main
```

## Step 9: View Commit History

### Basic Log

```bash
git log
```

### Short Log

```bash
git log --oneline
```

Shows compact history.

### Log with Graph

```bash
git log --oneline --graph --all
```

Visual representation of branches.

### Log for Specific File

```bash
git log filename.txt
```

## Step 10: Undo Changes

### Undo Unstaged Changes

```bash
git restore filename.txt
```

Or older syntax:
```bash
git checkout -- filename.txt
```

### Undo Staged Changes

```bash
git restore --staged filename.txt
```

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Undo Last Commit (Discard Changes)

```bash
git reset --hard HEAD~1
```

### Revert a Specific Commit

```bash
git revert commit-hash
```

Creates a new commit that undoes the changes.

## Complete Workflow Example

Here's a typical workflow from start to finish:

```bash
# 1. Clone repository
git clone https://github.com/username/repository.git
cd repository

# 2. Create new branch for feature
git checkout -b feature/add-deployment

# 3. Make changes to files
# ... edit files ...

# 4. Check status
git status

# 5. Stage changes
git add .

# 6. Commit with meaningful message
git commit -m "Feat: Add Kubernetes deployment guide"

# 7. Push branch to remote
git push -u origin feature/add-deployment

# 8. Create Pull Request on GitHub/GitLab
# (Do this through the web interface)

# 9. After PR merge, switch to main
git checkout main

# 10. Pull latest changes
git pull origin main

# 11. Delete feature branch locally
git branch -d feature/add-deployment

# 12. Delete feature branch on remote
git push origin --delete feature/add-deployment
```

## Useful Aliases

Create shortcuts for common commands:

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.log-graph 'log --oneline --graph --all'
```

Then use them:
```bash
git co main          # instead of git checkout main
git st               # instead of git status
git log-graph        # instead of git log --oneline --graph --all
```

## Common Issues and Solutions

### Authentication Issues

#### HTTPS - Credentials Not Saved
```bash
# Enable credential caching
git config --global credential.helper cache

# Cache for 1 hour (3600 seconds)
git config --global credential.helper 'cache --timeout=3600'
```

#### SSH - Permission Denied
```bash
# Check SSH key
ssh -T git@github.com

# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add key to SSH agent
ssh-add ~/.ssh/id_ed25519
```

### Merge Conflicts

When pulling results in conflicts:

```bash
# View conflicted files
git status

# Edit conflicted files manually and resolve conflicts

# After resolving, stage changes
git add .

# Complete the merge
git commit -m "Resolve merge conflicts"
```

### Wrong Branch Committed

```bash
# Check current branch
git branch

# Move last commit to correct branch
git cherry-pick commit-hash

# Delete commit from wrong branch
git reset --hard HEAD~1
```

### Accidental Push

```bash
# View commit history
git log --oneline

# Revert the problematic commit
git revert commit-hash

# Push revert
git push origin main
```

## Essential Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `git clone` | Clone remote repo locally |
| `git add .` | Stage all changes |
| `git commit -m ""` | Commit changes |
| `git push origin main` | Push to remote |
| `git pull origin main` | Fetch and merge from remote |
| `git fetch origin` | Fetch without merging |
| `git branch` | List branches |
| `git checkout -b` | Create and switch branch |
| `git merge branch-name` | Merge branch into current |
| `git status` | Show working tree status |
| `git log` | Show commit history |
| `git reset --hard` | Discard all changes |
| `git revert` | Create undo commit |
| `git stash` | Temporarily save changes |
| `git remote -v` | Show remote repositories |

## Best Practices

1. **Commit Often** - Small, focused commits are easier to understand
2. **Use Descriptive Messages** - Help others understand your changes
3. **Create Feature Branches** - Keep main branch stable
4. **Pull Before Push** - Avoid conflicts by staying updated
5. **Review Changes** - Use `git diff` before committing
6. **Never Force Push to Shared Branches** - Can lose others' work
7. **Keep Commits Atomic** - One feature per commit
8. **Use .gitignore** - Exclude files that shouldn't be tracked

## Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)
