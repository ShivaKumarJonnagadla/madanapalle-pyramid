# Deploying the website

You need free accounts at **GitHub** (github.com) and **Vercel** (vercel.com).
Both the `gh` and `vercel` command-line tools are already installed on this machine.

You have two options. **Option A is the fastest** and does not even need GitHub.

---

## Option A, Deploy straight to Vercel (fastest, ~2 minutes)

```bash
cd "/Users/shivakumar.jonnagadla1/Downloads/Twitter/pyramid-site"
vercel login          # opens the browser, sign in with Google/GitHub/email
vercel                # answer the prompts (accept defaults). This makes a preview URL.
vercel --prod         # promotes it to your public production URL
```

Vercel will print a URL like `https://madanapalle-pyramid.vercel.app`. That is your live site.
To re-deploy after any edit, just run `vercel --prod` again.

---

## Option B, Put it on GitHub first, then connect Vercel

Useful if you want the code stored on GitHub and auto-deploys on every push.

```bash
cd "/Users/shivakumar.jonnagadla1/Downloads/Twitter/pyramid-site"

# 1. Sign in to GitHub
gh auth login          # choose GitHub.com → HTTPS → login with browser

# 2. Create the repo and push (the folder is already a git repo with a first commit)
gh repo create madanapalle-pyramid --public --source=. --push
```

Then either:

- Run `vercel` (as in Option A) inside the folder, **or**
- Go to https://vercel.com/new, click **Import** next to the `madanapalle-pyramid`
  repository, and click **Deploy**. Every future `git push` will redeploy automatically.

---

## After you have a live URL

1. Open the site and check the photos, videos and the UPI QR all load.
2. Confirm the account name shows **Madanapalle Pyramid Spiritual Society**.
3. Put that URL into the social-media posts (see `social-posts.md`) in place of
   `[YOUR-WEBSITE-LINK]`.

## Custom domain (optional)

In the Vercel dashboard → your project → **Settings → Domains**, you can add a name
like `madanapallepyramid.org` if you buy one. Not required, the free `.vercel.app`
address works perfectly for sharing.
