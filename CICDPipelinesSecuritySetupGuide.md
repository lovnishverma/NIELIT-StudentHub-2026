# CI/CD Pipeline & Security Setup Guide

Since the NIELIT StudentHub is a **serverless, client-side application** hosted on GitHub Pages, there is a crucial distinction between "hiding" credentials from the **public repository** and "hiding" them from the **browser**.

### The Reality of Client-Side Apps
Because the site runs entirely in the user's browser (HTML/JS), **you cannot hide these credentials from the browser**. Any URL or key required to fetch data *must* be sent to the client. A user can always see them by pressing `F12` (DevTools) -> Network.

**However**, you **CAN** and **SHOULD** hide them from your public GitHub source code to prevent bots from scraping your keys or people cloning your repo with your credentials.

---

## Phase 1: Refactor Code to Extract Secrets

First, remove the hardcoded credentials from your HTML files (`index.html`, `feed.html`, `project.html`, etc.) and place them in a central configuration file.

### 1. Create a Configuration File
Create a new file named `config.js` in your root folder. This file will hold your keys locally but will be ignored by Git.

```javascript
// config.js
const CONFIG = {
    SHEET_URL: 'YOUR_ACTUAL_SHEET_URL',
    CLOUDINARY_NAME: 'YOUR_CLOUD_NAME',
    CLOUDINARY_PRESET: 'studenthub_preset'
};

```

### 2. Update HTML Files

In every HTML file where you currently define `const SHEET_URL = ...`, replace those lines with a reference to the config file.

**Add this BEFORE your main script logic:**

```html
<script src="config.js"></script>

<script>
    // Update your existing code to use the global CONFIG object
    const SHEET_URL = CONFIG.SHEET_URL;
    const CLOUDINARY_NAME = CONFIG.CLOUDINARY_NAME;
    const CLOUDINARY_PRESET = CONFIG.CLOUDINARY_PRESET;

    // ... rest of your application logic ...
</script>

```

### 3. Update `.gitignore`

Create or edit the `.gitignore` file in your repository root and add the following line. This ensures your local `config.js` (containing real keys) is never pushed to GitHub.

```text
config.js

```

---

## Phase 2: Configure GitHub Secrets

Since `config.js` is ignored, we need a way to inject these values when GitHub builds your site.

1. Go to your GitHub Repository.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret** and add the following secrets:
* `APP_SHEET_URL` (Paste your Google Script Web App URL)
* `APP_CLOUD_NAME` (Paste your Cloudinary Cloud Name)
* `APP_CLOUD_PRESET` (Paste your Upload Preset Name)



---

## Phase 3: Create a Deployment Workflow

We will use GitHub Actions to generate the `config.js` file dynamically during the deployment process using the secrets configured above.

1. In your repo, create this directory path: `.github/workflows/`
2. Create a file named `deploy.yml` inside it with the following content:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"] # Change to "master" if that is your default branch

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # This step creates the config.js file on the build server using your Secrets
      - name: Inject Configuration
        run: |
          echo "const CONFIG = {" > config.js
          echo "    SHEET_URL: '${{ secrets.APP_SHEET_URL }}'," >> config.js
          echo "    CLOUDINARY_NAME: '${{ secrets.APP_CLOUD_NAME }}'," >> config.js
          echo "    CLOUDINARY_PRESET: '${{ secrets.APP_CLOUD_PRESET }}'" >> config.js
          echo "};" >> config.js

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

```

### Finalize GitHub Settings

1. Go to **Settings** > **Pages**.
2. Change "Source" from "Deploy from a branch" to **"GitHub Actions"**.

**Result:** When you push code, GitHub Actions will create `config.js` on the fly using your hidden secrets and deploy the site. Your source code will never show the keys.

---

## Phase 4: Security Hardening (The "Real" Security)

Since the browser *can* still see these keys, you must secure the *services* themselves to reject unauthorized use.

### 1. Lock Down Cloudinary

This prevents other websites from taking your keys and using your storage quota.

1. Log in to [Cloudinary](https://cloudinary.com).
2. Go to **Settings (Gear Icon)** > **Upload**.
3. Scroll to **Upload presets** and edit your `studenthub_preset`.
4. Find **Allowed HTTP Referrers**.
5. Enter your domain: `nielitropar.github.io` (and `localhost` for testing).
6. **Save**. Now, even if someone steals your Cloud Name, they cannot upload images from their own site.

### 2. Protect Google Apps Script

Google Apps Script Web Apps set to "Anyone" are public. To add a layer of protection against bots:

1. **Generate a Secret Token:** Create a random string (e.g., `NIELIT_APP_TOKEN_2026`).
2. **Add it to Secrets:** Add `APP_SECRET_TOKEN` to your GitHub Secrets and your local `config.js`.
3. **Update Frontend (`config.js` & Fetch calls):**
```javascript
// In config.js/Secrets injection
const CONFIG = {
    // ... other keys
    APP_TOKEN: 'NIELIT_APP_TOKEN_2026' 
};

// In your fetch calls
fetch(`${SHEET_URL}?action=getProjects&token=${CONFIG.APP_TOKEN}...`)

```


4. **Update Backend (`google-apps-script.js`):**
Add a check at the very top of `handleRequest`:
```javascript
function handleRequest(e, method) {
  // Security Check
  const validToken = 'NIELIT_APP_TOKEN_2026'; // Should match your frontend token
  const incomingToken = e.parameter.token;

  if (incomingToken !== validToken) {
     return createResponse('error', 'Unauthorized Access');
  }
  // ... rest of code
}

```
