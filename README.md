# Code Agent

* use Google Gemini LLM to ask questions and execute code in a loop until the question is answered
* execute code in a sandboxed environment and return the output to the LLM

## Command-Line InterFace

* `python3 main.py <query>`

## Environment Variables

* `GEMINI_API_KEY`: Google Gemini API Key
* `WORKING_DIRECTORY`: sandbox where agent will operate (fallback can be set in `configuration.py`)

## Stack

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=Python&logoColor=white)
![Gemini](https://img.shields.io/badge/-Gemini-886FBF?style=flat-square&logo=googlegemini&logoColor=white)