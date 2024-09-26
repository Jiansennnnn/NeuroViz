import os



def delete_directory_contents():

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    directory = os.path.join(current_dir, 'knowledgebase_file')
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return


    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)




delete_directory_contents()