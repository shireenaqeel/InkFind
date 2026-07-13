"""Dev entrypoint: `python run.py` → http://127.0.0.1:8000

Or run with autoreload: `uvicorn inkfind.main:app --reload`
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("inkfind.main:app", host="127.0.0.1", port=8000, reload=True)
