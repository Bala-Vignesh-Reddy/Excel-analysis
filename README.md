# Excel Analysis

I have a excel file in which there are link to the resume of the persons.. For analysis of that will be very complicated and tedious work to do.. 

To overcome this.. i have used gemini in which i have extracted pdf and according to the prompt it adds the result in the excel file.

## Generate Gemini API key and create a env file
.env - file
```bash
GEMINI_API_KEY="<your api key>"
```

## Install uv
```bash
pip install uv
```

## Install the dependencies
```bash
uv sync
```

## Execute the code
```bash
uv run hello.py
```
