# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hash | Security - High (Bandit B324) | 47 | MD5 is unsuitable for security-sensitive hashing. | Replace MD5 with SHA-256. |
| Shell command execution | Security - High (Bandit B605) | 58 | os.system() executes a shell command and may introduce command-injection risks. | Replace it with print(). |
| Unsafe eval() | Security - Medium (Bandit B307) | 42 | eval() executes a supplied expression as Python code. | Use a validated numeric discount calculation. |
| Silent exception handling | Code quality (Bandit B110, Pylint W0702, Flake8 E722) | 26-27 | A bare except with pass hides errors. | Handle invalid seat IDs explicitly. |
| Insecure PIN generation | Security - Low (Bandit B311) | 51 | random.randint() is not suitable for security-sensitive PINs. | Use Python's secrets module. |
| Mutable default argument | Bug risk (Pylint W0102) | 15 | The default list is shared between function calls. | Use None and initialize a new list when needed. |
| Unused imports and variables | Code quality (Pylint W0611/W0612, Flake8 F401/F841) | 6, 31, 41, 63 | Unused names reduce code clarity. | Remove unused imports and variables. |
| Missing docstrings and style issues | Style (Pylint C0116/C0103, Flake8 E501/W292) | Multiple | Missing documentation, incorrect naming, a long line, and a missing final newline. | Add docstrings, use snake_case, wrap long lines, and add a final newline. |
| Unsafe file handling | Code quality (Pylint W1514/R1732) | 55-56 | The file lacks an explicit encoding and context manager. | Use with open(..., encoding="utf-8"). |
| Incorrect None comparison | Code quality (Pylint C0121, Flake8 E711) | 32 | The code uses == None instead of is None. | Change the comparison to is None. |

## Initial Analysis Summary

- Pylint score: 5.37/10
- Bandit: 5 findings (2 High, 1 Medium, 2 Low)
- Flake8: 7 reported style and code-quality issues

The findings will be fixed and verified by rerunning all three tools.