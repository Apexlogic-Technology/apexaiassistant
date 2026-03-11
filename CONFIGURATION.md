# ApexAiAssistant Configuration Guide

> **For Apexlogic Technology Support Staff** — Use this guide when setting up ApexAiAssistant on a client's ERPNext system.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Initial Configuration](#3-initial-configuration)
4. [AI Provider Setup](#4-ai-provider-setup)
5. [Enabling Modules](#5-enabling-modules)
6. [Action Registry Setup](#6-action-registry-setup)
7. [User Roles and Permissions](#7-user-roles-and-permissions)
8. [Verifying the Installation](#8-verifying-the-installation)
9. [Troubleshooting](#9-troubleshooting)
10. [Uninstalling the App](#10-uninstalling-the-app)

---

## 1. Prerequisites

Before deploying ApexAiAssistant, confirm the following on the client's server:

| Requirement | Minimum Version | Check Command |
|---|---|---|
| Frappe Framework | v15.x | `bench version` |
| ERPNext | v15.x | `bench version` |
| Python | 3.10+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| Yarn | 1.22+ | `yarn --version` |

**Python packages required** (auto-installed via `requirements.txt`):
- `openai >= 1.0.0`
- `litellm >= 1.0.0`
- `pandas`, `numpy`, `plotly`, `scikit-learn`
- `openpyxl`, `PyPDF2`

> [!IMPORTANT]
> The client must have an active account with at least one AI provider (OpenAI, Anthropic, Ollama, or DeepSeek) with API credits configured before going live.

---

## 2. Installation

Run all commands from the **bench root directory** (usually `~/frappe-bench`).

### Step 1 — Fetch the app

```bash
bench get-app https://github.com/Apexlogic-Technology/apexaiassistant.git
```

If the esbuild step fails (known harmless warning), add the app manually:

```bash
printf "\napexaiassistant" >> sites/apps.txt
```

### Step 2 — Install on the client site

Replace `client-site.com` with the actual site name:

```bash
bench --site client-site.com install-app apexaiassistant
```

### Step 3 — Install Python dependencies

```bash
./env/bin/pip install litellm
```

### Step 4 — Run migrations

```bash
bench --site client-site.com migrate
```

### Step 5 — Copy assets (if not done automatically)

Only needed if the chat icon or styles don't appear:

```bash
mkdir -p sites/assets/apexaiassistant/css
mkdir -p sites/assets/apexaiassistant/js
cp apps/apexaiassistant/apexaiassistant/public/css/* sites/assets/apexaiassistant/css/
cp apps/apexaiassistant/apexaiassistant/public/js/* sites/assets/apexaiassistant/js/
bench --site client-site.com clear-cache
```

### Step 6 — Restart the bench

```bash
sudo supervisorctl restart all
```

---

## 3. Initial Configuration

After installation, open the client's ERPNext site in a browser as **Administrator**.

### Navigate to Settings

1. Press `/` or `Ctrl + G` to open the awesome bar
2. Search for `ApexAiAssistant Settings` and open it
3. Or navigate to: `ApexAiAssistant` workspace → **AI Settings** shortcut

### Settings Overview

| Field | Description | Default |
|---|---|---|
| **AI Provider** | Choose from: OpenAI, Anthropic, Ollama, DeepSeek | `OpenAI` |
| **API Key** | The provider's secret API key | *(empty)* |
| **API Endpoint URL** | Required for Ollama; optional for DeepSeek | *(empty)* |
| **AI Model** | Model identifier string | `gpt-4o` |
| **Enable Audit Log** | Log all AI actions to the audit table | `✓ Enabled` |
| **Max Tokens** | Maximum response token length | `4000` |
| **Enabled Modules** | List of ERPNext modules the AI can access | *(set up below)* |

---

## 4. AI Provider Setup

### 4.1 — OpenAI (Recommended for most clients)

**Settings:**
| Field | Value |
|---|---|
| AI Provider | `OpenAI` |
| API Key | `sk-proj-xxxxx...` (from platform.openai.com) |
| API Endpoint URL | *(leave blank)* |
| AI Model | `gpt-4o` *(best)* or `gpt-4o-mini` *(cheaper)* |

**Getting an API Key:**
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Log in → click **API Keys** in the left sidebar
3. Click **+ Create new secret key**
4. Copy the key immediately (it won't be shown again)
5. Ensure the account has **billing enabled** with a credit balance

**Estimated Costs:**
| Model | Cost per Query (approx.) |
|---|---|
| gpt-4o | ~$0.01–0.03 |
| gpt-4o-mini | ~$0.001–0.003 |

> [!TIP]
> Recommend `gpt-4o-mini` for clients focused on cost savings, or `gpt-4o` for the best accuracy and data interpretation quality.

---

### 4.2 — Anthropic (Claude)

**Settings:**
| Field | Value |
|---|---|
| AI Provider | `Anthropic` |
| API Key | `sk-ant-xxxxx...` (from console.anthropic.com) |
| API Endpoint URL | *(leave blank)* |
| AI Model | `claude-3-5-sonnet-20241022` |

**Getting an API Key:**
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Navigate to **API Keys** and create a new key
3. Ensure workspace has credits

---

### 4.3 — Ollama (Self-Hosted / On-Premise)

Best for clients who cannot send data to external APIs for compliance reasons.

**Settings:**
| Field | Value |
|---|---|
| AI Provider | `Ollama` |
| API Key | *(leave blank)* |
| API Endpoint URL | `http://localhost:11434/v1` |
| AI Model | `llama3.1` *(or any installed model)* |

**Server Setup (Ollama):**
```bash
# Install Ollama on the same server
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (run on the server)
ollama pull llama3.1
ollama pull mistral

# Start the service
systemctl start ollama
```

> [!NOTE]
> Ollama requires the server to have at least 8GB RAM for smaller models (7B parameters) and 16–32GB for larger models (13B–70B). Confirm the client server specs first.

---

### 4.4 — DeepSeek

**Settings:**
| Field | Value |
|---|---|
| AI Provider | `DeepSeek` |
| API Key | *(from platform.deepseek.com)* |
| API Endpoint URL | `https://api.deepseek.com` |
| AI Model | `deepseek-chat` |

---

## 5. Enabling Modules

In **ApexAiAssistant Settings**, scroll to the **Enabled Modules** section. Add a row for each ERPNext module the client wants the AI to have access to.

### Available Modules

| Module Name | Description |
|---|---|
| `CRM` | Leads, Opportunities, Customers, Competitors |
| `Selling` | Sales Orders, Quotations, Delivery Notes |
| `Buying` | Purchase Orders, Supplier Quotations |
| `Stock` | Inventory, Stock Entries, Item Levels |
| `Accounting` | GL Entries, Payment Entries, Invoices |
| `HR` | Employees, Leave Applications, Attendance |
| `Payroll` | Salary Structures, Payslips, Payroll Entries |
| `Projects` | Projects, Tasks, Timesheets |
| `Support` | Issues, Service Level Agreements |
| `Manufacturing` | Work Orders, BOMs, Production Plans |
| `Assets` | Assets, Maintenance Schedules |
| `Quality` | Quality Inspections, Non-Conformances |
| `Maintenance` | Maintenance Visits, Schedules |

### Recommendation by Client Type

| Client Type | Suggested Modules |
|---|---|
| Trading Company | CRM, Selling, Buying, Stock, Accounting |
| Service Company | CRM, Selling, Projects, Support, Accounting, HR |
| Manufacturing | Selling, Buying, Stock, Manufacturing, Accounting |
| HR-Focused | HR, Payroll, Projects |
| Full ERP | All modules |

> [!IMPORTANT]
> Only enable modules the client's ERPNext instance actually has installed and active. Enabling an uninstalled module will cause the AI to report errors when queried on that topic.

---

## 6. Action Registry Setup

The **Action Registry** controls exactly what operations the AI is allowed to perform. Default actions are registered automatically during installation.

### Accessing the Registry

`ApexAiAssistant` workspace → **Action Registry** → or search `ApexAiAssistant Action Registry`

### Understanding Action Categories

| Category | Description | Confirmation Required? |
|---|---|---|
| `QUERY` | Read-only data queries (list, count, fetch) | No |
| `CREATE` | Creates new draft records | No (review recommended) |
| `DRAFT` | Prepares draft documents for review | No |
| `APPROVE` | Approves or submits documents | Yes — always |
| `POST` | Posts financial entries | Yes — always |
| `EXECUTE_PAYROLL` | Runs payroll operations | Yes — always |

### Key Settings Per Action

| Field | Description |
|---|---|
| **Action Name** | Unique identifier used by the AI |
| **Action Category** | Type of operation (see above) |
| **Module** | Which ERPNext module this action belongs to |
| **Enabled** | Toggle to enable/disable individual actions |
| **Requires Confirmation** | Force user to confirm before execution |
| **Risk Level** | Low / Medium / High / Critical |
| **Allowed Roles** | ERPNext roles permitted to use this action |
| **Handler Function** | Python dotted path to the function |

### Configuring Role-Based Access

For each action, click into **Allowed Roles** and add the ERPNext roles that should have access. Examples:

| Action | Suggested Roles |
|---|---|
| `get_sales_orders` | Sales User, Sales Manager, System Manager |
| `create_sales_order` | Sales User, Sales Manager |
| `approve_payment` | Accounts Manager, System Manager |
| `execute_payroll` | HR Manager, System Manager |

> [!WARNING]
> Never assign `APPROVE`, `POST`, or `EXECUTE_PAYROLL` category actions to basic/untrusted roles. These have real financial consequences.

---

## 7. User Roles and Permissions

ApexAiAssistant inherits ERPNext's role system. The AI **will not** show data or perform actions that the user does not have ERPNext permission for.

### Setting Up Who Can Use the AI Chat

By default, all ERPNext users with the **Employee Self Service** role or higher can access the chat interface. To restrict access:

1. Go to **Role Permission Manager** in ERPNext
2. Search for `AI Conversation` DocType
3. Add or remove roles as needed

### Recommended Role Configuration

| Role | Chat Access | Query Actions | Draft Actions | Approve/Post Actions |
|---|---|---|---|---|
| All / Guest | ❌ | ❌ | ❌ | ❌ |
| Employee | ✅ | Limited | ❌ | ❌ |
| Sales User | ✅ | Sales + CRM | Sales | ❌ |
| Accounts User | ✅ | Accounting | ❌ | ❌ |
| Accounts Manager | ✅ | Accounting | Accounting | ✅ |
| HR Manager | ✅ | HR + Payroll | HR | Payroll |
| System Manager | ✅ | All | All | All |

---

## 8. Verifying the Installation

### 8.1 — Check the App is Installed

```bash
bench --site client-site.com list-apps
# Expected output includes: apexaiassistant
```

### 8.2 — Verify Assets are Loaded

In the client's browser (logged in as any user):
1. Open Developer Tools → **Network** tab
2. Reload the page (`Ctrl+Shift+R`)
3. Search for `apexaiassistant` — confirm `apexaiassistant.css` and `apexaiassistant.bundle.js` load with status `200`

### 8.3 — Check the Chat Icon

- The chat icon (💬 message-circle icon) should appear in the **top navbar** next to the search bar
- Clicking it should open the AI Chat panel on the right side

### 8.4 — Send a Test Message

Once the chat panel is open, send a simple test:
```
"Hello, are you working?"
```
Expected response: A greeting from the AI confirming it's active.

```
"Show me the top 5 customers by total sales this year"
```
Expected response: A formatted table with customer names and sales figures.

### 8.5 — Check the Audit Log

1. Navigate to `ApexAiAssistant` workspace → **Audit Log**
2. Confirm entries are being created for each AI interaction

### 8.6 — Verify Settings Page is Accessible

Search for `ApexAiAssistant Settings` — confirm the form opens and reflects the saved API key and provider.

---

## 9. Troubleshooting

### ❌ Chat icon not showing

```bash
# Re-copy assets and clear cache
cp -r apps/apexaiassistant/apexaiassistant/public/* sites/assets/apexaiassistant/
bench --site client-site.com clear-cache
sudo supervisorctl restart all
```

Then hard refresh the browser: `Ctrl+Shift+R`

---

### ❌ "No module named 'litellm'"

```bash
./env/bin/pip install litellm
sudo supervisorctl restart all
```

---

### ❌ "App apexaiassistant not in apps.txt"

This happens when `bench get-app` fails during the build step. Fix:
```bash
printf "\napexaiassistant" >> sites/apps.txt
bench --site client-site.com install-app apexaiassistant
```

---

### ❌ "OpenAI API Error" / Chat not responding

1. Go to **ApexAiAssistant Settings** → verify the API key is correct
2. Check the API provider account has active credits/billing
3. Try switching to `gpt-4o-mini` if rate-limited on `gpt-4o`
4. Check the error in: `bench --site client-site.com logs`

---

### ❌ AI Workspace content area is empty

The workspace needs to be reset from the database:

```bash
bench --site client-site.com execute "
import frappe
frappe.delete_doc('Workspace', 'ApexAiAssistant', force=True, ignore_permissions=True)
frappe.db.commit()
"
bench --site client-site.com import-doc apps/apexaiassistant/apexaiassistant/apexaiassistant/workspace/apexaiassistant/apexaiassistant.json
bench --site client-site.com clear-cache
```

---

### ❌ Duplicate workspace menus in sidebar

```bash
bench --site client-site.com execute "
import frappe
frappe.delete_doc('Workspace', 'Apex AI', force=True, ignore_permissions=True)
frappe.db.commit()
"
bench --site client-site.com clear-cache
```

---

### ❌ Actions not registering after install

Run migrate to trigger the `after_migrate` hook which registers default actions:

```bash
bench --site client-site.com migrate
```

---

### ❌ "Duplicate entry" error during install

This means a partial installation exists. Use `--force`:

```bash
bench --site client-site.com install-app apexaiassistant --force
```

---

## 10. Uninstalling the App

To completely remove ApexAiAssistant from a client site:

```bash
# Step 1: Uninstall from site (removes all data)
bench --site client-site.com uninstall-app apexaiassistant --yes

# Step 2: Remove from bench
bench remove-app apexaiassistant --force

# Step 3: Clean up files
rm -rf apps/apexaiassistant
rm -rf sites/assets/apexaiassistant

# Step 4: Restart
sudo supervisorctl restart all
```

> [!CAUTION]
> Uninstalling the app **permanently deletes** all chat history, AI conversation sessions, action registry entries, and audit logs from the database. Ensure the client has been informed and data has been exported if needed before proceeding.

---

## Support Contact

For escalation or technical assistance:

- **Email:** info@apexlogicsoftware.com
- **GitHub:** [https://github.com/Apexlogic-Technology/apexaiassistant](https://github.com/Apexlogic-Technology/apexaiassistant)
- **Version:** 0.0.1

---

*Last Updated: March 2026 — Apexlogic Technology*
