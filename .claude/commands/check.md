# /check

**Description:**  
Run `./refresh_problems.sh` to refresh `.vscode/problems.json` with the current VS Code problems.  
Then read `.vscode/problems.json`. If the file is empty or shows zero errors, do nothing.  
If it contains errors, generate and apply patches to fix them.

**Usage:** 
/check