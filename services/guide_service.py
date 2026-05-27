import re

class GuideService:
    def get_guide_for_finding(self, finding):
        finding_type = finding.get("type", "")
        message = finding.get("message", "") or ""
        file_path = finding.get("file", "") or ""
        fix_msg = finding.get("fix", "") or ""

        # Default fallback guide
        guide = {
            "title": f"Resolve: {finding_type}",
            "description": message or "This issue should be resolved to ensure the application remains secure and stable.",
            "steps": [
                {
                    "title": "Locate the affected area",
                    "detail": f"Open `{file_path}` and inspect the security warning."
                },
                {
                    "title": "Apply recommendation",
                    "detail": fix_msg or "Review this finding and update the affected code."
                }
            ],
            "before_code": "# Current configuration\n" + (message if message else "Vulnerable code/setup here"),
            "after_code": "# Correct implementation\n" + (fix_msg if fix_msg else "Apply security best practices"),
            "resources": [
                {"name": "OWASP Top Ten Project", "url": "https://owasp.org/www-project-top-ten/"}
            ]
        }

        # 1. AWS Access Key ID
        if "AWS Access Key" in message or "AWS Access Key" in fix_msg or "aws_access_key" in message.lower():
            guide["title"] = "Secure AWS Access Key Credentials"
            guide["description"] = "Hardcoding AWS Access Keys exposes your cloud infrastructure. Attackers scan public repositories constantly and can spin up compute resources or access sensitive data, leading to massive cloud bills."
            guide["steps"] = [
                {"title": "Revoke the key immediately", "detail": "Go to the AWS IAM Console, identify the compromised Access Key ID, and deactivate/delete it right away."},
                {"title": "Store credentials in environment variables", "detail": "Define `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your environment (e.g., in a local `.env` file that is in `.gitignore`)."},
                {"title": "Use default credential loading", "detail": "Modify your code to let AWS SDKs automatically resolve credentials from environment variables instead of hardcoding."}
            ]
            guide["before_code"] = "import boto3\n\n# VULNERABLE: Hardcoded secrets exposed in code\ns3 = boto3.client(\n    's3',\n    aws_access_key_id='AKIAIOSFODNN7EXAMPLE',\n    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'\n)"
            guide["after_code"] = "import os\nimport boto3\n\n# SECURE: Boto3 automatically reads AWS credentials\n# from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.\ns3 = boto3.client('s3')"
            guide["resources"] = [
                {"name": "AWS Access Key Best Practices", "url": "https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html"},
                {"name": "Boto3 Credentials Guide", "url": "https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"}
            ]

        # 2. Google / Gemini API Key
        elif "Google" in message or "Gemini API" in message or "AIzaSy" in message:
            guide["title"] = "Secure Google / Gemini API Keys"
            guide["description"] = "Committed Google/Gemini API keys let anyone consume your cloud resources or generative AI quota, leading to prompt abuse, potential data extraction, and unexpected charges."
            guide["steps"] = [
                {"title": "Revoke the key", "detail": "Go to Google AI Studio or Google Cloud Console (APIs & Services > Credentials) and delete the compromised key."},
                {"title": "Move key to environment", "detail": "Create a `.env` file locally containing `GEMINI_API_KEY=your_key` and add `.env` to `.gitignore`."},
                {"title": "Load key at runtime", "detail": "Load the key via your language's environment library (like `os.environ` in Python or `process.env` in JS)."}
            ]
            guide["before_code"] = "# VULNERABLE: Hardcoded Google API Key in client code\ngenai.configure(api_key=\"AIzaSyD-exampleKey1234567890\")"
            guide["after_code"] = "import os\n\n# SECURE: Read the Gemini API Key from environment variables\napi_key = os.environ.get(\"GEMINI_API_KEY\")\ngenai.configure(api_key=api_key)"
            guide["resources"] = [
                {"name": "Gemini API Key Security", "url": "https://ai.google.dev/gemini-api/docs/api-key"},
                {"name": "GCP Key Security Guidelines", "url": "https://cloud.google.com/docs/authentication/api-keys"}
            ]

        # 3. GitHub Personal Access Token
        elif "GitHub Personal Access Token" in message or "ghp_" in message or "pat_" in message:
            guide["title"] = "Secure GitHub Personal Access Tokens"
            guide["description"] = "Leaking GitHub Personal Access Tokens allows unauthorized parties to push, pull, or modify your repositories, release packages, or account configurations based on the token's scope."
            guide["steps"] = [
                {"title": "Revoke the token", "detail": "Go to GitHub Settings -> Developer settings -> Personal Access Tokens (Classic or Fine-grained) and delete/revoke the token immediately."},
                {"title": "Re-generate with minimal scopes", "detail": "Create a new token selecting only the absolute minimum permissions needed for your script or workflow."},
                {"title": "Inject token at runtime", "detail": "Save the token as an environment variable (or a GitHub Actions Secret) and reference it dynamically."}
            ]
            guide["before_code"] = "# VULNERABLE: Token hardcoded in request headers\nheaders = {\n    \"Authorization\": \"Bearer ghp_xyzSecretToken123456\"\n}"
            guide["after_code"] = "import os\n\n# SECURE: Load the GitHub Token from the system environment\ngithub_token = os.environ.get(\"GITHUB_TOKEN\")\nheaders = {\n    \"Authorization\": f\"Bearer {github_token}\"\n}"
            guide["resources"] = [
                {"name": "GitHub Token Authentication Security", "url": "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-commitment-to-security"}
            ]

        # 4. Slack Webhook URL
        elif "Slack" in message or "hooks.slack.com" in message:
            guide["title"] = "Secure Slack Incoming Webhooks"
            guide["description"] = "Publicly committed Slack webhook URLs allow anyone to send messages to your internal channels, paving the way for corporate phishing, spam, or service disruption."
            guide["steps"] = [
                {"title": "Deactivate webhook", "detail": "Log into your Slack App Directory and delete/disable the compromised webhook URL."},
                {"title": "Generate a new webhook", "detail": "Generate a new webhook URL, making sure to avoid writing it to any source code files."},
                {"title": "Retrieve from configuration", "detail": "Use environment variables to inject the URL into your notification script."}
            ]
            guide["before_code"] = "# VULNERABLE: Direct hardcoding of Slack webhook URL\nwebhook_url = \"https://hooks.slack.com/services/T_TEAM_ID/B_BOT_ID/WEBHOOK_SECRET\""
            guide["after_code"] = "import os\n\n# SECURE: Read webhook URL from environment configuration\nwebhook_url = os.environ.get(\"SLACK_WEBHOOK_URL\")"
            guide["resources"] = [
                {"name": "Slack Webhooks Configuration Guide", "url": "https://api.slack.com/messaging/webhooks"}
            ]

        # 5. Stripe Secret API Key
        elif "Stripe" in message or "sk_live" in message or "sk_test" in message:
            guide["title"] = "Secure Stripe Secret API Keys"
            guide["description"] = "Exposed Stripe secret keys let attackers call Stripe APIs as your business, enabling unauthorized refunds, payment manipulations, customer data theft, and financial fraud."
            guide["steps"] = [
                {"title": "Roll the API key", "detail": "Visit the Stripe Dashboard -> Developers -> API Keys. Click 'Roll key' next to the compromised key to deactivate it and get a new one."},
                {"title": "Utilize environment variables", "detail": "Set `STRIPE_SECRET_KEY` in your environment files and add those files to `.gitignore`."},
                {"title": "Initialize client securely", "detail": "Pass the environment variable into the Stripe initialization method."}
            ]
            guide["before_code"] = "// VULNERABLE: Hardcoded Stripe Secret key\nconst stripe = require('stripe')('sk_test_51Nxxxxxxxxxxxxxxxxxxxxxxxx');"
            guide["after_code"] = "// SECURE: Read key from process environment variables\nconst stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);"
            guide["resources"] = [
                {"name": "Stripe API Keys Best Practices", "url": "https://stripe.com/docs/keys"}
            ]

        # 6. Private SSH / Cryptographic Key
        elif "private ssh/cryptographic key" in message.lower() or "-----BEGIN" in message or "-----BEGIN" in fix_msg:
            guide["title"] = "Secure Cryptographic Private Keys"
            guide["description"] = "Committing private SSH keys or TLS certificates gives attackers access to servers, signing systems, or the ability to decrypt confidential network traffic."
            guide["steps"] = [
                {"title": "Revoke authorization", "detail": "Remove the public key counterpart from server `authorized_keys` files and delete it from deployment configurations."},
                {"title": "Generate a new keypair", "detail": "Generate a new SSH or TLS key pair locally. Never share or commit the private key file."},
                {"title": "Add to .gitignore", "detail": "Add private key extensions and files (like `*.key`, `*.pem`, `id_rsa`) to `.gitignore` so they are never committed."}
            ]
            guide["before_code"] = "# VULNERABLE: Private key file committed in repository\n# file: keys/id_rsa\n-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0123456789...\n-----END RSA PRIVATE KEY-----"
            guide["after_code"] = "# SECURE: Delete the key file from the repo and git history.\n# Add it to your .gitignore:\n# file: .gitignore\n*.pem\n*.key\nid_rsa\nid_ed25519"
            guide["resources"] = [
                {"name": "SSH Key Security Management", "url": "https://www.ssh.com/academy/ssh/key"}
            ]

        # 7. Generic Password in URL
        elif "connection string" in message.lower() or "credentials in connection string" in message.lower():
            guide["title"] = "Secure Database Connection Credentials"
            guide["description"] = "Connection strings often contain plain-text database usernames and passwords. When committed, anyone with repository access can log into, modify, or leak your database contents."
            guide["steps"] = [
                {"title": "Change database password", "detail": "Update the database credentials on the database host immediately to lock out unauthorized users."},
                {"title": "Deconstruct URL components", "detail": "Define environment variables for `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_NAME`."},
                {"title": "Assemble dynamically", "detail": "Format the connection URL at runtime using the environment variables."}
            ]
            guide["before_code"] = "# VULNERABLE: Exposed password in DB URL string\nDATABASE_URL = \"postgresql://db_user:mySuperSecretPassword123@dbhost.internal:5432/production_db\""
            guide["after_code"] = "import os\n\n# SECURE: Reconstruct the connection URL from environment variables\nuser = os.environ.get(\"DB_USER\")\npassword = os.environ.get(\"DB_PASSWORD\")\nhost = os.environ.get(\"DB_HOST\", \"localhost\")\nport = os.environ.get(\"DB_PORT\", \"5432\")\ndb_name = os.environ.get(\"DB_NAME\")\n\nDATABASE_URL = f\"postgresql://{user}:{password}@{host}:{port}/{db_name}\""
            guide["resources"] = [
                {"name": "Twelve-Factor App Configuration", "url": "https://12factor.net/config"}
            ]

        # 8. Environment file committed
        elif ".env" in file_path.lower() or "environment file committed" in message.lower():
            guide["title"] = "Exclude Environment Files from Version Control"
            guide["description"] = "`.env` files contain configuration details and active API keys meant only for local environments. Committing them logs these secrets into Git history permanently, even if deleted later."
            guide["steps"] = [
                {"title": "Remove tracked file", "detail": "Remove the file from git tracking without deleting it from your local machine using: `git rm --cached .env`."},
                {"title": "Update gitignore", "detail": "Open or create a `.gitignore` file at your project root, and add `.env` on a new line."},
                {"title": "Rotate all leaked keys", "detail": "Change and rotate every database password and API key that was stored in the committed `.env` file."}
            ]
            guide["before_code"] = "# VULNERABLE: .env file is tracked in git status\n# git status shows: modified: .env"
            guide["after_code"] = "# SECURE: Untrack .env and add to .gitignore\n# Run: git rm --cached .env\n# Then in .gitignore:\n.env\n.env.local\n.env.development"
            guide["resources"] = [
                {"name": "GitHub Guide to Ignoring Files", "url": "https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files"}
            ]

        # 9. Service Account Key
        elif "serviceaccount" in file_path.lower() or "service account key" in message.lower():
            guide["title"] = "Secure Cloud Service Account Keys"
            guide["description"] = "Google Cloud or Firebase service account credentials grant full administrative authorization to your Cloud console and databases. Committing these exposes the keys to anyone viewing the codebase."
            guide["steps"] = [
                {"title": "Delete compromised key", "detail": "Log into GCP IAM or Firebase Console, locate the Service Account, and delete the exposed JSON key credentials immediately."},
                {"title": "Use Application Default Credentials", "detail": "Do not hardcode service account file paths. Rely on Google's automatic runtime credential detection."},
                {"title": "Ignore files in Git", "detail": "Add `*serviceAccount*.json` to `.gitignore` to ensure they are never committed again."}
            ]
            guide["before_code"] = "// VULNERABLE: Direct reference to committed service account JSON file\nconst admin = require(\"firebase-admin\");\nconst serviceAccount = require(\"./firebase-service-account.json\");\n\nadmin.initializeApp({\n  credential: admin.credential.cert(serviceAccount)\n});"
            guide["after_code"] = "// SECURE: Let Google Cloud libraries find credentials dynamically\nconst admin = require(\"firebase-admin\");\n\nadmin.initializeApp({\n  // Loads from GOOGLE_APPLICATION_CREDENTIALS environment variable automatically\n  credential: admin.credential.applicationDefault()\n});"
            guide["resources"] = [
                {"name": "GCP Service Account Credentials", "url": "https://cloud.google.com/docs/authentication/production"}
            ]

        # 10. SQLite Database
        elif "db.sqlite3" in file_path.lower() or "sqlite database committed" in message.lower():
            guide["title"] = "Exclude Databases from Repositories"
            guide["description"] = "SQLite databases contain app data, user records, and testing metadata. Committing the file exposes user database records and causes git repository bloat due to frequent file changes."
            guide["steps"] = [
                {"title": "Untrack database file", "detail": "Remove the SQLite file from git versioning: `git rm --cached db.sqlite3`."},
                {"title": "Configure gitignore", "detail": "Add `*.sqlite3` and `*.db` to your `.gitignore` file."},
                {"title": "Build on setup", "detail": "Ensure your project builds a fresh database using migrations or setup scripts when run locally."}
            ]
            guide["before_code"] = "# VULNERABLE: Active database file is tracked in git\n# git status shows: modified: db.sqlite3"
            guide["after_code"] = "# SECURE: Remove from git and add to .gitignore\n# Run: git rm --cached db.sqlite3\n# Then add to .gitignore:\n*.sqlite3\n*.db"
            guide["resources"] = [
                {"name": "Django Migration Documentation", "url": "https://docs.djangoproject.com/en/stable/topics/migrations/"}
            ]

        # 11. Wildcard CORS Origin
        elif "cors" in message.lower() or "access-control-allow-origin" in message.lower():
            guide["title"] = "Configure Strict CORS Access Origins"
            guide["description"] = "Setting Cross-Origin Resource Sharing (CORS) to wildcard `*` allows any site (including malicious domains) to read API responses using the victim's credentials inside a browser."
            guide["steps"] = [
                {"title": "Define trusted domains", "detail": "Identify the frontend URLs that need to invoke your API (e.g., `https://my-frontend.com` and `http://localhost:3000`)."},
                {"title": "Configure CORS allowlist", "detail": "Remove wildcard origins and replace them with your list of verified frontend origins."}
            ]
            guide["before_code"] = "# VULNERABLE: CORS wildcard allows all sites to access backend APIs\nfrom flask_cors import CORS\n\nCORS(app, resources={r\"/api/*\": {\"origins\": \"*\"}})"
            guide["after_code"] = "# SECURE: Explicitly define allowed origins\nfrom flask_cors import CORS\n\nALLOWED_ORIGINS = [\n    \"https://my-app-frontend.com\",\n    \"http://localhost:3000\"\n]\nCORS(app, resources={r\"/api/*\": {\"origins\": ALLOWED_ORIGINS}})"
            guide["resources"] = [
                {"name": "OWASP CORS Security Guide", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html"}
            ]

        # 12. Plain HTTP API Call
        elif "http://" in message.lower() or "plain http" in message.lower():
            guide["title"] = "Enforce HTTPS Encryption for API Calls"
            guide["description"] = "Plain HTTP requests transit the network in unencrypted cleartext. Attackers can view, alter, or inject payloads into requests, exposing API tokens and user authentication session data."
            guide["steps"] = [
                {"title": "Update URLs to HTTPS", "detail": "Verify that all backend endpoint references in scripts use the `https://` prefix."},
                {"title": "Enforce SSL redirects", "detail": "Enable automatic HTTP-to-HTTPS redirection in your production environment config."}
            ]
            guide["before_code"] = "// VULNERABLE: Cleartext API endpoint request\nfetch(\"http://api.my-auth-service.com/v1/login\", {\n  method: \"POST\"\n})"
            guide["after_code"] = "// SECURE: TLS Encrypted request\nfetch(\"https://api.my-auth-service.com/v1/login\", {\n  method: \"POST\"\n})"
            guide["resources"] = [
                {"name": "W3C Transport Security Guidelines", "url": "https://www.w3.org/Security/"}
            ]

        # 13. Sensitive Route Exposed
        elif "sensitive" in message.lower() or "exposed route" in message.lower() or "route is exposed" in message.lower():
            guide["title"] = "Secure Sensitive API Routes"
            guide["description"] = "Exposing internal administration, debug, or developer tools without authentication allows anybody to dump databases, shut down applications, or modify system settings."
            guide["steps"] = [
                {"title": "Verify authorization layers", "detail": "Install middleware or decorators to intercept requests on administrative endpoints."},
                {"title": "Verify developer builds", "detail": "Ensure developer/debug utility routes are excluded from release/production versions of the app."}
            ]
            guide["before_code"] = "# VULNERABLE: Route exposes admin commands without verification\n@app.route(\"/admin/reset-database\")\ndef reset_database():\n    db.reset()\n    return \"Done\""
            guide["after_code"] = "# SECURE: Verify authentication and authorization role\n@app.route(\"/admin/reset-database\")\n@login_required\n@admin_only # Custom decorator validating user roles\ndef reset_database():\n    db.reset()\n    return \"Done\""
            guide["resources"] = [
                {"name": "OWASP REST Security Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"}
            ]

        # 14. Debug Mode Enabled
        elif "debug mode" in message.lower() or "debug" in message.lower() and "production" in fix_msg.lower():
            guide["title"] = "Disable Debug Mode in Production"
            guide["description"] = "Leaving application debug mode active in production displays detailed backtraces and system structures on errors, and can expose interactive shells (like Werkzeug) that permit arbitrary remote code execution."
            guide["steps"] = [
                {"title": "Extract config variable", "detail": "Do not hardcode `debug=True`. Define a variable `APP_DEBUG` in your environment configs."},
                {"title": "Evaluate flag dynamically", "detail": "Convert the environment string to boolean and pass it to the server runner."},
                {"title": "Set to false on servers", "detail": "Confirm that production staging and servers have the environment variable configured to `False`."}
            ]
            guide["before_code"] = "# VULNERABLE: Debug mode always active\nif __name__ == \"__main__\":\n    app.run(debug=True)"
            guide["after_code"] = "import os\n\n# SECURE: Debug mode loads from configuration environment\nif __name__ == \"__main__\":\n    # Default to False for safety\n    debug_flag = os.environ.get(\"FLASK_DEBUG\", \"False\").lower() in (\"true\", \"1\")\n    app.run(debug=debug_flag)"
            guide["resources"] = [
                {"name": "Flask Deployment Configuration Safety", "url": "https://flask.palletsprojects.com/en/stable/deploying/"}
            ]

        # 15. Git Merge Conflict Markers
        elif "conflict marker" in message.lower() or "merge conflict" in message.lower():
            guide["title"] = "Resolve and Clean Git Conflict Markers"
            guide["description"] = "Committing unresolved Git conflict markers causes compilation or syntax errors, and reveals a fragmented development workflow where conflicts are pushed without checking."
            guide["steps"] = [
                {"title": "Locate markers", "detail": "Search the file for Git tags like `<<<<<<< HEAD`, `=======`, or `>>>>>>>`."},
                {"title": "Resolve lines manually", "detail": "Compare the changes from your branch and the incoming branch, keeping the correct lines and discarding the other."},
                {"title": "Clean all tags", "detail": "Delete the conflict tag lines, verify the code runs locally, then commit the resolved file."}
            ]
            guide["before_code"] = "# VULNERABLE: Unresolved conflict markers in file\n<<<<<<< HEAD\nDATABASE_URL = \"postgresql://localhost/dev\"\n=======\nDATABASE_URL = os.environ.get(\"DB_URL\")\n>>>>>>> main"
            guide["after_code"] = "# SECURE: Clean resolved code block\nDATABASE_URL = os.environ.get(\"DB_URL\")"
            guide["resources"] = [
                {"name": "Resolving Git Merge Conflicts", "url": "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line"}
            ]

        # 16. Hardcoded Local Absolute Path
        elif "hardcoded local" in message.lower() or "absolute path" in message.lower():
            guide["title"] = "Avert Hardcoded Absolute File Paths"
            guide["description"] = "Absolute file paths point to a specific directory structure on your local machine. Committing these ensures that the application will crash with 'file not found' errors when other developers or deployment nodes attempt to execute the app."
            guide["steps"] = [
                {"title": "Define project base directory", "detail": "Retrieve the path of the current source file relative to the project root using libraries like `pathlib.Path`."},
                {"title": "Build paths relative", "detail": "Construct all storage or config paths dynamically relative to the base directory."}
            ]
            guide["before_code"] = "# VULNERABLE: Path tied to local machine profile\nUPLOAD_DIRECTORY = \"C:\\\\Users\\\\D4rkman\\\\Documents\\\\securerepo\\\\uploads\""
            guide["after_code"] = "from pathlib import Path\n\n# SECURE: Build directories dynamically relative to file location\nBASE_DIR = Path(__file__).resolve().parent\nUPLOAD_DIRECTORY = BASE_DIR / \"uploads\""
            guide["resources"] = [
                {"name": "Python Pathlib Guide", "url": "https://docs.python.org/3/library/pathlib.html"}
            ]

        # 17. Dockerfile Non-Root User
        elif "dockerfile" in file_path.lower() and "user" in message.lower():
            guide["title"] = "Configure Non-Root Users in Containers"
            guide["description"] = "Docker containers run tasks as root by default. If a vulnerability in your application allows code execution inside the container, attackers can compromise host volumes or escape container isolation with root rights."
            guide["steps"] = [
                {"title": "Create a system group and user", "detail": "Add a `RUN groupadd` and `RUN useradd` command to register a low-privilege user account."},
                {"title": "Set ownership", "detail": "Ensure the application workspace folders are owned by the created system user."},
                {"title": "Switch runtime active user", "detail": "Include a `USER` directive to drop root privileges before launching the container process."}
            ]
            guide["before_code"] = "# VULNERABLE: Application runs as root container user\nFROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"app.py\"]"
            guide["after_code"] = "# SECURE: Drop privileges before executing app process\nFROM python:3.9-slim\nWORKDIR /app\n\nRUN groupadd -g 999 appuser && \\\n    useradd -r -u 999 -g appuser appuser\n\nCOPY --chown=appuser:appuser . .\nUSER appuser\nCMD [\"python\", \"app.py\"]"
            guide["resources"] = [
                {"name": "Docker Best Practices for User Security", "url": "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user"}
            ]

        # 18. Outdated Runtime / Software Version
        elif "outdated" in message.lower() or "runtime" in message.lower() or "version" in message.lower() or finding_type == "Outdated Software":
            guide["title"] = "Upgrade Deprecated/Outdated Software"
            guide["description"] = "Using legacy runtime or library versions leaves application layers vulnerable to known CVE exploits. Maintaining runtimes updated ensures compatibility with security fixes."
            guide["steps"] = [
                {"title": "Identify stable version", "detail": "Check the software's website or NPM/PyPI registries for the latest secure LTS (Long-Term Support) version."},
                {"title": "Update config files", "detail": f"Modify version declarations in `{file_path}` (e.g. Dockerfile tags, package.json dependencies, or python runtime versions)."},
                {"title": "Rebuild and test", "detail": "Re-run installations, rebuild image structures, and run unit tests to check for breaking changes."}
            ]
            guide["before_code"] = f"# VULNERABLE: Outdated software reference in {file_path}\n# {message}"
            guide["after_code"] = f"# SECURE: Update version tags to secure releases\n# Refer to: {fix_msg}"
            guide["resources"] = [
                {"name": "NVD NIST Vulnerability Search", "url": "https://nvd.nist.gov/"}
            ]

        return guide
