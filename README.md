# ApexAiAssistant - AI-Powered Assistant for ERPNext

ApexAiAssistant is a role-aware AI chatbot that integrates seamlessly with ERPNext to help users query data, generate visualizations, prepare drafts, execute approved actions, and export data while respecting permissions and workflows.

## Features

- **Role-Aware**: Respects ERPNext user roles and permissions
- **Never Hallucinates**: Only provides accurate data from your ERPNext system
- **Action Registry**: Whitelisted actions ensure safe operations
- **Audit Trail**: Complete logging of all AI actions
- **Multi-Module Support**: 50+ actions across 12 modules

## Quick Installation

### Method 1: From GitHub (Recommended)

```bash
cd ~/frappe-bench

# Install with --skip-assets to avoid build errors
bench get-app https://github.com/africanwebguy/apexaiassistant.git --skip-assets

# Copy pre-built assets
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/css
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/js
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/css/* ~/frappe-bench/sites/assets/apexaiassistant/css/
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/js/* ~/frappe-bench/sites/assets/apexaiassistant/js/

# Install on your site
bench --site your-site.local install-app apexaiassistant
bench --site your-site.local migrate
bench restart
```

### Method 2: From ZIP

```bash
# Extract to apps folder
cd ~/frappe-bench/apps
unzip apexaiassistant.zip

# Add to apps.txt
cd ~/frappe-bench
echo "apexaiassistant" >> sites/apps.txt

# Install Python package
pip install -e ./apps/apexaiassistant

# Copy assets
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/css
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/js
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/css/* ~/frappe-bench/sites/assets/apexaiassistant/css/
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/js/* ~/frappe-bench/sites/assets/apexaiassistant/js/

# Install on site
bench --site your-site.local install-app apexaiassistant
bench --site your-site.local migrate
bench restart
```

## Configuration

1. Login to ERPNext
2. Search "ApexAiAssistant Settings"
3. Enter OpenAI API key
4. Save
5. Refresh browser (Ctrl+Shift+R)
6. Click chat icon!

## 50+ Actions Across 12 Modules

CRM • Selling • Buying • Stock • Accounting • HR • Payroll • Projects • Manufacturing • Support • Assets • Quality & Maintenance

See `COMPLETE_ACTIONS_LIST.md` for details.

## Troubleshooting

**Chat icon not showing:**
```bash
cp -r ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/* ~/frappe-bench/sites/assets/apexaiassistant/
bench --site your-site.local clear-cache
bench restart
```

**Build errors:** Normal! Use `--skip-assets` and copy assets manually.

## Documentation

- `SKIP_ASSETS_INSTALL.md` - Complete installation guide
- `COMPLETE_ACTIONS_LIST.md` - All actions documented

## License

MIT
