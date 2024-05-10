

### Getting started:
- Activate virtual env.
- Navigate to project root directory.
- Install dependencies if needed.  
  `pip install -r requirements.txt`
- Run the app.  
  `uvicorn main:app --reload`

A simple mock server that can mock respones based on configuration.

Language: `Python 3.12.3`
</br>
Dependencies: Dumpted in `requirements.txt`

### To run:
- Ensure availability of mentioned python version. Python virtual env can be used.
- Install dependecies.
</br>
Navigate to project root directory, then:
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
