python -m venv mycustompython

cd "mycustompython\Scripts\" ; .\Activate.ps1; cd "../../"; clear
`to deactivate env` deactivate

pip install "fastapi[standard]" python-dotenv vt-py
