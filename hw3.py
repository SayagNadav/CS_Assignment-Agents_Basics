from openai import AzureOpenAI
import os
import sys
import json
import pandas as pd
import subprocess
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
import requests

# OpenAI API
AZURE_OPENAI_API_KEY = os.getenv('CLASS_OPENAI_API_KEY')
MODEL_4o = 'gpt-4o-mini'
OPENAI_API_VERSION_4o = '2024-08-01-preview'
AZURE_OPENAI_ENDPOINT_4o = os.getenv('SUBSCRIPTION_OPENAI_ENDPOINT_4o')

# Tools:
# Defining the tools we want gpt to use:
tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_entities_from_file",
            "description": "Extract entities of a specific type from a file. Returns a comma-separated list of all entities of that type in the file as a string in the format '[entity1, entity2, ..., entityk]'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to extract entities from"
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "The type of entities to extract (e.g., 'city', 'person', 'organization')"
                    }
                },
                "required": ["file_name", "entity_type"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "internet_search_attribute",
            "description": "Search the Internet to find a specific attribute of a given entity. Returns a JSON structure with the entity, attribute and attribute value found from search results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entity": {
                        "type": "string",
                        "description": "The entity to search for (e.g., 'Abraham Lincoln', 'Canada')"
                    },
                    "attribute": {
                        "type": "string",
                        "description": "The attribute to find for the entity (e.g., 'birthdate', 'current prime minister')"
                    }
                },
                "required": ["entity", "attribute"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gen_plot_prog",
            "description": "Generate a Python program that creates a plot based on a plot request and CSV data. The generated program will be saved to a file and the plot will be saved as a PNG. Returns the generated program.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plot_request": {
                        "type": "string",
                        "description": "A string describing the plot to be generated"
                    },
                    "input_file": {
                        "type": "string",
                        "description": "The path to the CSV file containing the data"
                    },
                    "columns": {
                        "type": "string",
                        "description": "The names of the column headers in the CSV file"
                    },
                    "output_program_file": {
                        "type": "string",
                        "description": "The file name where the generated Python program will be saved"
                    },
                    "output_png": {
                        "type": "string",
                        "description": "The file name for the output PNG plot file"
                    }
                },
                "required": ["plot_request", "input_file", "columns", "output_program_file", "output_png"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_Python_prog",
            "description": "Execute a Python program from a file. Returns 'Program executed successfully' if successful, otherwise returns error messages from stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "program_file": {
                        "type": "string",
                        "description": "The file name of the Python program to execute"
                    }
                },
                "required": ["program_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "debug_and_regenerate_prog",
            "description": "Debug a Python program that failed to execute and generate a fixed version. Takes a program file and error messages, reflects on the errors and overwrites the file with a corrected program.",
            "parameters": {
                "type": "object",
                "properties": {
                    "program_file": {
                        "type": "string",
                        "description": "The filename of the Python program that needs debugging"
                    },
                    "errors": {
                        "type": "string",
                        "description": "The error messages generated when the program failed to execute"
                    },
                    "original_plot_request": {
                        "type": "string",
                        "description": "The original plot request that was used to generate this program"
                    },
                    "input_file": {
                        "type": "string",
                        "description": "The input CSV file the program should work with"
                    },
                    "columns": {
                        "type": "string",
                        "description": "The columns that should be used from the CSV file"
                    },
                    "output_png": {
                        "type": "string",
                        "description": "The expected output PNG filename"
                    }
                },
                "required": ["program_file", "errors", "original_plot_request", "input_file", "columns", "output_png"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates or overwrites the specified file with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    },
                    "filename": {
                        "type": "string",
                        "description": "The filename where the content will be written"
                    }
                },
                "required": ["content", "filename"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# Functions of the tools:

# 1. extract_entities_from_file

def extract_entities_from_file(file_name: str, entity_type: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    
    prompt = f"""
    Extract all {entity_type} entities from the following text. Return a list in the form [entity1, entity2, ..., entityk].
    Return ONLY the list. No explanations, no markdown formatting, no ``` markers, no extra spacings or line drops.
    Text:
    {text}
    """
    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()
    return result

# 2. internet_search_attribute (using SerpAPI)

def internet_search_attribute(entity: str, attribute: str) -> str:
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    query = f"{entity} {attribute}"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 3
    }
    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()
    data = response.json()

    snippets = []
    for result in data.get("organic_results", [])[:3]:
        snippet = result.get("snippet")
        if snippet:
            snippets.append(snippet)

    combined_text = "\n".join(snippets)
    prompt = f"""
    Given the following internet search results, extract the value of the attribute '{attribute}' for the entity '{entity}'.
    Return the result in this JSON format: {{"entity": "{entity}", "attribute": "{attribute}", "attribute_value": <value>}}

    Results:
    {combined_text}
    """
    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 3. gen_plot_prog

def gen_plot_prog(plot_request: str, input_file: str, columns: str, output_program_file: str, output_png: str) -> str:
    prompt = f"""
You need to write a Python program that reads a CSV file and creates a plot.

Requirements:
- Read CSV file: {input_file}
- Available columns: {columns}
- Plot request: {plot_request}
- Save plot to: {output_png}

INSTRUCTIONS:
1. Handle any column name variations (extra spaces, different capitalization)
2. Use proper error handling for missing data
3. Include import statements: pandas as pd, matplotlib.pyplot as plt, json (if needed)
4. Use plt.figure(figsize=(12, 8)) for better visibility
5. Add proper labels, title, and legend
6. Save with plt.savefig('{output_png}', dpi=300, bbox_inches='tight')
7. Do NOT use plt.show()

Return ONLY executable Python code. No explanations, no markdown formatting, no ``` markers.
Start with imports and end with plt.savefig().
"""

    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    program_code = response.choices[0].message.content.strip()
    
    with open(output_program_file, 'w', encoding='utf-8') as f:
        f.write(program_code)

    return program_code

# 4. execute_Python_prog

def execute_Python_prog(program_file: str) -> str:
    try:
        result = subprocess.run(
            [sys.executable, program_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return "Program executed successfully"
        else:
            return result.stderr
    except Exception as e:
        return str(e)

# 5. debug_and_regenerate_prog

def debug_and_regenerate_prog(program_file: str, errors: str, original_plot_request: str = "", 
                             input_file: str = "", columns: str = "", output_png: str = "") -> str:
    with open(program_file, 'r', encoding='utf-8') as f:
        original_code = f.read()

    prompt = f"""
A Python program has failed with the following error. You have the original requirements to help you fix it properly.

ERROR: {errors}

ORIGINAL CODE:
{original_code}

ORIGINAL REQUIREMENTS:
- Plot request: {original_plot_request}
- Input file: {input_file}
- Expected columns: {columns}
- Output PNG: {output_png}

Your task:
1. Analyze the error in context of the original requirements
2. Check if the program is addressing the right requirements
3. Fix both the error AND ensure the program meets the original specifications
4. Return a complete, corrected Python program

CRITICAL: Return ONLY the complete corrected Python code. No explanations, no markdown.
The code must be syntactically correct and fulfill the original plot request.
"""
    
    response = client.chat.completions.create(
        model=MODEL_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    
    fixed_code = response.choices[0].message.content.strip()
    
    # Clean up markdown formatting
    if fixed_code.startswith('```python'):
        fixed_code = fixed_code[9:]
    elif fixed_code.startswith('```'):
        fixed_code = fixed_code[3:]
    
    if fixed_code.endswith('```'):
        fixed_code = fixed_code[:-3]
    
    fixed_code = fixed_code.strip()

    with open(program_file, 'w', encoding='utf-8') as f:
        f.write(fixed_code)

    return fixed_code


# 6. write_file

def write_file(content: str, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

FUNCTION_REGISTRY = {
    "extract_entities_from_file": extract_entities_from_file,
    "internet_search_attribute": internet_search_attribute,
    "gen_plot_prog": gen_plot_prog,
    "execute_Python_prog": execute_Python_prog,
    "debug_and_regenerate_prog": debug_and_regenerate_prog,
    "write_file": write_file,
}

tools_that_invoke_llm = ["extract_entities_from_file", "internet_search_attribute", "gen_plot_prog", "debug_and_regenerate_prog"]

# logs:

def truncate_string(value, max_length=50):
    """Truncate string to max_length characters for logging"""
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length] + "..."
    return str(value)

def log_tool_entry(tool_name, parameters, log_file):
    """Log tool entry with parameters"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"**Entering tool {tool_name}**\n")
        for param_name, param_value in parameters.items():
            truncated_value = truncate_string(param_value, 50)
            f.write(f"Parameter {param_name} = {truncated_value}\n")

def log_tool_exit(tool_name, log_file):
    """Log tool exit"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"**Exiting tool {tool_name}**\n")

# Agent: 

def execute_tool_call(tool_call, log_file):
    """Execute a single tool call with logging"""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    # Log entry
    log_tool_entry(function_name, arguments, log_file)
    
    try:
        # Get function from registry
        if function_name not in FUNCTION_REGISTRY or FUNCTION_REGISTRY[function_name] is None:
            result = f"Error: Function '{function_name}' not implemented"
        else:
            func = FUNCTION_REGISTRY[function_name]
            result = func(**arguments)
    except Exception as e:
        result = f"Error executing {function_name}: {str(e)}"
    
    # Log exit
    log_tool_exit(function_name, log_file)
    
    return {
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": str(result)
    }

def run_agent(query_json, client, model="gpt-4o-mini"):
    """
    Main agent loop
    
    Args:
        query_json: Dictionary with query_name and resources
        client: OpenAI client
        model: Model to use
    """
    
    # Extract query info
    query_name = query_json["query_name"]  # Keep the full filename
    query_name_base = query_name.replace(".txt", "")  # Remove .txt for log filename
    resources = query_json["resources"]
    log_file = f"{query_name_base}.log"

    llm_calls = 0
    tool_calls = 0
    max_llm_calls = 15
    max_tool_calls = 10
    
    # Create simple system message
    system_message = {
        "role": "system",
        "content": "You are an intelligent agent that can answer queries by using available tools and resources."
    }
    
    # Read the actual query from the query file
    with open(query_name, 'r', encoding='utf-8') as f:  # Use query_name directly
        actual_query = f.read().strip()
    
    user_message = {
        "role": "user", 
        "content": f"""You are an intelligent agent that can answer queries by using available tools and resources.
        
    Available resources:
    {json.dumps(resources, indent=2)}

    You have access to the following tools:
    1. extract_entities_from_file - Extract entities from files using llm
    2. internet_search_attribute - Search for entity attributes online and process the results using llm
    3. gen_plot_prog - Generate python plotting programs using llm
    4. execute_Python_prog - Execute Python programs 
    5. debug_and_regenerate_prog - Debug and fix failed Python programs using llm
    6. write_file - Write content to files

Plan your approach step by step. Fully answer the query. Use the tools as needed to complete the query. Do not create new files without being told to.
Be efficient - you have maximal limits of {max_llm_calls} LLM calls (including this one) and {max_tool_calls} tool invocations total.

Query: {actual_query}"""
    }
    
    # Initialize conversation
    messages = [system_message, user_message]
    

    
    print(f"Starting agent for query: {query_name}")
    print(f"Query content: {actual_query}")
    
    while llm_calls < max_llm_calls and tool_calls < max_tool_calls:
        llm_calls += 1
        print(f"\n--- LLM Call {llm_calls} ---")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("Calling LLM for next tool to invoke\n")
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
            )
            
            assistant_message = response.choices[0].message
            
            # Add assistant message to conversation
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })
            
            # Check if there are tool calls
            if assistant_message.tool_calls:
                print(f"Assistant wants to call {len(assistant_message.tool_calls)} tool(s)")
                
                # Update llm calls counter as there are tools which invoke an LLM
                for tool_call in assistant_message.tool_calls:
                    if tool_call.function.name in tools_that_invoke_llm:
                        llm_calls += 1

                # Check llm call limit
                if llm_calls > max_llm_calls:
                    print(f"LLM call limit would be exceeded. Stopping.")
                    break

                # Check tool call limit
                if tool_calls + len(assistant_message.tool_calls) > max_tool_calls:
                    print(f"Tool call limit would be exceeded. Stopping.")
                    break
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_calls += 1
                    print(f"Executing tool: {tool_call.function.name}")
                    
                    # Execute tool and get result
                    tool_result = execute_tool_call(tool_call, log_file)
                    
                    # Add tool result to conversation
                    messages.append(tool_result)
                    
                    print(f"Tool result: {tool_result['content'][:1000]}...")
            
            else:
                # No tool calls, assistant provided final answer
                res = assistant_message.content
                
                print("Assistant provided final response:")
                print(res)
                
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"final response is = {res}\n")

                break
                
        except Exception as e:
            print(f"Error in LLM call: {e}")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"Error in LLM call {llm_calls}: {e}\n")
            break
    
    print(f"\nAgent completed. Used {llm_calls} LLM calls and {tool_calls} tool calls.")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Used {llm_calls} LLM calls and {tool_calls} tool calls.")
    return messages

if __name__ == "__main__":
    with open("input.json", 'r', encoding='utf-8') as f:
        query = json.load(f)

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=OPENAI_API_VERSION_4o,
        azure_endpoint=AZURE_OPENAI_ENDPOINT_4o,
    )
    run_agent(query, client)