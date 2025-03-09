## Contribution Process
### 1. Preparation
- Review the [open issues](https://github.com/clasanch/pdf-reducer/issues) and find one you want to work on
- Comment on the issue to inform that you're working on it
- Wait for confirmation to avoid duplicate work
### 2. Setup
- Fork the repository to your GitHub account
- Clone your fork locally:
```

git clone https://github.com/YOUR_USERNAME/pdf-reducer.git

cd pdf-reducer

```
- Configure the original repository as "upstream":
```

git remote add upstream https://github.com/clasanch/pdf-reducer.git

```
### 3. Development
- Create a new branch for your feature or fix:
```

git checkout -b feature/issue-number-brief-description

```
For example: `git checkout -b feature/issue-2-add-logging`
- Work on your solution keeping changes focused and concise
- Keep your fork synchronized with any changes in the original repository:
```

git fetch upstream

git checkout main

git merge upstream/main

git checkout your-feature-branch

git rebase main

```
- Make sure to follow the project's code conventions
- Include tests if possible
### 4. Submitting Changes
- Ensure your code works correctly
- Commit your changes with descriptive messages:
```

git commit -m "Fix: clear description of the change"

```
- Push the changes to your fork:
```

git push origin your-feature-branch

```
- Create a Pull Request from your feature branch to the original repository's main branch
- Clearly describe what changes you've made and why
### 5. Review
- Respond to comments and make requested changes
- Once approved, the maintainer will merge your PR into the main branch
