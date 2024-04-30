from PIL import Image
import os
import sys

def convert_to_jpeg(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            with Image.open(file_path) as img:
                if img.format != 'JPEG':
                    output_filename = f"{os.path.splitext(filename)[0]}.jpg"
                    
                    rgb_im = img.convert('RGB')
                    rgb_im.save(os.path.join(directory, output_filename), "JPEG")
                    print(f"Converted {filename} to {output_filename}")
                    
                    os.remove(file_path)
                    print(f"Deleted original file {filename}")
        except IOError:
            print(f"Deleted {filename} due to open or conversion error")
            os.remove(file_path)
            

def main():
    if len(sys.argv) != 2:
        print("Usage python <convert_to_jpeg.py> path/to/directory")
    else:
        directory = sys.argv[1]
        convert_to_jpeg(directory)
    
if __name__ == "__main__":
    main()