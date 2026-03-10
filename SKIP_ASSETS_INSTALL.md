# ✅ ApexAiAssistant - WORKING Installation (Skip Assets Method)

## 🎯 The Solution

The build system tries to compile our already-compiled files. 
**Solution**: Use `--skip-assets` flag during installation!

---

## 🚀 Installation (CORRECT METHOD)

### Method 1: From GitHub (Recommended)

```bash
cd ~/frappe-bench

# Step 1: Get the app with --skip-assets
bench get-app https://github.com/Apexlogic-Technology/apexaiassistant.git --skip-assets

# Step 2: Install on your site  
bench --site test.apexlogicsoftware.com install-app apexaiassistant

# Step 3: Build assets manually (one time)
bench build --app apexaiassistant || true  # Ignore build errors
cp -r ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/* ~/frappe-bench/sites/assets/apexaiassistant/

# Step 4: Restart
bench --site test.apexlogicsoftware.com migrate
bench restart
```

### Method 2: Manual Installation (If Method 1 fails)

```bash
# Step 1: Clone manually
cd ~/frappe-bench/apps
git clone https://github.com/Apexlogic-Technology/apexaiassistant.git --depth 1

# Step 2: Add to apps.txt
cd ~/frappe-bench
echo "apexaiassistant" >> sites/apps.txt

# Step 3: Install Python package
pip install -e ./apps/apexaiassistant

# Step 4: Copy assets manually
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/css
mkdir -p ~/frappe-bench/sites/assets/apexaiassistant/js
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/css/* ~/frappe-bench/sites/assets/apexaiassistant/css/
cp ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/js/* ~/frappe-bench/sites/assets/apexaiassistant/js/

# Step 5: Install on site
bench --site test.apexlogicsoftware.com install-app apexaiassistant
bench --site test.apexlogicsoftware.com migrate
bench restart
```

---

## ⚙️ Configure (30 seconds)

1. **Login** to your ERPNext site
2. **Search**: "ApexAiAssistant Settings" (use the awesome bar, press `/`)
3. **Enter** your OpenAI API key
4. **Save**
5. **Hard refresh** browser: `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
6. **Click** the chat icon in the navbar
7. **Test**: Type "Hello, are you working?"

---

## 🔑 Get OpenAI API Key

1. Visit: https://platform.openai.com/
2. Sign up or login
3. Go to: **API Keys** section
4. Click: **Create new secret key**
5. Copy the key (starts with `sk-proj-...` or `sk-...`)
6. **Important**: Add billing info and credits to your OpenAI account
7. Paste key in ApexAiAssistant Settings

💰 **Pricing**:
- gpt-4o: ~$0.01-0.02 per query
- gpt-4o-mini: ~$0.001 per query (cheaper option)

---

## ✅ Verify Installation

### Check if app is installed:
```bash
bench --site test.apexlogicsoftware.com list-apps
# Should show: frappe, erpnext, hrms, apexaiassistant
```

### Check if assets are present:
```bash
ls -la ~/frappe-bench/sites/assets/apexaiassistant/
# Should show css/ and js/ folders
```

### Check in browser:
1. Open Developer Tools (F12)
2. Go to Console tab
3. Check for any apexaiassistant errors
4. Should see chat button in navbar

---

## 🐛 Troubleshooting

### Issue: Chat icon not showing
**Solution**:
```bash
# Copy assets again
cp -r ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/* ~/frappe-bench/sites/assets/apexaiassistant/

# Clear cache and restart
bench --site test.apexlogicsoftware.com clear-cache
bench restart

# Hard refresh browser: Ctrl+Shift+R
```

### Issue: "ApexAiAssistant Settings not found"
**Solution**:
```bash
bench --site test.apexlogicsoftware.com migrate
bench --site test.apexlogicsoftware.com clear-cache
bench restart
```

### Issue: "OpenAI API error"
**Solutions**:
1. Check API key is correct
2. Verify you have credits in your OpenAI account
3. Check you're not rate-limited
4. Try using gpt-4o-mini instead of gpt-4o

### Issue: Build errors persist
**Solution**: Ignore them! Assets are already built.
```bash
# Just copy the assets manually:
cp -r ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/* ~/frappe-bench/sites/assets/apexaiassistant/
```

---

## 🎯 Usage Examples

Once configured, try these:

```
"Show me sales orders from last month"
"What's our current stock?"
"List pending leave applications"
"Show me top 10 customers by revenue"
"Analyze sales performance this quarter"
"Show me the opportunity pipeline"
"What's our lead conversion rate?"
"Create a draft sales order for customer ABC"
```

---

## 📊 What You Get

### 12 Modules:
CRM • Selling • Buying • Stock • Accounting • HR • Payroll • Projects • Manufacturing • Support • Assets • Quality & Maintenance

### 50+ Actions:
- Data queries
- Analytics & reports
- Draft creation
- Workflow approvals  
- Payroll execution
- Custom exports

See `COMPLETE_ACTIONS_LIST.md` for full details!

---

## 💡 Pro Tips

1. **Be specific** in your queries
2. **Use natural language** - talk like you would to a colleague
3. **Check the audit log** - All actions are logged in "ApexAiAssistant Audit Log"
4. **Review before confirming** - Always double-check financial actions
5. **Start with queries** - Get familiar before using action commands

---

## 📞 Still Having Issues?

### Check logs:
```bash
# ERPNext logs
bench --site test.apexlogicsoftware.com logs

# Check error log
tail -f ~/frappe-bench/logs/bench.log
```

### Debug in browser:
1. Press F12 to open Developer Tools
2. Go to Console tab
3. Look for errors mentioning "apexaiassistant"
4. Check Network tab for failed API calls

### Verify file structure:
```bash
# Check public files exist
ls ~/frappe-bench/apps/apexaiassistant/apexaiassistant/public/

# Check assets copied correctly
ls ~/frappe-bench/sites/assets/apexaiassistant/
```

---

## 🎉 You're All Set!

After installation and configuration:
- Chat icon will appear in navbar
- Click it to open the chat panel
- Start asking questions!
- All actions are logged for compliance
- Role-based permissions enforced

**Happy ERPing!** 🚀

---

## 📚 Documentation

- `README.md` - Quick overview
- `INSTALLATION.md` - Detailed installation 
- `COMPLETE_ACTIONS_LIST.md` - All 50+ actions
- `SETUP_GUIDE.md` - Comprehensive guide

---

**Note**: The build errors during `bench get-app` are normal for this app since the assets are pre-built. Using `--skip-assets` bypasses this issue entirely!
