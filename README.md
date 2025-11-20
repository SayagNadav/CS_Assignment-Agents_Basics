**📦 LLM Multi-Tool Agent System (Assignment 3)**

This project implements a multi-step function-calling agent powered by an LLM.

The agent dynamically selects and executes tools to solve complex queries involving text files, CSV analysis, internet lookup and automatic Python program generation.

It demonstrates advanced skills in:

LLM orchestration

Tool-driven agent design

Prompt engineering

Automated CSV analysis

Dynamic code generation

Program debugging & self-correction

Structured logging

Environment variable management

**It is designed as an academic exercise, but fully functional.**

**🚀 Main Feature – Autonomous Agent Loop**

**The agent:**

Loads an input.json containing the task and resources

Starts a conversation with an LLM

Lets the LLM choose tools step-by-step

Executes those tools

Appends outputs back into the reasoning loop

Terminates when the query is solved or limits are reached

**🔧 Tools Implemented**

extract_entities_from_file(file_name, entity_type)
Extracts entities (e.g., cities, people, organizations) from unstructured text using the LLM.

internet_search_attribute(entity, attribute)
Performs an internet search (via SerpAPI) and uses the LLM to extract structured JSON results.

gen_plot_prog(plot_request, input_file, columns, output_program_file, output_png)
Generates a complete Python script that:

Reads a CSV

Computes requested metrics

Generates a matplotlib plot

Saves it as a .png

Does not call plt.show(), ensuring the program terminates

execute_Python_prog(program_file)
Runs generated code and returns either "Program executed successfully" or stderr errors.

debug_and_regenerate_prog(program_file, errors, …)
Reads the error output, reflects on it and regenerates a corrected Python script.

write_file(content, filename)
Writes JSON or other outputs as required by each query.

**📋 Logging**

Every tool call logs:

Entry

All parameters (truncated to 50 chars)

Exit

Each query generates a log file:

<query_name>.log

**📁 Repository Structure**

Core files:

hw3.py                       # Full agent + tools implementation

requirements.txt             # Python dependencies

README.md                    # Project documentation (this file)


Example flow files:

input.json                   # Example agent input wiring a query to a CSV resource

WHR.txt                      # Natural-language query for the example

World-happiness-report-2024.csv   # Sample dataset used in the example

happiness_plot_program.py    # Example Python program that plots the data

happiness_plot.png           # Resulting plot generated from the dataset


input.json describes a query named WHR.txt and declares World-happiness-report-2024.csv as the CSV resource the agent can use. 

input

WHR.txt contains the natural-language task: create a program that plots the happiness scores of the top 5 and lowest 5 countries plus the overall average, then execute it. 

WHR

happiness_plot_program.py is an example of a plotting script that reads the happiness CSV, computes top/bottom 5 and the average score, and saves the plot as happiness_plot.png. 

happiness_plot_program

happiness_plot.png is the generated visualization showing the ladder scores for the top 5 and bottom 5 countries and a bar for the overall average (with a dashed horizontal line at the average value).

happiness_plot_program


**⚠️ Note**

The original assignment PDF is not included in this repository to avoid redistribution of restricted materials.

**🔐 Environment Variables**

Create a .env file locally (NOT committed to GitHub):

CLASS_OPENAI_API_KEY=your_key

SUBSCRIPTION_OPENAI_ENDPOINT_4o=your_endpoint

SERPAPI_API_KEY=your_serpapi_key


The application automatically loads them via python-dotenv.

**▶️ Running the Agent**

Prepare an input.json in the working directory describing:

The query file (e.g., WHR.txt)

Available resources (CSV, TXT, PNG, etc.)

Run:

python hw3.py


Depending on the query, outputs may include:

JSON files

PNG plot files (such as happiness_plot.png)

Generated Python programs

Log files (*.log)