Simple minimum server.

Language: `Python 3.12.3`
</br>
Dependencies: Dumpted in `requirements.txt`

### To run:
- Ensure availability of mentioned python version. Python virtual env can be used.
- Install dependecies.
</br>
`pip install -r requirements.txt`
- Run after navigating to `src` dir:
</br>
`uvicorn main:app`
</br>
Or, with custom params:
</br>
`uvicorn main:app --host 127.0.0.1 --port 1234 --reload`
</br>

N.B.: To run from the root dir, use `src.main:app`.
