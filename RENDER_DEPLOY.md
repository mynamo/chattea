# Deploy chattea to Render

## Step 1 — Commit & push (production changes already applied)

```bash
cd ~/Documents/Data\ Projects/chattea
git add -A
git commit -m "Make chattea production-ready"
git push
```

## Step 2 — Create the Render web service

1. Go to **render.com**, sign up / log in with GitHub.
2. **New +  →  Web Service**  →  connect the **mynamo/chattea** repo.
3. Settings (the Django project lives in the `server/` subfolder — this matters):

   | Field | Value |
   |-------|-------|
   | Root Directory | `server` |
   | Environment | `Python 3` |
   | Build Command | `./build.sh` |
   | Start Command | `gunicorn server.wsgi` |
   | Instance Type | Free |

4. Add **Environment Variables**:

   | Key | Value |
   |-----|-------|
   | `DJANGO_SECRET_KEY` | *(the key from the chat — do NOT commit it)* |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | `.onrender.com` |

5. **Create Web Service**. First build takes a few minutes.

## Step 3 — After first deploy

Render gives you a URL like `https://chattea-xxxx.onrender.com`. Add one more env var
using that exact URL, then let it redeploy:

   | Key | Value |
   |-----|-------|
   | `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://chattea-xxxx.onrender.com` |

## Notes

- Free tier **sleeps** after 15 min idle (~30s cold start on next visit).
- The SQLite DB **resets on each deploy** (Render's free disk is ephemeral) — fine for a
  demo; add Render PostgreSQL later if you want chat data to persist.
- Every `git push` auto-redeploys, just like your Streamlit apps.
