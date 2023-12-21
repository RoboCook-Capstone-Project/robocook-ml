import os 
import pandas as pd 



def merge_csv(): 
    input_folder = './data/cleaned'
    output_folder = './data/final'
    os.makedirs(output_folder, exist_ok=True)
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]       

    final_dataset = pd.DataFrame()

    for file in csv_files: 
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        final_dataset = pd.concat([final_dataset, df], ignore_index=True)

    final_dataset.insert(0, 'id', range(1, 1+len(final_dataset)))

    output_path = os.path.join(output_folder, 'final_dataset.csv')
    final_dataset.to_csv(output_path, index=False)





if __name__ == "__main__": 
    merge_csv()