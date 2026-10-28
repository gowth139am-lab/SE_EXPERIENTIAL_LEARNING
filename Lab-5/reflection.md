# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding-style violations, and maintainability problems early in development. It improves code quality and reduces the risk of errors.

## 2. What issues did you find, and how did you fix them?

The original program had several issues, including unsafe use of `eval()`, weak MD5 hashing, shell command execution using `os.system()`, insecure random PIN generation, a mutable default argument, and a bare exception handler. I replaced unsafe operations, used secure PIN generation, improved exception handling, corrected file handling, and removed unused variables and imports.

## 3. How did Pylint, Bandit, and Flake8 help improve the program?

Pylint identified code-quality and maintainability problems. Bandit highlighted potential security vulnerabilities. Flake8 detected style violations, unused imports and variables, and formatting problems. Using all three tools provided different perspectives on the same program and helped verify the fixes.

## 4. What did you learn from this lab, and what challenges did you face?

I learned that a program can run correctly while still containing security and code-quality issues. The main challenge was understanding the warnings and fixing the underlying problems without breaking the program's functionality. After the changes, the program ran successfully, the Pylint score improved from 5.37/10 to 10.00/10, Bandit reported no issues, and Flake8 produced no errors. I learned that static analysis should be part of regular software development and testing.