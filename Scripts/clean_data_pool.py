import os
import sys

def clean_data_pool(dataset, data_pool):
    dataset_files = set()
    
    # Traverse the dataset directory and collect all file names
    for dirpath, _, filenames in os.walk(dataset):
        for filename in filenames:
            dataset_files.add(filename)
        
    # Traverse the data pool directory    
    for dirpath, _, filenames in os.walk(data_pool):
        for filename in filenames:
            # If the file exists in the dataset, remove it from the data pool
            if filename in dataset_files:
                file_path = os.path.join(dirpath, filename)
                print(f"Removing {file_path}")
                os.remove(file_path) # Remove the file
                
def main():
    if len(sys.argv) != 3:
        print("Usage: Python script.py <path_to_dataset> <path_to_data_pool>")
        sys.exit(1)
            
    dataset_path = sys.argv[1]
    data_pool_path = sys.argv[2]
        
    clean_data_pool(dataset_path, data_pool_path)
        
if __name__ == "__main__":
    main()