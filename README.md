**📦 LLM Multi-Tool Basic Agent System (CS Assignment)**

This project implements a multi-step function-calling agent powered by an LLM.
The agent dynamically selects and executes tools to solve complex queries involving text processing, CSV analysis, internet lookup and automatic Python program generation.

It demonstrates advanced skills in:

LLM orchestration

Tool-driven agent design

Prompt engineering

Automated CSV analysis

Dynamic code generation

Program debugging & self-correction

Structured logging

Environment variable management

It is designed as an academic exercise, but fully functional.

**🚀 Features**
**🧠 Autonomous Agent Loop**

**The agent:**

Loads a query.json containing the task and available resources

Initiates a conversation with an LLM

Lets the LLM choose appropriate tools step-by-step

Executes those tools

Feeds the results back into the reasoning loop

Terminates when the query is solved or limits are reached

**🔧 Tools Implemented**
1. extract_entities_from_file(file_name, entity_type)

Extracts entities (cities, people, organizations, etc.) from unstructured text using the LLM.

2. internet_search_attribute(entity, attribute)

Uses SerpAPI + LLM to extract structured JSON attributes from web search results.

3. gen_plot_prog(plot_request, input_file, columns, output_program_file, output_png)

Generates a Python script that:

Reads a CSV

Computes requested metrics

Generates a matplotlib plot

Saves it as .png

Avoids plt.show() so the program terminates cleanly

4. execute_Python_prog(program_file)

Runs generated code and returns success or stderr output.

5. debug_and_regenerate_prog(program_file, errors, …)

Reads Python errors, reflects on them and regenerates a corrected script.

6. write_file(content, filename)

Writes JSON, text, or other outputs.

**📋 Logging**

Each tool call logs:

Entering tool

All parameters (truncated to 50 chars)

Exiting tool

A log file is created per query:

<query_name>.log

📁 Repository Structure
hw3.py              # Full agent & tools implementation
requirements.txt    # Python main dependencies
README.md           # This documentation


⚠️ Note:
The original assignment description PDF is intentionally not included to avoid redistribution of restricted material.

📂 Where to Place Input Files (Important)

The agent expects input files (CSV, TXT, PNG, etc.) to exist locally in the same folder where you run hw3.py and they must be referenced inside your input.json.

Folder structure example:
project_root/

│── hw3.py

│── input.json

│── students.txt

│── grades.csv

│── happiness.csv

│── some_image.png

│── requirements.txt

│── README.md

│── .env              # Not committed to GitHub

Rules for input files:

All input resources listed in input.json must physically exist in the same directory (or a subfolder you specify).

If your input.json uses paths like "query1/World-happiness-report.csv", you must create that folder locally:

project_root/
    query1/
        World-happiness-report.csv


The program does not download files — it only uses local ones.

The agent reads the paths exactly as written in input.json.

This ensures the agent can correctly open and process every resource file.

🔐 Environment Variables

Create a .env file locally (never commit it):

CLASS_OPENAI_API_KEY=your_key
SUBSCRIPTION_OPENAI_ENDPOINT_4o=your_endpoint
SERPAPI_API_KEY=your_serpapi_key


Loaded automatically via python-dotenv.

▶️ Running the Agent

Prepare an input.json file describing:

The query file

The resource files the agent is allowed to use

Run:

python hw3.py


Depending on the query, the agent may produce:

JSON files

PNG plot files

Auto-generated Python programs

Logs (*.log)

These are saved directly to the working directory (or subfolders if specified in your query).
