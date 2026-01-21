# NIELIT StudentHub - Complete Setup Guide

This guide will walk you through setting up NIELIT StudentHub from scratch, with detailed explanations and troubleshooting for each step.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Understanding the Architecture](#understanding-the-architecture)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### Required Accounts

1. **Google Account**
   - Needed for: Google Sheets (database) and Google Apps Script (backend)
   - Free tier sufficient
   - Sign up: [accounts.google.com](https://accounts.google.com)

2. **Cloudinary Account**
   - Needed for: Image hosting and CDN
   - Free tier: 25GB storage, 25GB bandwidth/month
   - Sign up: [cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)

3. **GitHub Account** (for deployment)
   - Needed for: Hosting via GitHub Pages
   - Free tier sufficient
   - Sign up: [github.com/join](https://github.com/join)

### Required Knowledge

**Minimum:**
- Basic understanding of HTML and JavaScript
- Ability to copy/paste code
- Basic file navigation

**Recommended:**
- Understanding of web development concepts
- Familiarity with browser DevTools (F12)
- Basic Git knowledge

### Tools Needed

1. **Text Editor**
   - Recommended: [VS Code](https://code.visualstudio.com/)
   - Alternatives: Sublime Text, Atom, Notepad++
   
2. **Web Browser**
   - Recommended: Chrome (for DevTools)
   - Also test in: Firefox, Safari, Edge

3. **Command Line** (optional, for local testing)
   - Python (for `python -m http.server`)
   - Node.js (for `npx serve`)
   - Or just double-click HTML files

---

## Understanding the Architecture

### How StudentHub Works

```
┌─────────────────────────────────────────────────────────────┐
│                   1. USER INTERACTION                       │
│              (HTML/CSS/JavaScript in Browser)               │
└──────────────────────┬──────────────────┬───────────────────┘
                       │                  │
        ┌──────────────▼──────┐  ┌────────▼──────────┐
        │   2. IMAGE UPLOAD   │  │  3. DATA REQUESTS │
        │   (to Cloudinary)   │  │  (to Apps Script) │
        └──────────────┬──────┘  └────────┬──────────┘
                       │                  │
                       │                  │
        ┌──────────────▼──────┐  ┌────────▼──────────┐
        │   Cloudinary CDN    │  │  Google Apps      │
        │   (Image Storage)   │  │     Script        │
        └─────────────────────┘  └────────┬──────────┘
                                           │
                                  ┌────────▼──────────┐
                                  │  Google Sheets    │
                                  │   (Database)      │
                                  └───────────────────┘
```

### Data Flow Example: Posting a Project

1. **User Action**: User fills project form, uploads image
2. **Image Upload**: JavaScript uploads image to Cloudinary → receives URL
3. **Data Submission**: JavaScript sends project data + image URL to Apps Script
4. **Backend Processing**: Apps Script validates data, appends to Google Sheets
5. **Response**: Success message sent back to browser
6. **UI Update**: Project appears in feed immediately

### Why This Architecture?

**Advantages:**
- ✅ **Zero Server Cost** - Google Sheets and Cloudinary free tiers
- ✅ **No Backend Coding** - Google Apps Script is JavaScript
- ✅ **Easy Maintenance** - Update via Google Sheets UI
- ✅ **Scalable** - Cloudinary CDN + Google infrastructure
- ✅ **Simple Deployment** - Static files on GitHub Pages

**Limitations:**
- ⚠️ Google Sheets quotas (20,000 rows max in free tier)
- ⚠️ Apps Script execution time (6 min max)
- ⚠️ Cloudinary bandwidth limits (25GB/month free)
- ⚠️ Not suitable for real-time features

---

## Step-by-Step Setup

### Step 1: Download/Clone the Repository

**Option A: Using Git (Recommended)**

```bash
# Clone the repository
git clone https://github.com/nielitropar/nielitropar.github.io.git

# Navigate into the directory
cd nielitropar.github.io

# Verify files
ls -la
# Should see: index.html, profiles.html, google-apps-script.js, etc.
```

**Option B: Download ZIP**

1. Go to repository: https://github.com/nielitropar/nielitropar.github.io
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract ZIP to your desired location
5. Navigate into the extracted folder

**What You Should Have:**
```
nielitropar.github.io/
├── index.html               # Main app file
├── profiles.html            # Profiles page
├── google-apps-script.js    # Backend code
├── logo.png                 # NIELIT logo
├── README.md               # Documentation
├── QUICK_REFERENCE.md      # Quick guide
├── SETUP_GUIDE.md          # This file
└── LICENSE                 # MIT License
```

---

### Step 2: Set Up Cloudinary (Image Hosting)

#### 2.1 Create Cloudinary Account

1. Go to: https://cloudinary.com/users/register/free
2. Fill in:
   - Email address
   - Password
   - Check "I agree to terms"
3. Click "Sign up"
4. Verify your email (check inbox/spam)
5. Complete any onboarding prompts

#### 2.2 Get Your Cloud Name

1. Login to Cloudinary dashboard
2. Look at the top of the page
3. You'll see: **Cloud name: your_cloud_name**
4. **Write this down** - you'll need it later

Example cloud name: `dy8up08qd` or `student-hub-cloud`

#### 2.3 Create Upload Preset

**Why?** Upload presets control how images are processed and stored.

1. **Navigate to Upload Settings**
   - Click gear icon (⚙️) in top-right
   - Select "Upload" from left sidebar
   - Scroll down to "Upload presets" section

2. **Add New Preset**
   - Click "Add upload preset" button
   - You'll see a form

3. **Configure Preset**
   Fill in these exact values:
   
   - **Preset name**: `studenthub_preset` (exact name!)
   - **Signing Mode**: **Unsigned** ⚠️ CRITICAL!
     - Click dropdown, select "Unsigned"
     - If set to "Signed", uploads will fail
   
   - **Folder**: `studenthub` (optional, for organization)
   - **Access Mode**: `Public`
   - **Unique filename**: ✅ Enable (recommended)
   - **Overwrite**: ❌ Disable (recommended)

4. **Save**
   - Click "Save" button at bottom
   - You should see your preset in the list

5. **Verify**
   - Check that preset name is exactly: `studenthub_preset`
   - Check that "Signing Mode" shows "Unsigned"

**Common Mistakes:**
- ❌ Preset name typo (must be exactly `studenthub_preset`)
- ❌ Signing Mode set to "Signed" (must be "Unsigned")
- ❌ Access Mode not public

---

### Step 3: Set Up Google Sheets Backend

#### 3.1 Create Google Sheet

1. Go to: https://sheets.google.com
2. Click "+ Blank" to create new spreadsheet
3. **Name it**: "NIELIT StudentHub Database"
   - Click on "Untitled spreadsheet" at top
   - Type the name
   - Press Enter

**At this point, your sheet is empty - that's normal!**
The Apps Script will create sheets automatically.

#### 3.2 Open Apps Script Editor

1. In your Google Sheet, click: **Extensions** → **Apps Script**
2. A new tab opens with the Apps Script editor
3. You'll see a default `myFunction()` - **delete everything**

#### 3.3 Paste Backend Code

1. Open `google-apps-script.js` from your downloaded files
2. **Copy ALL the code** (Ctrl+A, Ctrl+C)
3. **Paste** into Apps Script editor (Ctrl+V)
4. **Verify** you see:
   - Comments at top: `// STUDENTHUB - PRODUCTION BACKEND (v2.0)`
   - Functions: `doGet`, `doPost`, `login`, `signup`, etc.
   - Bottom helper functions

#### 3.4 Save the Script

1. Click **Save** icon (💾) or Ctrl+S
2. **Name your project**: "StudentHub API"
   - Click "Untitled project" at top
   - Type "StudentHub API"
   - Press Enter

#### 3.5 Deploy as Web App

This is the most important step!

1. **Start Deployment**
   - Click **Deploy** button (top right)
   - Select **New deployment**

2. **Select Type**
   - Click gear icon (⚙️) next to "Select type"
   - Choose **Web app**

3. **Configure Deployment**
   Fill in these settings:
   
   - **Description**: "StudentHub API v2.0"
   - **Execute as**: **Me** (your email)
   - **Who has access**: **Anyone** ⚠️ CRITICAL!

   **Why "Anyone"?**
   - This allows your website (running in users' browsers) to call the API
   - The script itself is still secure
   - Data in Google Sheets remains private

4. **Authorize the Script**
   - Click **Deploy**
   - A popup appears: "Authorization required"
   - Click **Authorize access**
   - Select your Google account
   - **You'll see a warning**: "Google hasn't verified this app"
     - Click **Advanced**
     - Click **Go to StudentHub API (unsafe)**
     - This is safe - it's your own script!
   - Click **Allow**

5. **Copy the Web App URL**
   - After authorization, you'll see: "Deployment successfully created"
   - **Copy the Web App URL**
   - It looks like:
     ```
     https://script.google.com/macros/s/AKfycbxXXXXXXXXXXXXXXXXX/exec
     ```
   - **Save this URL** - you'll need it next!
   - Click **Done**

**Troubleshooting Deployment:**
- If "Anyone" option is grayed out: Your Google Workspace admin may have restrictions
- If authorization fails: Clear cookies and try again
- If deployment fails: Check for syntax errors in code (red underlines)

#### 3.6 Initialize Sample Data (Optional)

This creates demo user and sample data for testing.

1. **In Apps Script editor**, find function dropdown at top
2. **Select**: `initializeSampleData`
3. **Click**: Run (▶️ play button)
4. **Wait** for execution to complete (10-30 seconds)
5. **Check logs**: View → Logs
   - Should see: "Sample data initialized"
   - Should see demo credentials listed

6. **Verify in Sheet**:
   - Go back to your Google Sheet
   - You should now see 4 tabs: Users, Projects, Profiles, Comments
   - Each should have headers and sample data

**What if it fails?**
- Check Execution log (View → Executions)
- Look for error messages
- Common issue: Sheet already initialized (safe to ignore)

---

### Step 4: Configure the Website

Now we connect everything together!

#### 4.1 Configure index.html

1. **Open** `index.html` in your text editor
2. **Press** Ctrl+F (Find) and search for: `SHEET_URL`
3. **You'll find** around line 1225:

```javascript
const SHEET_URL = 'https://script.google.com/macros/s/AKfycbzGbZ...../exec';
const CLOUDINARY_PRESET = 'studenthub_preset'; 
const CLOUDINARY_NAME = 'dy8up08qd';
```

4. **Replace** with YOUR values:

```javascript
const SHEET_URL = 'YOUR_APPS_SCRIPT_WEB_APP_URL_HERE';
const CLOUDINARY_PRESET = 'studenthub_preset';  // Keep this exact name
const CLOUDINARY_NAME = 'YOUR_CLOUDINARY_CLOUD_NAME';
```

**Example (with your actual values):**
```javascript
const SHEET_URL = 'https://script.google.com/macros/s/AKfycbyN8x.../exec';
const CLOUDINARY_PRESET = 'studenthub_preset';
const CLOUDINARY_NAME = 'student-hub-cloud';
```

5. **Save** the file (Ctrl+S)

#### 4.2 Configure profiles.html

1. **Open** `profiles.html` in your text editor
2. **Press** Ctrl+F and search for: `SHEET_URL`
3. **You'll find** around line 111:

```javascript
const SHEET_URL = 'https://script.google.com/macros/s/AKfycbzGbZ...../exec';
```

4. **Replace** with YOUR Apps Script URL (same as in index.html):

```javascript
const SHEET_URL = 'YOUR_APPS_SCRIPT_WEB_APP_URL_HERE';
```

5. **Save** the file

**⚠️ CRITICAL:** Both files must have the exact same `SHEET_URL`!

#### 4.3 Verify Configuration

**Checklist:**
- [ ] `SHEET_URL` in index.html matches your Apps Script URL
- [ ] `SHEET_URL` in profiles.html matches index.html
- [ ] `CLOUDINARY_NAME` in index.html matches your Cloud Name
- [ ] `CLOUDINARY_PRESET` is exactly `studenthub_preset` (no typos)
- [ ] Both files saved

---

## Testing

### Test 1: Local Testing (No Server)

**Simplest Method:**

1. **Double-click** `index.html`
2. It opens in your default browser
3. You should see the login page

**Test Login:**
- Email: `demo@nielit.gov.in`
- Password: `demo123`
- Click "Log In"

**If it works:** ✅ Configuration successful!
**If it fails:** See troubleshooting below

### Test 2: Local Server (Recommended)

**Why?** More realistic environment, better debugging.

**Option A: Python**
```bash
# In project directory
python -m http.server 8000
# Visit: http://localhost:8000
```

**Option B: Node.js**
```bash
# In project directory
npx serve
# Visit: http://localhost:3000
```

**Option C: VS Code**
- Install "Live Server" extension
- Right-click index.html → "Open with Live Server"

### Test 3: Feature Testing

Once logged in, test each feature:

#### Test Authentication
- [ ] Login with demo account works
- [ ] Signup creates new account
  - Try email: `test@nielit.gov.in`
  - Password: `test123`
- [ ] Logout works
- [ ] Re-login with new account works

#### Test Profile
- [ ] View sidebar profile (shows your name, avatar)
- [ ] Click "Edit Profile"
  - Upload profile picture (test Cloudinary)
  - Add bio, LinkedIn, GitHub links
  - Save changes
- [ ] Verify changes persist after reload

#### Test Projects
- [ ] Click "Post Project"
- [ ] Fill form:
  - Upload project image
  - Add title, description
  - Add GitHub link
  - Add tech stack (e.g., "React, Node.js")
- [ ] Submit
- [ ] Project appears in feed immediately
- [ ] Image displays correctly

#### Test Interactions
- [ ] Upvote a project (button should disable)
- [ ] Click comment button
- [ ] Add a comment
- [ ] Comment appears in modal
- [ ] Comment count updates on card

#### Test Search
- [ ] Search for project (by title)
- [ ] Search for project (by tech)
- [ ] Search for project (by author)
- [ ] Click "Profiles" tab
- [ ] Search for user (by name)
- [ ] Search for user (by major)

#### Test Navigation
- [ ] Click on user's name → goes to their profile
- [ ] Click "My Projects" → shows your projects
- [ ] Click "Profiles" tab → shows directory
- [ ] Click on profile card → shows portfolio
- [ ] Click "Back to Directory"

#### Test Mobile
- [ ] Open DevTools (F12)
- [ ] Toggle device toolbar (Ctrl+Shift+M)
- [ ] Test on iPhone X, iPad, Galaxy S20
- [ ] Bottom navigation appears (< 968px width)
- [ ] All features work on mobile
- [ ] Tap targets are large enough

### Troubleshooting Tests

**Login fails:**
1. Open Console (F12 → Console)
2. Look for errors
3. Check SHEET_URL is correct
4. Try API directly: `YOUR_SHEET_URL?action=getProjects` in browser

**Images don't upload:**
1. Check Console for Cloudinary errors
2. Verify CLOUDINARY_NAME is correct
3. Verify preset is "Unsigned"
4. Try smaller image (< 2MB)

**Projects don't load:**
1. Check Console for errors
2. Test API: `YOUR_SHEET_URL?action=getProjects`
3. Should return JSON (empty array or projects)
4. Check Apps Script logs (View → Executions)

---

## Deployment

### Option 1: GitHub Pages (Recommended)

#### Prerequisites
- GitHub account
- Git installed on your computer

#### Steps

**1. Initialize Git Repository (if not cloned):**
```bash
cd nielitropar.github.io
git init
```

**2. Create GitHub Repository:**
- Go to: https://github.com/new
- Repository name: `nielit-studenthub` (or any name)
- Description: "Student project showcase platform"
- Public or Private (your choice)
- **Don't** initialize with README (you have files)
- Click "Create repository"

**3. Connect Local to GitHub:**
```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Add files
git add .

# Commit
git commit -m "Initial commit - NIELIT StudentHub configured"

# Push
git branch -M main
git push -u origin main
```

**4. Enable GitHub Pages:**
- Go to repository on GitHub
- Click **Settings** tab
- Scroll to **Pages** section (left sidebar)
- Under "Source":
  - Branch: **main**
  - Folder: **/ (root)**
- Click **Save**

**5. Wait for Deployment:**
- GitHub builds your site (1-2 minutes)
- Refresh the page
- You'll see: "Your site is live at https://YOUR_USERNAME.github.io/YOUR_REPO/"

**6. Visit Your Site:**
- Click the URL
- Your StudentHub is now live!

**7. Set Up Custom Domain (Optional):**
- Buy domain (e.g., from Namecheap)
- Add CNAME record pointing to: `YOUR_USERNAME.github.io`
- In GitHub Pages settings, add your custom domain
- Enable HTTPS

### Option 2: Other Hosting

**Netlify:**
1. Drag and drop project folder to: https://app.netlify.com/drop
2. Your site is live instantly
3. Free SSL, custom domains available

**Vercel:**
```bash
npm i -g vercel
cd nielitropar.github.io
vercel
```

**Firebase Hosting:**
```bash
npm install -g firebase-tools
firebase init hosting
firebase deploy
```

**Traditional Web Hosting:**
- Upload all files via FTP
- Ensure `index.html` is in root directory
- Configure .htaccess if needed

---

## Advanced Configuration

### Customization

#### Change Colors

Edit CSS variables (both HTML files):

```css
:root {
    --primary: #003366;     /* NIELIT dark blue */
    --accent: #0066CC;      /* NIELIT light blue */
    --background: #F5F7FA;  /* Light gray background */
    --card-bg: #FFFFFF;     /* White cards */
    --text-primary: #1A1A1A; /* Almost black text */
    --text-secondary: #6B7280; /* Gray text */
    --border: #E5E7EB;      /* Light border */
}
```

#### Change Logo

Replace `logo.png` with your logo, or update these lines:

**index.html:**
- Line ~106: `<img src="logo.png" ...>`
- Line ~161: `<img src="logo.png" ...>`

**profiles.html:**
- Line ~69: `<img src="logo.png" ...>`

#### Change Fonts

1. Choose fonts: https://fonts.google.com
2. Update import (line ~6):
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap">
```
3. Update CSS:
```css
body {
    font-family: 'YourFont', sans-serif;
}
```

### Add Features

#### Add Project Categories

1. **Update Apps Script** - Add column to Projects sheet
2. **Update Post Form** - Add category dropdown
3. **Update Filter** - Filter by category
4. **Update UI** - Display category badge

#### Add Notifications

1. **Create Notifications sheet**
2. **Add API endpoint** in Apps Script
3. **Create notification component** in HTML
4. **Poll for updates** or use webhooks

#### Add Admin Panel

1. **Create admin flag** in Users sheet
2. **Add admin check** in Apps Script
3. **Create admin UI** in HTML
4. **Add moderation features**

### Security Enhancements

#### Rate Limiting

Add to Apps Script:

```javascript
function checkRateLimit(email) {
  const cache = CacheService.getScriptCache();
  const key = 'rate_' + email;
  const count = parseInt(cache.get(key) || '0');
  
  if (count > 100) {
    throw new Error('Rate limit exceeded');
  }
  
  cache.put(key, String(count + 1), 3600); // 1 hour
}
```

#### Input Validation

Already implemented in Apps Script:
- Email format validation
- Password strength checking
- HTML escaping (XSS protection)
- SQL injection prevention (N/A for Sheets)

### Monitoring

#### Apps Script Logs

1. Open Apps Script editor
2. View → Executions
3. See all API calls, errors, execution times

#### Google Analytics

Add to both HTML files (before `</head>`):

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Track events:

```javascript
gtag('event', 'login', {
  'event_category': 'engagement',
  'event_label': 'user_login'
});

gtag('event', 'post_project', {
  'event_category': 'content',
  'event_label': projectTitle
});
```

---

## Troubleshooting

See README.md for comprehensive troubleshooting guide.

**Quick Checks:**
1. ✅ SHEET_URL correct in both HTML files?
2. ✅ Apps Script deployed with "Who has access: Anyone"?
3. ✅ Cloudinary preset is "Unsigned"?
4. ✅ Browser console shows no errors?
5. ✅ API test in browser returns JSON?

**Getting Help:**
- Check browser console (F12)
- Check Apps Script logs
- Read error messages carefully
- Search README.md for specific error
- Open GitHub Issue with details

---

## Next Steps

After successful setup:

1. **Customize** - Update colors, logo, content
2. **Test Thoroughly** - All features on all devices
3. **Gather Feedback** - From first users
4. **Monitor Usage** - Check Apps Script quotas
5. **Plan Improvements** - Based on user needs
6. **Backup Regularly** - Export Google Sheet
7. **Update Documentation** - For your institution
8. **Create User Guide** - For students
9. **Set Up Support** - Email, GitHub Issues
10. **Launch!** - Announce to students

---

**Congratulations!** Your StudentHub is now set up and ready to use! 🎉

For ongoing support, refer to:
- **README.md** - Complete documentation
- **QUICK_REFERENCE.md** - Quick lookup
- **GitHub Issues** - Report bugs, request features

**Made with ❤️ at NIELIT Ropar**
