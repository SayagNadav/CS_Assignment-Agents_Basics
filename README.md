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

**🚀 Main Feature**

**🧠 Autonomous Agent Loop**

**The agent:**

Loads a query.json containing the task and resources

Starts a conversation with an LLM

Lets the LLM choose tools step-by-step

Executes those tools

Appends outputs back into the reasoning loop

Terminates when the query is solved or limits are reached

**🔧 Tools Implemented**
1. extract_entities_from_file(file_name, entity_type)

Extracts entities (e.g., cities, people, organizations) from unstructured text using the LLM.

2. internet_search_attribute(entity, attribute)

Performs an internet search (via SerpAPI) and uses the LLM to extract structured JSON results.

3. gen_plot_prog(plot_request, input_file, columns, output_program_file, output_png)

Generates a complete Python script that:

Reads a CSV

Computes requested metrics

Generates a matplotlib plot

Saves it as a .png

Does not call plt.show(), ensuring the program terminates

4. execute_Python_prog(program_file)

Runs generated code and returns:

"Program executed successfully"

Or stderr errors

5. debug_and_regenerate_prog(program_file, errors, …)

Reads the error output, reflects on it and regenerates a corrected Python script.

6. write_file(content, filename)

Writes JSON or other outputs as required by each query.

**📋 Logging**

Every tool call logs:

Entry

All parameters (truncated)

Exit

Each query generates:

<query_name>.log

**📁 Repository Structure**

hw3.py              # Full agent + tools implementation

requirements.txt    # Python dependencies

README.md           # Project documentation (this file)


**⚠️ Note:**

The original assignment PDF is not included in this repository to avoid redistribution of restricted materials.

**🔐 Environment Variables**

Create .env locally in your machine (NOT committed to GitHub):

CLASS_OPENAI_API_KEY=your_key

SUBSCRIPTION_OPENAI_ENDPOINT_4o=your_endpoint

SERPAPI_API_KEY=your_serpapi_key


The application automatically loads them via python-dotenv.

**▶️ Running the Agent**

Prepare an input.json in the working dir describing:

The query file

Available resources (CSV, TXT, PNG, etc.)

Run:

python hw3.py


Outputs may include:

JSON files

PNG plot files

Generated Python programs

Logs

**🧪 Capabilities Demonstrated**

This project shows proficiency in:

Autonomous reasoning loops

Multi-tool function calling

Error-aware code generation

Plotting and data aggregation

Internet search parsing

File I/O automation

Environment and secrets handling

Iterative agent design

Structured logging practices

This is the type of system used for:

Data question-answering agents

Automated analysis bots

AI-enhanced ETL pipelines

Code generation / debugging assistants

**👤 Author**

Nadav Sayag
