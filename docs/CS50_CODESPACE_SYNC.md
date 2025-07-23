# CS50 Codespace Workflow Guide

## ⚠️ Important: Git is Disabled in CS50 Codespaces

**CS50 codespaces have Git disabled**, so you cannot use `git pull` or `git push` commands. This requires a different workflow than standard GitHub development.

## 🚀 Recommended Workflow for CS50

### 1. Local Development (Your PC)
```bash
# Make changes to your code
# Test locally
python app.py

# Commit and push to GitHub
git add .
git commit -m "Description of changes"
git push origin main
```

### 2. CS50 Codespace Setup
1. **Download ZIP from GitHub**:
   - Go to your GitHub repository
   - Click "Code" → "Download ZIP"
   - Extract to a known location

2. **Open in CS50 Codespace**:
   - In VSCode, press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Codespaces" and select "GitHub Codespaces: Open in Codespace"
   - Or use the Codespaces extension in the sidebar

3. **Upload Files**:
   - Drag and drop extracted files into the codespace
   - Or use the file upload feature in the codespace

## 🔧 CS50 Codespace Navigation

### Finding Your Codespace
- **Command Palette**: `Ctrl+Shift+P` → "Codespaces"
- **Extension**: Install "GitHub Codespaces" extension
- **Browser**: Go to github.com → Codespaces tab

### Workspace Management Challenges

#### The Problem
CS50 codespaces are **isolated environments** - you can't easily switch between:
- CS50 codespace
- Local GitHub repos
- OneDrive projects (Udemy courses)
- Other development environments

#### Solutions

##### 1. Use Multiple VSCode Windows
- **CS50 codespace**: One VSCode window
- **Local projects**: Another VSCode window
- **Udemy courses**: Third VSCode window

##### 2. Use Different Browsers/Profiles
- **CS50**: Dedicated browser profile
- **Personal projects**: Another profile

##### 3. Use VSCode Desktop for Local Work
- **Local development**: VSCode desktop
- **CS50 submission**: Codespace only

## 🐍 Environment Management

### Virtual Environment Issues
```bash
# CS50 codespace might not recognize pip
# Try these alternatives:
python3 -m pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Environment Differences
- **CS50**: Python 3.x, limited packages
- **Your PC**: Full Python environment
- **Settings**: May not sync across environments

### Best Practices
1. **Always check Python version**: `python --version`
2. **Use explicit pip calls**: `python -m pip install`
3. **Keep requirements.txt updated**
4. **Test in both environments**

## 📁 File Organization Strategy

### Recommended Structure
```
OneDrive/
├── Udemy_Courses/
│   ├── Course1/
│   └── Course2/
├── Personal_Projects/  # Avoid GitHub conflicts
└── Temporary/

GitHub_Projects/
├── Project1/
├── Project2/
└── listener-maths-crossword/
```

### Why Not OneDrive for GitHub Projects
- **Sync conflicts** with Git
- **File locking** issues
- **Version control** confusion
- **Performance** problems with large repos

## 🔄 Multi-Machine Development

### Settings Synchronization
- **VSCode settings**: May sync via Microsoft account
- **Extensions**: May sync automatically
- **Workspace settings**: Usually local to machine

### Environment Setup Per Machine
```bash
# Each machine needs:
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🎯 CS50-Specific Workflow

### For Project Submission
1. **Develop locally** on your PC
2. **Test thoroughly** in local environment
3. **Push to GitHub** when ready
4. **Download ZIP** for CS50 codespace
5. **Upload to codespace** for final testing
6. **Record demo** in codespace environment

### Demo Preparation
- **Test everything** in codespace before recording
- **Check all features** work in CS50 environment
- **Prepare talking points** for video
- **Have backup plan** if something breaks

## 🛠️ Troubleshooting

### Common CS50 Issues
1. **Pip not found**: Use `python -m pip`
2. **Port conflicts**: Use different ports
3. **File permissions**: Check file ownership
4. **Memory limits**: Optimize for codespace constraints

### Workspace Switching
- **Close current workspace**: File → Close Workspace
- **Open new workspace**: File → Open Folder
- **Use multiple windows**: Window → New Window

## 📚 Learning Strategy

### What to Focus On
- ✅ **Programming logic** and algorithms
- ✅ **User experience** and interface design
- ✅ **Problem-solving** approaches
- ✅ **Code organization** and documentation

### What to Treat as "Black Boxes"
- 🔧 **Deployment systems** (Render, Heroku)
- 🔧 **Framework internals** (Flask details)
- 🔧 **Environment management** (venv, pip)
- 🔧 **Git workflow** (beyond basic commands)

## 🎉 Success Metrics

### Project Completion
- ✅ **Core functionality** works in CS50 environment
- ✅ **Documentation** is comprehensive
- ✅ **Code** is well-organized and commented
- ✅ **Demo** showcases key features

### Learning Outcomes
- ✅ **Problem-solving** skills demonstrated
- ✅ **Technical implementation** is solid
- ✅ **User experience** is polished
- ✅ **Documentation** shows understanding

## 🔮 Future Considerations

### If You Continue Development
- **Consider** moving away from CS50 codespaces
- **Use** local development + cloud deployment
- **Explore** other development environments
- **Focus** on building interesting applications

### For Other Courses
- **Udemy**: Use OneDrive for easy multi-machine access
- **Personal projects**: Use GitHub + local development
- **CS50**: Use codespaces only for submission

This updated workflow acknowledges the limitations of CS50 codespaces while providing practical solutions for multi-environment development. 