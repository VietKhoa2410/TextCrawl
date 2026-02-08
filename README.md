# Desciption
Quick script for crawl text from a specific web and save it to a single file.

# Run

Create file `.env.
```
BASE_URL=https://******/
START_FROM_PAGE=
END_AT_PAGE=
SAVE_FILE_NAME=
```

Start script
```
uv sync
npm init playwright@latest --yes "--" . '--quiet' '--browser=chromium' '--lang=js'
uv run main.py
```