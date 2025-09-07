# GitHub Repo Sweeper

A lightweight command line utility for cleaning up your GitHub repositories. Easily list, search, and delete repositories from your account with a simple interactive interface.

---

## ✨ Features

- **List all repositories** for your GitHub account
- **Search repositories** by name and/or programming language
- **Delete repositories** interactively (with confirmation)
- **Personal Access Token (PAT)** authentication (with optional secure save)
- **Error logging** to `sweeper.log`

---

## 🚀 Installation

> **Requirements:**  
> - Python 3.8+
> - [PyGithub](https://pygithub.readthedocs.io/en/latest/)  
> - [keyring](https://pypi.org/project/keyring/)  
> - A GitHub [Personal Access Token (PAT)](https://github.com/settings/tokens)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kuhlekt1v/gh-repo-sweeper.git
   cd gh-repo-sweeper
   ```

2. **Install using pip:**
   ```bash
   # Normal installation.
   pip install .

   # Development installation (code changes will be reflected immediately).
   pip install -e .
   ```
   *(Using a virtual environment during development is recommended)*

---

## 🛠️ Usage

After installation, simply run:

```bash
gh-repo-sweeper
```

You’ll interact with a simple text-based menu:

```text
=== GitHub Repo Sweeper ===

A lightweight utility for cleaning up your GitHub repositories.
You can list repositories, search by name, and optionally delete
repos you no longer need.

What would you like to do?
==========================
1. List all repositories
2. Search for a repository
3. Exit
```

### 1. Listing Repositories

- Select `1` to list all your repositories.
- You’ll see a numbered list of your repositories with their main language.

### 2. Searching Repositories

- Select `2` to search by keyword, programming language, or both.
- Enter your criteria as prompted.
- Matching repositories will be displayed.

### 3. Deleting Repositories

- After listing or searching, you’ll be offered deletion options:
    - Delete by index: e.g., `1,2,5` or `1-3,7`
    - Delete by full name: e.g., `username/repo1`
- You **must confirm** before deletion.
- **Deleted repositories cannot be restored!**

---

## 🔑 Authentication

On first run, you’ll be prompted for a GitHub Personal Access Token (PAT).
- You can [generate a PAT here](https://github.com/settings/tokens) (ensure `repo` scope is enabled for deletion).
- The token can be saved securely for future use using your system's keyring.

---

## ⚠️ Warning

**Repository deletion is irreversible!**  
Be certain before confirming deletions.

---

## 👤 License & Contribution

MIT License.  
Feel free to open issues or submit PRs!

---

## 🙋 FAQ

### Q: Does this delete organizations’ repositories?
A: No, only personal repositories you own and have permission to delete.

### Q: Where is my token stored?
A: If you choose to save it, your GitHub token is securely stored in your system's keyring (e.g., macOS Keychain, Windows Credential Manager, or Linux Secret Service) using the `keyring` library. It is **never saved in plain text**.

---

## 💡 Inspiration

Built by [@kuhlekt1v](https://github.com/kuhlekt1v) — build in public!
