python -m venv .venv

cd ".venv\Scripts\" ; .\Activate.ps1; cd "../../"; clear
`to deactivate env` deactivate

pip install "fastapi[standard]" python-dotenv vt-py

cd backend
activate venv
`fastapi dev main.py`

cd frontend
`python -m http.server 3000`

## References

https://shreshtait.com/blog/2024/01/what-are-newly-registered-domain-names/

https://github.com/shreshta-labs/newly-registered-domains
