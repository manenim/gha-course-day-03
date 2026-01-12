# Day 3: Contexts and Expressions (Conditions)

## **1. Concepts**

### **The "Context" Object**
GitHub Actions exposes a set of variables called **Contexts**. These are JSON objects containing information about the workflow run, the runner, the secrets, and the event that triggered the run.

The most important one is the **`github` context**.
It behaves like a global variable you can access anywhere using the expression syntax `${{ }}`.

**Common `github` properties:**
*   `${{ github.actor }}`: The username who triggered the workflow (e.g., `manenim`).
*   `${{ github.ref }}`: The branch or tag ref (e.g., `refs/heads/main`).
*   `${{ github.event_name }}`: The event (e.g., `push`, `pull_request`).
*   `${{ github.sha }}`: The commit SHA.

### **Expressions & Conditionals (`if`)**
You can use these contexts to make decisions. The `if` keyword allows you to prevent a Job or Step from running unless a condition is met.

```yaml
steps:
  - name: Deploy to Prod
    if: github.ref == 'refs/heads/main'  # Only run on main branch
    run: ./deploy.sh
```

**Functions:**
*   `startsWith('Hello World', 'He')` -> true
*   `contains(github.ref, 'release')` -> true if branch is `release/v1`
*   `always()` -> Forces a step to run even if previous steps failed (great for cleanup/logs).

---

## **2. Visuals: The Decision Tree**

```
[ Job Triggered ]
       |
       v
[ Condition Check: "Is branch == main?" ]
       |
       +----(YES)----> [ Run Job/Step ]
       |
       +----(NO)-----> [ SKIP (Greyed out in UI) ]
```

---

## **3. Code Examples**

**Example 1: Accessing Data (Templating)**
```yaml
steps:
  - run: echo "Triggered by ${{ github.actor }} on branch ${{ github.ref }}"
```

**Example 2: Conditional Job (The Gate)**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps: ...

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' # <--- CONDITIONAL JOB
    runs-on: ubuntu-latest
    steps: ...
```

---

## **4. References**
*   [Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
*   [Expressions](https://docs.github.com/en/actions/learn-github-actions/expressions)

---

## **5. The Challenge: Platform Ticket PT-103**

**Context:** The team wants a pipeline for their Python app. However, they have a strict rule: **"We only release to production from the `main` branch."**

**Objective:** Create a pipeline that tests *every* branch, but only "releases" (simulated) on `main`.

**Requirements:**
1.  **Repo Setup:** Initialize `day-3` as a new git repo (Polyrepo style).
2.  **File Location:** `.github/workflows/day-3.yaml`
3.  **Triggers:** `push` (to any branch).
4.  **Job 1: `status-check`**
    *   Runs on `ubuntu-latest`.
    *   **Step 1:** Checkout code.
    *   **Step 2:** Print the phrase: `"Running on branch ${{ github.ref }}"`.
    *   **Step 3:** Setup Python (v3.10) - *Practice looking up the action!*
    *   **Step 4:** Run the script `python main.py`.
5.  **Job 2: `release`**
    *   **CRITICAL:** Must depend on `status-check`.
    *   **CRITICAL:** Must include an `if:` condition so it **ONLY** runs if the branch is `refs/heads/main`.
    *   **Step:** Print `"Releasing to Production..."`.

**Constraints:**
*   Do NOT hardcode the branch name in the print statement; use the context variable.
*   Verify the logic by pushing to a branch named `feature/test` (Job 2 should skip) and then to `main` (Job 2 should run).
