import pandas as pd
import os


# Load 1000 lines from a JSONL file
def load_csv_sample(file_path, num_lines=100000):
    sample_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for _ in range(num_lines):
            line = file.readline()
            if not line:
                break
            sample_data.append(line.strip().split(','))
    #save to sample_data.json
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_data.csv', index=False)

    return sample_data

def main():
    # Define the path to the JSONL file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jsonl_file_path = os.path.join(current_dir, '../../data/processed', 'user_category_transactions.csv')

    # Load a sample of 1000 lines from the JSONL file
    # sample = load_csv_sample(jsonl_file_path, num_lines=1000)

    # Load top 10 of the CSV file
    df = pd.read_csv(jsonl_file_path, nrows=2)
    sample = df.values.tolist()
    print(sample)


    # Print the number of records loaded
    print(f'Loaded {len(sample)} records from the CSV file.')


if __name__ == '__main__':
    main()