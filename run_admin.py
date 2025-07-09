# run_admin.py

import uvicorn
from admin.app import create_admin_app

app = create_admin_app()

if __name__ == "__main__":
    uvicorn.run("run_admin:app", host="0.0.0.0", port=8000, reload=True)
