# Push DocsPilot to GitHub

## Quick Deploy (5 minutes)

### Step 1: Push to GitHub

```bash
git push origin main
```

This will trigger the GitHub Actions workflow automatically.

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/Yash-Kalkhambkar/DocsPilot/settings/pages
2. Under "Source", select: **Deploy from a branch**
3. Branch: **gh-pages** (will be created by CI)
4. Folder: **/ (root)**
5. Click **Save**

### Step 3: Wait for Deployment

1. Go to: https://github.com/Yash-Kalkhambkar/DocsPilot/actions
2. Wait for "Documentation Pipeline" workflow to complete (~2-3 minutes)
3. Look for green checkmark ✅

### Step 4: Visit Your Live Site

Once deployed, visit:
**https://yash-kalkhambkar.github.io/DocsPilot/**

## What the CI Pipeline Does

On every push to `main`:

1. ✅ Validates metadata (all topics have correct front matter)
2. ✅ Checks links (internal and external)
3. ✅ Runs Vale linting (style and terminology)
4. ✅ Runs pytest tests (18 tests)
5. ✅ Builds MkDocs site (strict mode)
6. ✅ Deploys to GitHub Pages (gh-pages branch)

## If CI Fails

### Metadata Errors

Run locally to debug:
```bash
python scripts/validate_metadata.py
```

Fix any missing or invalid front matter.

### Link Errors

Run locally to debug:
```bash
python scripts/check_links.py
```

Fix broken internal links or dead external URLs.

### Vale Errors

Install Vale and run:
```bash
vale docs/
```

Fix terminology or style violations.

### Test Failures

Run locally to debug:
```bash
pytest tests/ -v
```

Check test output for specific failures.

### MkDocs Build Errors

Run locally to debug:
```bash
mkdocs build --strict
```

Fix any broken links or invalid markdown.

## Make Repository Public

Before submitting for portfolio review:

1. Go to: https://github.com/Yash-Kalkhambkar/DocsPilot/settings
2. Scroll to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Public"
5. Type repository name: `DocsPilot`
6. Confirm

## Update README Badge

After first successful CI run, the badge will show status:

```markdown
![CI Status](https://github.com/Yash-Kalkhambkar/DocsPilot/workflows/Documentation%20Pipeline/badge.svg)
```

Badge colors:
- 🟢 Green: CI passing
- 🔴 Red: CI failing
- ⚪ Gray: No runs yet

## Local Preview (Optional)

Before pushing, preview locally:

```bash
mkdocs serve
```

Visit: http://127.0.0.1:8000

Press Ctrl+C to stop.

## Troubleshooting

### "gh-pages branch not found"

Wait for first CI run to complete. The workflow creates this branch automatically.

### "Permission denied"

Make sure you're authenticated:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Failed to push"

If you haven't pushed yet:
```bash
git remote -v
```

Should show:
```
origin  https://github.com/Yash-Kalkhambkar/DocsPilot.git (fetch)
origin  https://github.com/Yash-Kalkhambkar/DocsPilot.git (push)
```

If remote is missing:
```bash
git remote add origin https://github.com/Yash-Kalkhambkar/DocsPilot.git
```

### "Site not loading"

1. Check GitHub Pages is enabled
2. Verify gh-pages branch exists
3. Wait 2-3 minutes after first deployment
4. Clear browser cache
5. Try incognito/private browsing

## After Deployment

### Update STATUS.md

Mark completed items:
- [x] CI green on main ✅
- [x] Live docs site loads ✅
- [x] Repository is public ✅

### Test the Live Site

Visit and verify:
- [ ] Home page loads
- [ ] Navigation works (Concepts, Tasks, Reference)
- [ ] Search functionality works
- [ ] Dark/light mode toggle works
- [ ] All internal links work
- [ ] Code blocks render with syntax highlighting

### Share the Link

Add to your resume/portfolio:
- **Documentation:** https://yash-kalkhambkar.github.io/DocsPilot/
- **Source Code:** https://github.com/Yash-Kalkhambkar/DocsPilot

## Timeline

- **Local testing:** ✅ Complete (100% tests pass)
- **Push to GitHub:** ~30 seconds
- **CI workflow:** ~2-3 minutes
- **GitHub Pages deployment:** ~1-2 minutes
- **Total:** ~5 minutes from push to live

## You're Ready! 🚀

Everything is tested and working. Just run:

```bash
git push origin main
```

Then enable GitHub Pages in settings, and your portfolio piece will be live!
