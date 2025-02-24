
# From Causal Parrots to Causal Prophets? Towards Sound Causal Reasoning with Large Language Models

This repository contains the code, data, and experiments related to the paper titled *From Causal Parrots to Causal Prophets? Towards Sound Causal Reasoning with Large Language Models*.

## Overview

Causal reasoning is a fundamental property of human and machine intelligence. While large language models (LLMs) excel in many natural language tasks, their ability to infer causal relationships beyond memorized associations is debated. This study systematically evaluates recent LLMs' causal reasoning across three levels of Pearl’s Ladder of Causation—associational, interventional, and counterfactual—as well as commonsensical, anti-commonsensical, and nonsensical causal structures using the CLadder dataset.

We further explore the effectiveness of prompting techniques, including chain of thought (CoT), self-consistency (SC), and causal chain of thought (CausalCoT), in enhancing causal reasoning, and propose two new techniques: causal tree of thoughts (CausalToT) and causal program of thoughts (CausalPoT).

While larger models tend to outperform smaller ones and are generally more robust against perturbations, our results indicate that all tested LLMs still have difficulties, especially with counterfactual reasoning. However, our CausalToT and CausalPoT significantly improve performance over existing prompting techniques, suggesting that hybrid approaches combining LLMs with formal reasoning frameworks can mitigate these limitations. Our findings contribute to understanding LLMs' reasoning capacities and outline promising strategies for improving their ability to reason causally.

## Folder Structure

The project is organized as follows:

- **`data/cladder/`**  
    Contains the original CLadder dataset.
  - `cladder-v1-q-commonsense.json`: Dataset used for all experiments, contains commonsensical causal questions.  
- **`data/cladder-perturbed/`**
    Contains perturbed versions of the CLadder dataset that we generated for our experiments.
  - `anticommonsensical-data.pkl`: Perturbed anti-commonsensical dataset.  
  - `nonsensical-data.pkl`: Perturbed nonsensical dataset.  

- **`src/`**  
  Source code for notebooks and experiments.  
  - `benchmark-cladder-openai.ipynb`: Code for running benchmark experiments with the OpenAI API on OpenAI models (GPT-4o, GPT-4o-mini)
  - `benchmark-cladder-deepinfra.ipynb`: Code for running benchmark experiments with the DeepInfra API on open-source/open-weights models (LLama-3.1-8B, Mistral-7B, WizardLM-2-8x22B, LLama-3.1-Nemotron-70B).
  - `benchmark-cladder-anthropic.ipynb`: Code for running benchmark experiments with the Anthropic API on Anthropic models (Claude 3.5 Haiku, Claude 3.5 Sonnet)
  - `perturb-dataset-anticommonsensical.ipynb`: Code for generating perturbed anti-commonsensical dataset.
  - `perturb-dataset-nonsensical.ipynb`: Code for generating perturbed nonsensical dataset.
  - `program-of-thoughts.ipynb`: Code for running experiments with Program of Thoughts.
  - `tree-of-thoughts.ipynb`: Code for running experiments with Tree of Thoughts.
  - `utils.py`: Utility functions for loading and processing data. 
  - `model_inference.py`: Utility functions for running models.
  - `prompts.py`: Prompts used for experiments used in this thesis.

- **`.gitignore`**  
  Specifies files and directories excluded from Git version control.


## Prompts

Here, we reference the prompts from the Causal Program of Thoughts and Causal Tree of Thoughts section from our paper.

The *GEN prompt* in the code can be found in src/tree-of-thoughts.ipynb

```python
generate_prompt = '''
Question: {question} -> {causal_cot_prompt} -> 
-> Generate {num_generated_options} possible options for this, and then put all the options in a list, each option being a string, like
Options: {{"X", "X", "X"}}. Make sure this is in a single line!
'''
```
The *EVAL prompt* in the code can be found in src/tree-of-thoughts.ipynb
```python
evaluate_prompt = '''
Question: {question} -> Options: {new_thoughts} -> 
-> Assign a score between 1 - 10 for each option in Options: depending on how well it answers the question (10 being the highest or the best), then put the score into a list, each score being a string, like
Options: {{"X", "X", "X"}}. Make sure this is in a single line!
```

The *CODE prompt* can be found in src/prompts.py.

The *ANSWER prompt* can be found in src/program-of-thoughts.ipynb
```python
answer_prompt = 'Question: \n' + prompt_question + "\n The solution after generating doWhy code to solve this problem is: " + solution + "\n Instruction: Based on this causal estimate, answer yes or no. Think about how the causal estimate answers the question, do not do calculations, but give an explanation. Answer: "
```

## Requirements

To run the code in this repository, ensure that you have the following dependencies installed:

- Python 3.x
- Required Python libraries (can be installed via `requirements.txt`)

Install the necessary libraries by running:
```bash
pip install -r requirements.txt
```
Create a constants.py file in the src/ directory and place the OpenAI, DeepInfra and Anthropic keys as:

```python
OPENAI_API_KEY = "your-openai-api-key"
DEEPINFRA_API_KEY = "your-deepinfra-api-key"
ANTHROPIC_API_KEY = "your-anthropic-api-key"
```


### Setup and Running the Code

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-account/your-repository.git
    cd your-repository
    ```

2. **Install dependencies (assuming you have Python and pip installed):**
    ```bash
    pip install -r requirements.txt
    ```

3. Navigate to the `src/` directory to find the Jupyter notebooks and run specific experiments.


## License

This code is released under the MIT License. See the LICENSE file for more information.
