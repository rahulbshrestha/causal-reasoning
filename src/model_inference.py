from prompts import causal_cot_prompt, program_of_thoughts_prompt
import pandas as pd
from openai import OpenAI
from utils import extract_yes_or_no, extract_python_code
import openai, anthropic


def initialize_openai_client(api_key, base_url) -> OpenAI:
    """
    Initializes and returns an OpenAI client with the provided API key and base URL.

    Parameters:
        api_key (str): The API key for authentication.
        base_url (str): The base URL of the OpenAI API.

    Returns:
        OpenAI: An initialized OpenAI client.
    """
    if not api_key:
        raise ValueError("API key is required but not provided.")
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client


def intialize_anthropic_client(api_key):
    if not api_key:
        raise ValueError("API key is required but not provided.")

    client = anthropic.Anthropic(api_key=api_key)
    return client


def generate_completion(prompt, model, temperature=1.0, client=None):
    if not client:
        raise KeyError("Client not initialized.")

    if type(client) == openai.OpenAI:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return completion.choices[0].message.content

    elif type(client) == anthropic.Anthropic:
        completion = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.content[0].text

    else:
        raise KeyError("Client not found.")


def cot_self_consistency(prompt, model, self_consistency_count, temperature=1.0):
    answers = []

    for i in range(0, self_consistency_count):
        prompt_answer = generate_completion(prompt, model, temperature)
        extracted_answer = extract_yes_or_no(prompt_answer)
        answers.append(extracted_answer)
        print("Model answer ", i, " : ", extracted_answer)

    print("Answers: ", answers)
    most_common_string = max(answers, key=lambda x: answers.count(x))

    return most_common_string, answers


def run_model_on_cladder(
    df,
    model,
    method_name,
    info_column,
    question_column,
    output_column,
    min_range,
    max_range,
    temperature=1.0,
    overwrite=False,
    self_consistency_reasoning_chains=1,
    client=None,
):
    for col in [output_column, info_column, question_column]:
        if col not in df.columns:
            raise KeyError(f"{col} : Column name doesn't exist in dataframe!")

    for i in range(min_range, max_range):
        # Skip rows if overwrite is False and column is already populated
        if not overwrite and pd.notnull(df.iloc[i][output_column]):
            print(f"Skipping: {i}")
            continue

        prompt_question = df.iloc[i][info_column] + " " + df.iloc[i][question_column]

        if method_name == "input_output":
            prompt_question += " Answer with 'yes' or 'no' at the end."
            prompt_answer = generate_completion(
                prompt_question, model, temperature, client
            )
            extracted_answer = extract_yes_or_no(prompt_answer)

        elif method_name == "zero_shot":
            prompt_question += (
                " Let's think step by step. Answer with 'yes' or 'no' at the end."
            )
            prompt_answer = generate_completion(
                prompt_question, model, temperature, client
            )
            extracted_answer = extract_yes_or_no(prompt_answer)

        elif method_name == "causal_chain_of_thought":
            prompt_question += (
                causal_cot_prompt + " Answer with 'yes' or 'no' at the end."
            )
            prompt_answer = generate_completion(
                prompt_question, model, temperature, client
            )
            extracted_answer = extract_yes_or_no(prompt_answer)

        elif method_name == "cot_self_consistency":
            prompt_answer = ""
            extracted_answer, answers = cot_self_consistency(
                prompt_question,
                model,
                self_consistency_reasoning_chains,
                temperature,
                client,
            )

        elif method_name == "tree_of_thoughts":
            pass

        elif method_name == "program_of_thoughts":
            
            from langchain_experimental.utilities import PythonREPL
            python_repl = PythonREPL()  
            
            generated_code = generate_completion(prompt_question + '\n' + program_of_thoughts_prompt,  model, temperature, client)
            extracted_code = python_repl.sanitize_input(extract_python_code(generated_code))    
            solution = python_repl.run(extracted_code)
            
            followup_prompt = 'Question: \n' + prompt_question + "\n The solution after generating doWhy code to solve this problem is: " + solution + "\n Instruction: Based on this causal estimate, answer yes or no. Think about how the causal estimate answers the question, do not do calculations, but give an explanation. Answer: "
            print('FOLLOWUP PROMPT IS: ', followup_prompt)
            answer = generate_completion(followup_prompt, model, temperature, client)
            extracted_answer = extract_yes_or_no(answer)

            prompt_answer = '\n!!! Code generated by LLM: !!!\n\n' + extracted_code + '\n!!! Solution from Python interpreter: !!!\n\n' + solution + '\n!!! Final answer: !!!\n\n' + answer 
            
            
        else:
            raise ValueError(f"Unknown method name: {method_name}")

        df.at[i, output_column] = extracted_answer
        df.at[i, output_column + "_reasoning"] = prompt_answer

        print("(LOG) Prompt Question: ", prompt_question)
        print("(LOG) Correct answer: ", df.iloc[i]['answer'])
        print("(LOG) Prompt Answer: ", prompt_answer)
        print("(LOG) Extracted Answer : ", extracted_answer)
        print("(LOG) Generated answer for row number: ", i)
