import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def count_files_in_directory(path):
    """ Helper function to count files in a given directory """
    return sum([len(files) for r, d, files in os.walk(path)])

def count_dataset(base_path, location):
    counts = {}
    # if location == 'exterior':
    #     counts = {
    #         'Exterior Left Inswing': 0,
    #         'Exterior Left Outswing': 0,
    #         'Exterior Right Inswing': 0,
    #         'Exterior Right Outswing': 0,
    #     }
    # else:
    #     counts = {
    #         'Interior Left Inswing': 0,
    #         'Interior Left Outswing': 0,
    #         'Interior Right Inswing': 0,
    #         'Interior Right Outswing': 0
    #     }


    categories = {
        'lh_in': 'Left Inswing',
        'lh_out': 'Left Outswing',
        'rh_in': 'Right Inswing',
        'rh_out': 'Right Outswing'
    }


    for swing_type in categories.keys():
        directory_path = os.path.join(base_path, 'doors', location, swing_type)
        if os.path.exists(directory_path):
            file_count = count_files_in_directory(directory_path)
            counts[f"{location.capitalize()} {categories[swing_type]}"] = file_count

    return counts

def display_table(counts):
    df = pd.DataFrame(list(counts.items()), columns=['Category', 'File Count'])
    print(df)
    return df

def plot_data(df):
    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")
    
    # Create a bar plot
    plt.figure(figsize=(12, 8))
    barplot = sns.barplot(data=df, x='Category', y='File Count', palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('File Count by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Files')
    plt.tight_layout()  # Adjusts plot to ensure everything fits without overlap

    # Show the plot
    plt.show()


base_path = "C:/Users/pagel/OneDrive/Documents/Tivock/DoorCNN/Dataset/raw_data"  


def main():
    if len(sys.argv) != 2:
        print("Usage: python <file_name> <interior or exterior>")
        sys.exit(1)
    location = sys.argv[1]
    counts = count_dataset(base_path, location)
    df = display_table(counts)
    plot_data(df)
    
if __name__ == '__main__':
    main()
