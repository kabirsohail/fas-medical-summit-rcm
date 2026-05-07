# DEPLOY THIS WEEK — Step-by-step Netlify guide

**Goal:** Get the FAS website live on a real URL today, in about 1 hour, free, without any technical skills.

**What you'll have at the end:** A working URL like `fas-medical.netlify.app` you can share with FAS owners as proof of what you built.

**This does NOT include WordPress.** That's Step 2 (next week). For now we just want it LIVE somewhere.

---

## Before you start — what you need

1. ✅ The `fas-website` folder (unzipped from `fas-website.zip`)
2. ✅ An email address you can check
3. ✅ ~1 hour
4. ✅ A laptop (Mac or PC, doesn't matter)

That's it. No credit card needed. No technical skills.

---

## STEP 1 — Sign up for Netlify (5 minutes)

1. Open your web browser (Safari, Chrome, whatever)
2. Go to: **https://www.netlify.com**
3. Click the **"Sign up"** button (top right)
4. Click **"Sign up with email"** (or use Google if easier)
5. Enter your email and create a password
6. Check your email for a verification link, click it
7. You're now in the Netlify dashboard

**You should see:** A mostly empty dashboard with a button that says something like "Add new site" or "Deploy manually" or a big drop zone area.

---

## STEP 2 — Deploy your site (10 minutes)

This is the magic part. Literally drag-and-drop.

1. In the Netlify dashboard, look for a section called **"Sites"** or **"Add new site"**
2. Click **"Add new site"** → **"Deploy manually"**
   - On some screens, this is just a big drop-zone that says "Drag and drop your site folder here"
3. Open Finder (Mac) or File Explorer (Windows)
4. Navigate to where you unzipped `fas-website`
5. **Drag the entire `fas-website` folder onto the Netlify drop-zone**
6. Wait 30-60 seconds. You'll see "Uploading..." then "Building..."
7. **Done.** Your site is live.

**You should see:** A page saying "Your site is live at..." with a URL like `https://gentle-cookie-12345.netlify.app`

Click that URL. Your site should load. Pinch yourself.

---

## STEP 3 — Give it a real-ish name (5 minutes)

The auto-generated URL is ugly. Fix it:

1. In the Netlify dashboard, click your site
2. Click **"Site settings"** or **"Domain management"**
3. Click **"Change site name"** (or "Options" → "Edit site name")
4. Type something like `fas-medical-summit`
5. Save
6. **Your URL is now:** `https://fas-medical-summit.netlify.app`

That's your shareable preview URL. Send it to FAS owners.

---

## STEP 4 — Make the contact forms work (15 minutes)

Right now both forms (homepage and contact page) show fake "thanks" messages but don't actually email anyone. Let's fix that with **Formspree** (free).

### 4a. Sign up for Formspree

1. Go to: **https://formspree.io**
2. Sign up with your email (free account = 50 form submissions/month, plenty)
3. Click **"+ New form"** or **"New project"**
4. Name the form: `FAS Consultation`
5. Set the email recipient: `info@fasmedicalsummitrcm.com`
6. Click create
7. You'll get an endpoint URL like: `https://formspree.io/f/abcd1234`
8. **Copy that URL.** You'll need it.

### 4b. Update the homepage form

This requires editing one HTML file. Don't panic — it's just find-and-replace.

1. On your laptop, open the `fas-website` folder
2. Right-click `index.html` → "Open With" → TextEdit (Mac) or Notepad (PC)
   - **IMPORTANT on Mac:** TextEdit might want to open it as "rich text". If you see formatting buttons, go to Format menu → "Make Plain Text" first
3. Press `Cmd+F` (Mac) or `Ctrl+F` (Windows) to open Find
4. Search for: `<form` (just those 5 characters)
5. You'll find the consultation form. Look for this part nearby:
   ```
   <form id="consultation-form"
   ```
6. Right after `<form id="consultation-form"`, you should add:
   ```
   action="https://formspree.io/f/YOUR_ID_HERE" method="POST"
   ```
   Replace `YOUR_ID_HERE` with whatever Formspree gave you.
7. So the line ends up looking like:
   ```
   <form id="consultation-form" action="https://formspree.io/f/abcd1234" method="POST">
   ```
8. Save the file (Cmd+S / Ctrl+S)

### 4c. Do the same to contact.html

Repeat steps 1-8 above but on `contact.html` in the same folder.

### 4d. Re-deploy to Netlify

1. Go back to Netlify
2. Click your site
3. Click **"Deploys"** tab
4. **Drag the `fas-website` folder onto the drop-zone again** (this updates it)
5. Wait 30 seconds for it to redeploy
6. Visit your live URL, scroll to the consultation form, fill it out, hit submit
7. Check info@fasmedicalsummitrcm.com email — submission should arrive

**If it works:** Forms are live. You're done with this step.
**If it doesn't:** Check that the `action="..."` URL is exactly what Formspree gave you, with no typos.

---

## STEP 5 — Send to FAS owners (5 minutes)

Now you have:
- ✅ A live site at a real URL
- ✅ Working contact forms
- ✅ Free hosting that doesn't expire
- ✅ Something to actually show FAS owners

Send them an email (template):

> Hi [Name],
>
> I've been working on a complete redesign of fasmedicalsummitrcm.com — focused on attracting surgical specialty practices (ASCs, anesthesiologists, pain management, etc.). It's a premium dark-navy/gold design with interactive 3D elements, custom illustrations, and a 4-step practice revenue audit tool.
>
> Preview here: **https://fas-medical-summit.netlify.app**
>
> Take a look on both desktop and mobile. The contact form is wired up and submissions go to info@fasmedicalsummitrcm.com.
>
> If you like the direction, I'd like to talk about putting this live at fasmedicalsummitrcm.com — there are a few hosting/WordPress decisions to make and I want to do this the right way.
>
> Let me know your thoughts.

---

## STEP 6 — Conversation with FAS owners

When they reply, the questions you need to ask:

1. **"Who owns the fasmedicalsummitrcm.com domain currently?"**
   - You need DNS access to point it at the new site
2. **"Do you want to replace the current site, or run a new one alongside it?"**
   - Most likely answer: replace
3. **"Where is the current site hosted? (What WordPress hosting service do you pay for?)"**
   - If they have hosting already paid for, use it = saves money
4. **"Who manages the current WordPress site? Is there a developer involved?"**
   - If yes, that person can help with migration
5. **"Do you want to keep the existing blog posts, or are we starting fresh on content?"**
   - The new site has 10 blog topics — they're placeholder titles, not real articles yet

**Their answers determine the next step.** Don't decide WordPress strategy until you know.

---

## What happens NEXT (after they reply)

Based on FAS's answers, ONE of these is the right next move:

### Scenario A: "Yes, we love it. We have WordPress hosting on [provider]. Use that."
→ You migrate to their existing WP hosting. Move to `WORDPRESS_DEPLOYMENT.md` plan.

### Scenario B: "Yes, we love it. We don't really care about WordPress, just put it live."
→ You stay on Netlify (which is what you already have). Just point the domain at Netlify. **Total cost: $0.** No WordPress needed.

### Scenario C: "We love it but we want to edit blog posts ourselves."
→ Two sub-options:
   - **Sub-option 1:** Use Netlify CMS (free, gives them an admin panel) — semi-technical to set up
   - **Sub-option 2:** Custom WP theme — needs a developer ($3K+)

### Scenario D: "We need to think about it."
→ Site stays on Netlify forever, or until they decide. Costs you nothing.

---

## What this guide does NOT cover

- ❌ Custom domain setup (`fasmedicalsummitrcm.com` pointing at your site) — wait until FAS owners give you DNS access
- ❌ WordPress conversion — covered in `WORDPRESS_DEPLOYMENT.md`, not for this week
- ❌ The `og-image.png` (social share image) — referenced in the site but doesn't exist yet. Low priority for now.

---

## Red flags / things that can go wrong

### "My site is uploaded but the navigation links don't work"
- Make sure you uploaded the whole **folder**, not just `index.html`
- Drag the `fas-website` folder, not the files inside it

### "The form doesn't email anyone"
- Verify the Formspree URL is exact: `https://formspree.io/f/YOUR_ID` (with your real ID)
- First submission requires Formspree email confirmation — check spam folder
- Make sure your file save didn't accidentally insert "smart quotes" — `action="..."` needs straight quotes, not `action=“…”`

### "The page looks weird / broken"
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+F5 (Windows). Browser cache problem.
- Try in a private/incognito window

### "Netlify says deploy failed"
- Re-zip the folder and try again
- Make sure there are no special characters in your file names

---

## Total time and cost summary

| Step | Time | Cost |
|---|---|---|
| Sign up Netlify | 5 min | $0 |
| Deploy site | 10 min | $0 |
| Rename URL | 5 min | $0 |
| Wire up forms | 15 min | $0 |
| Send to FAS owners | 5 min | $0 |
| **TOTAL** | **~40 min** | **$0** |

You'll have a real live URL by the end of today. WordPress decision can wait until you've talked to FAS owners.
