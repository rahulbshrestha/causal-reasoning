causal_cot_prompt = """
Guidance: Address the question by following the steps below:
Step 1) Extract the causal graph: Identify the causal graph that depicts the relationships in the scenario.
The diagram should simply consist of edges denoted in "var1 -> var2" format, separated by commas.
Step 2) Determine the query type: Identify the type of query implied by the main question. Choices
include "marginal probability", "conditional probability", "explaining away effect", "backdoor adjustment set", "average treatment effect", "collider bias", "normal counterfactual question", "average
treatment effect on treated", "natural direct effect" or "natural indirect effect". Your answer should
only be a term from the list above, enclosed in quotation marks.
Step 3) Formalize the query: Translate the query into its formal mathematical expression based on its
type, utilizing the "do(·)" notation or counterfactual notations as needed.
Step 4) Gather all relevant data: Extract all the available data. Your answer should contain nothing
but marginal probabilities and conditional probabilities in the form "P(...)=..." or "P(...|...)=...", each
probability being separated by a semicolon. Stick to the previously mentioned denotations for the
variables.
Step 5) Deduce the estimand using causal inference: Given all the information above, deduce the
estimand using skills such as do-calculus, counterfactual prediction, and the basics of probabilities.
Answer step by step.
Step 6) Calculate the estimand: Insert the relevant data in Step 4 into the estimand, perform basic
arithmetic calculations, and derive the final answer. There is an identifiable answer. Answer step by
step
"""

memorization_test_prompt = """
You are an AI assistant that has read many sources of text from the internet. I am looking at
text from the  "CLadder: Assessing Causal Reasoning in Language Models
" dataset, published by Zhijing Jin, Yuen Chen, Felix Leeb, Luigi Gresele, Ojasv Kamal, Zhiheng Lyu, Kevin Blin, Fernando Gonzalez Adauto, Max Kleiman-Weiner, Mrinmaya Sachan, Bernhard Schölkopf. Here is the README for the dataset:
CLadder: Assessing Causal Reasoning in Language Models
�� Get the dataset now! cladder-v1.zip
zip file size: 6.5MB
Version: v1
Date: 2023-05-25
Huggingface dataset: https://huggingface.co/datasets/causalnlp/CLadder
This repo contains the full CLadder dataset (and code) for evaluating (formal) causal reasoning in language models. The dataset asks yes/no questions in natural language that generally require statistical and causal inference to answer.

Although there are several different variants, the main dataset (including questions from all variants) is cladder-v1-balanced.json, so that is the recommended file to use for most purposes.

Our NeurIPS 2023 paper:
"CLadder: Assessing Causal Reasoning in Language Models" by Zhijing Jin*, Yuen
    Chen*, Felix Leeb*, Luigi Gresele*, Ojasv Kamal, Zhiheng Lyu, Kevin Blin,
    Fernando Gonzalez, Max Kleiman-Weiner, Mrinmaya Sachan, Bernhard Schlkopf.
Citation:
@inproceedings{jin2023cladder,
    author = {Zhijing Jin and Yuen Chen and Felix Leeb and Luigi Gresele and
       Ojasv Kamal and Zhiheng Lyu and Kevin Blin and Fernando Gonzalez and Max
        Kleiman-Weiner and Mrinmaya Sachan and Bernhard Sch{\"{o}}lkopf},
    title = "{CL}adder: {A}ssessing Causal Reasoning in Language Models",
    year = "2023",
    booktitle = "NeurIPS",
    url = "https://openreview.net/forum?id=e2wtjx0Yqu",
}
Here’s an example from the dataset:
{"question\_id": 0, "desc\_id": "alarm-mediation-ate-model1110-spec0-q0", "
    give\_info": "For people who do not drink coffee, the probability of
    ringing alarm is 42\%. For people who drink coffee, the probability of
    ringing alarm is 51\%.", "question": "Will drinking coffee increase the
    chance of ringing alarm?", "answer": "yes", "meta": {"story\_id": "alarm", "
    graph\_id": "mediation", "treated": true, "result": true, "polarity": true,
    "groundtruth": 0.09148280511411633, "query\_type": "ate", "rung": 2, "
    formal\_form": "E[Y | do(X = 1)] - E[Y | do(X = 0)]", "given\_info": {"p(Y |
    X)": [0.4218874364506764, 0.5133702415647927]}, "estimand": "P(Y=1|X=1) - P
    (Y=1|X=0)", "treatment": "X", "outcome": "Y", "model\_id": 1110}, "reasoning
    ": {"step0": "Let X = drinking coffee; V2 = wife; Y = alarm clock.", "step1
    ": "X->V2,X->Y,V2->Y", "step2": "E[Y | do(X = 1)] - E[Y | do(X = 0)]", "
    step3": "P(Y=1|X=1) - P(Y=1|X=0)", "step4": "P(Y=1 | X=0) = 0.42\nP(Y=1 | X
    =1) = 0.51", "step5": "0.51 - 0.42 = 0.09", "end": "0.09 > 0"}}, {"
    question\_id": 1, "desc\_id": "alarm-mediation-ate-model1110-spec0-q1", "
    given\_info": "For people who do not drink coffee, the probability of
    ringing alarm is 42\%. For people who drink coffee, the probability of
    ringing alarm is 51\%.", "question": "Will drinking coffee decrease the
    chance of ringing alarm?", "answer": "no", "meta": {"story\_id": "alarm", "
    graph\_id": "mediation", "treated": true, "result": true, "polarity": false,
     "groundtruth": 0.09148280511411633, "query\_type": "ate", "rung": 2, "
    formal\_form": "E[Y | do(X = 1)] - E[Y | do(X = 0)]", "given\_info": {"p(Y |
    X)": [0.4218874364506764, 0.5133702415647927]}, "estimand": "P(Y=1|X=1) - P
    (Y=1|X=0)", "treatment": "X", "outcome": "Y", "model\_id": 1110}, "reasoning
    ": {"step0": "Let X = drinking coffee; V2 = wife; Y = alarm clock.", "step1
    ": "X->V2,X->Y,V2->Y", "step2": "E[Y | do(X = 1)] - E[Y | do(X = 0)]", "
    step3": "P(Y=1|X=1) - P(Y=1|X=0)", "step4": "P(Y=1 | X=0) = 0.42\nP(Y=1 | X
    =1) = 0.51", "step5": "0.51 - 0.42 = 0.09", "end": "0.09 > 0"}} I am going to list some sample rows of data, and I want you to complete each row as best as possible. I am testing your memory.

"""

program_of_thoughts_prompt = """Generate dowhy code ONLY to solve this problem. 

Question: 
For patients not assigned the drug treatment, the probability of low cholesterol is 54%. For patients assigned the drug treatment, the probability of low cholesterol is 52%. For patients not assigned the drug treatment, the probability of taking of all assigned drugs is 79%. For patients assigned the drug treatment, the probability of taking of all assigned drugs is 43%.

Don't mistake p(X|Y) and p(X and Y), 

Code: 
import dowhy
from dowhy import CausalModel
import numpy as np
import pandas as pd

# Set a random seed for reproducibility
np.random.seed(42)

# Number of observations in the synthetic dataset
n = 1000

the probaility of X and Y is 0.45
p(X | Y) = 0.54
# Given probabilities
p_assigned_drug = 0.5  # Assume 50% of patients are assigned the drug treatment
p_low_cholesterol_given_no_drug = 0.54
p_low_cholesterol_given_drug = 0.52
p_takes_all_assigned_drugs_given_no_drug = 0.79
p_takes_all_assigned_drugs_given_drug = 0.43

# Generate whether the patient was assigned the drug treatment (0 = not assigned, 1 = assigned)
assigned_drug = np.random.choice([0, 1], size=n, p=[1 - p_assigned_drug, p_assigned_drug])

# Generate whether the patient takes all assigned drugs based on whether they were assigned the drug treatment
takes_all_drugs = np.array([
    np.random.binomial(1, p_takes_all_assigned_drugs_given_no_drug if drug == 0 else p_takes_all_assigned_drugs_given_drug)
    for drug in assigned_drug
])

# Generate whether the patient has low cholesterol based on drug treatment and whether they take all assigned drugs
low_cholesterol = np.array([
    np.random.binomial(1, p_low_cholesterol_given_no_drug if drug == 0 else p_low_cholesterol_given_drug)
    for drug in assigned_drug
])

# Create the DataFrame
data = pd.DataFrame({
    'AssignedDrug': assigned_drug,
    'TakesAllDrugs': takes_all_drugs,
    'LowCholesterol': low_cholesterol
})


# Define the causal model
model = CausalModel(
    data=data,
    treatment='TakesAllDrugs',  # Taking all drugs is the treatment
    outcome='LowCholesterol',   # Low cholesterol is the outcome
    graph="digraph {TakesAllDrugs -> LowCholesterol;}"  # Causal graph
)

# Estimate the causal effect using a linear regression method
causal_estimate = model.estimate_effect(
    identified_estimand=model.identify_effect(),
    method_name="backdoor.linear_regression"
)

# Print the causal estimate for additional insights
print("Causal Estimate:", causal_estimate.value)


"""
