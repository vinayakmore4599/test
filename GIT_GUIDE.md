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

## Step 11: Protecting Sensitive Files

### Add Files to .gitignore

Edit your `.gitignore` file and add sensitive files:

```
# Kubernetes Secrets (DO NOT COMMIT)
k8s/secret.yaml

# Environment Variables
.env
.env.local

# API Keys
api-keys.json
credentials.txt
```

### Remove Files Already Tracked by Git

If you accidentally committed a sensitive file, remove it from git tracking:

```bash
# Remove file from git tracking (keeps file locally)
git rm --cached k8s/secret.yaml

# Or remove multiple files
git rm --cached k8s/secret.yaml .env api-keys.json
```

### Update .gitignore

```bash
# Stage the .gitignore update
git add .gitignore

# Commit the change
git commit -m "Chore: Add sensitive files to .gitignore"

# Push to remote
git push origin main
```

### Complete Workflow for Protecting Secrets

```bash
# 1. Add sensitive file to .gitignore
echo "k8s/secret.yaml" >> .gitignore

# 2. Remove from git tracking
git rm --cached k8s/secret.yaml

# 3. Stage changes
git add .gitignore

# 4. Commit
git commit -m "Chore: Add k8s/secret.yaml to .gitignore to protect API keys"

# 5. Push to remote
git push origin main
```

### Create Example/Template Files

Instead of committing secrets, create example files:

```bash
# Create template files
cp k8s/secret.yaml k8s/secret.yaml.example
```

Content of `k8s/secret.yaml.example`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: flask-app-secret
  namespace: flask-app
type: Opaque
stringData:
  PERPLEXITY_API_KEY: "YOUR_API_KEY_HERE"  # Replace with actual key
```

Then add to .gitignore:
```
k8s/secret.yaml
.env
api-keys.json
```

And commit the example files:
```bash
git add k8s/secret.yaml.example
git commit -m "Docs: Add secret.yaml.example as template"
git push origin main
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

### Secrets Already in Git History

If you added sensitive files (API keys, passwords, etc.) and they're already in your commit history, `.gitignore` alone won't help. You need to remove them from history.

#### Remove Secrets from Commits

Remove file from git tracking:
```bash
git rm --cached k8s/secret.yaml
```

Or remove multiple sensitive files:
```bash
git rm --cached .env k8s/secret.yaml api-keys.json
```

#### Update .gitignore and Amend Commit

```bash
# Add files to .gitignore
echo "k8s/secret.yaml" >> .gitignore
echo ".env" >> .gitignore

# Stage changes
git add .gitignore

# Amend the last commit (combine changes)
git commit --amend --no-edit

# Force push to update remote (use with caution)
git push --force-with-lease
```

#### Complete Workflow to Clean Secrets

```bash
# 1. Remove secrets from tracking
git rm --cached k8s/secret.yaml

# 2. Add to .gitignore
echo "k8s/secret.yaml" >> .gitignore

# 3. Commit the changes
git add .gitignore
git commit -m "Remove secrets from history and add to .gitignore"

# 4. Force push to update remote
git push --force-with-lease
```

#### Important Notes on Force Push

- `git push --force-with-lease` is safer than `--force` (checks remote hasn't changed)
- Only force push if you're sure no one else has pulled those commits
- For team repositories, coordinate with team members before force pushing
- On shared main branch, communicate first

#### Create Secret Template Files

Instead of tracking actual secrets, commit template files:

```bash
# Create template file
cp k8s/secret.yaml k8s/secret.yaml.example

# Edit template with placeholder values
# Example content:
# apiVersion: v1
# kind: Secret
# metadata:
#   name: flask-app-secret
# stringData:
#   PERPLEXITY_API_KEY: "YOUR_API_KEY_HERE"

# Add template to git
git add k8s/secret.yaml.example

# Add actual secret to .gitignore
echo "k8s/secret.yaml" >> .gitignore
git add .gitignore

# Commit
git commit -m "Add secret.yaml.example template and exclude actual secrets"

# Push
git push origin main
```

#### Verify Secrets Are Removed

Check that sensitive files are no longer in git:
```bash
# Search git history for common secret patterns
git log -p | grep -i "api_key\|password\|secret"

# Or use git-secrets tool
git secrets --scan
```

## Step 12: Check Tracked Files

### View All Tracked Files

List all files currently tracked by git:

```bash
git ls-files
```

### View Tracked Files in Specific Directory

```bash
# Check what files are tracked in k8s/ directory
git ls-files k8s/

# Check what files are tracked in src/ directory
git ls-files src/
```

### Find Untracked Files

```bash
# Show untracked files
git ls-files --others --exclude-standard
```

### Check File Status

```bash
# Detailed status of tracked vs untracked
git status
```

Output categories:
- **Untracked files**: Not in .gitignore, not tracked by git
- **Changes not staged**: Files changed but not added
- **Changes to be committed**: Staged files ready to commit

### Example Workflow to Find and Remove Sensitive Files

```bash
# 1. List files in k8s directory to see what's tracked
git ls-files k8s/

# 2. Remove specific file from tracking
git rm --cached k8s/secret.yaml

# 3. Verify it's removed from staging area
git status

# 4. Stage the .gitignore update
git add .gitignore

# 5. Commit and push
git commit -m "Remove k8s/secret.yaml from tracking"
git push origin main
```

### Remove Multiple Files at Once

```bash
# Remove several sensitive files
git rm --cached .env k8s/secret.yaml credentials.json

# Or use pattern matching
git rm --cached 'k8s/*secret*'

# Then commit
git add .gitignore
git commit -m "Remove sensitive files from git tracking"
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
