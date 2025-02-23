import pandas
import re


def add_column(df, model_name):
    if model_name not in df.columns:
        df[model_name] = None
    else:
        print(model_name + " already exists in Dataframe!")

    return df


def add_columns_to_dataframe(df, column_names):
    for c in column_names:
        add_column(df, c)
        add_column(df, c + "_reasoning")

    df = df.reset_index(drop=True)

    return df


def extract_python_code(text):
    
    # Find the start and end of the Python code block
    start_index = text.find("```python") + len("```python")
    end_index = text.find("```", start_index)
    
    # If both start and end markers are found, return only the code in between
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index].strip()
    
    # If no code block is found, return an empty string or a message
    return "No Python code block found."


def extract_yes_or_no(input_string):
    # Using regular expression to find all occurrences of 'yes' or 'no' in the input string
    matches = re.findall(r"\b(?:yes|no)\b", input_string, re.IGNORECASE)

    if matches:
        # Return the last matched text in lowercase
        return matches[-1].lower()
    else:
        # Return None if no match is found
        return None


def generate_results(df, gt_column, pred_column_list):
    for pred_column in pred_column_list:
        # Check if the ground truth and predicted columns exist in the DataFrame
        if gt_column not in df.columns or pred_column not in df.columns:
            print("Specified columns not found in the DataFrame.")
            return

        # Calculate accuracy by comparing the ground truth and predicted columns
        correct_predictions = (df[gt_column] == df[pred_column]).sum()
        total_predictions = len(df)
        accuracy = (
            correct_predictions / total_predictions if total_predictions > 0 else 0
        )

        # Print accuracy as a percentage
        print("Accuracy for " + pred_column + f" : {accuracy * 100:.2f}%")


def generate_results_per_rung(df, gt_column, pred_column_list):
    for pred_column in pred_column_list:
        # Check if the ground truth and predicted columns exist in the DataFrame
        if gt_column not in df.columns or pred_column not in df.columns:
            print(
                f"Specified columns '{gt_column}' or '{pred_column}' not found in the DataFrame."
            )
            return

        # Ensure the 'rung' column exists
        if "rung" not in df.columns:
            print("Column 'rung' not found in the DataFrame.")
            return

        # Group by 'rung' and calculate accuracy for each group
        results = {}
        grouped = df.groupby("rung")
        for rung, group in grouped:
            correct_predictions = (group[gt_column] == group[pred_column]).sum()
            total_predictions = len(group)
            accuracy = correct_predictions / total_predictions
            results[rung] = accuracy

        # Print accuracy per rung
        print(f"Accuracy per rung for '{pred_column}':")
        for rung, accuracy in results.items():
            print(f"  Rung {rung}: {accuracy * 100:.1f}%")
