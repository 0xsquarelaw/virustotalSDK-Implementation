### First Setup Python Virtual Environment

`python -m venv .venv`

## Requirements

`pip install "fastapi[standard]" python-dotenv vt-py`

## To Run

cd backend

#### Window PowerShell command (activate venv)

```Powershell
cd ".venv\Scripts\" ; .\Activate.ps1; cd "../../"; clear
```

To deactivate:

- `deactivate`

## Run Backend Server

- `fastapi dev main.py`

## Run Frontend Server

cd frontend

- `python -m http.server 3000`

## References

https://shreshtait.com/blog/2024/01/what-are-newly-registered-domain-names/

https://github.com/shreshta-labs/newly-registered-domains

https://github.com/VirusTotal/vt-py

### Additional commands

- `git archive -o output.zip master`

## Note:

i m not implemeted premium features of vt-py
