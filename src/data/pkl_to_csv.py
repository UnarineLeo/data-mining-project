import pickle
import pandas as pd

# Define the input .pkl file path and the output .csv file path
pkl_file_path = "../../data/raw/user_category_transactions.pkl"  # Replace with the actual path to your .pkl file
csv_file_path = "../../data/processed/user_category_transactions.csv" # Replace with your desired output .csv file path

try:
    # Load the data from the .pkl file
    with open(pkl_file_path, "rb") as f:
        data = pickle.load(f)

    # Convert the loaded data to a pandas DataFrame
    # The structure of 'data' will determine how it's converted.
    # If 'data' is already a DataFrame, this step is straightforward.
    # If 'data' is a list of dictionaries or a dictionary, pandas can often handle it.
    df = pd.DataFrame(data)

    # Save the DataFrame to a .csv file
    df.to_csv(csv_file_path, index=False) # index=False prevents writing the DataFrame index as a column

    print(f"Successfully converted '{pkl_file_path}' to '{csv_file_path}'")

except FileNotFoundError:
    print(f"Error: The file '{pkl_file_path}' was not found.")
except pickle.UnpicklingError:
    print(f"Error: Could not unpickle the file. It might be corrupted or not a valid pickle file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
