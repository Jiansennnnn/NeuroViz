import os
import stat
#shutil.rmtree('/path/to/your/dir/')


def delete_directory_contents():

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    directory = os.path.join(current_dir, 'knowledgebase_file')
    relative_target_path  = os.path.join('..', 'graph_place', 'graph_histogram')
    directory1 = os.path.normpath(os.path.join(current_dir, relative_target_path))
    relative_target_path  = os.path.join('..', 'graph_place', 'graph_scatter')
    directory2 = os.path.normpath(os.path.join(current_dir, relative_target_path))
    relative_target_path  = os.path.join('..', 'graph_place', 'graph_line')
    directory4 = os.path.normpath(os.path.join(current_dir, relative_target_path))
    relative_target_path  = os.path.join('..', 'graph_place', 'graph_pie')
    directory5 = os.path.normpath(os.path.join(current_dir, relative_target_path))
    relative_target_path  = os.path.join('..', 'flask_util', 'backup')
    directory3 = os.path.normpath(os.path.join(current_dir, relative_target_path))
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    if not os.path.exists(directory1):
        print(f"Directory '{directory1}' does not exist.")
        return
    if not os.path.exists(directory2):
        print(f"Directory '{directory2}' does not exist.")
        return
    if not os.path.exists(directory3):
        print(f"Directory '{directory3}' does not exist.")
        return
    if not os.path.exists(directory4):
        print(f"Directory '{directory4}' does not exist.")
        return
    if not os.path.exists(directory5):
        print(f"Directory '{directory5}' does not exist.")
        return

    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)
    for root, dirs, files in os.walk(directory1, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)
    for root, dirs, files in os.walk(directory2, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)
    for root, dirs, files in os.walk(directory3, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)
    for root, dirs, files in os.walk(directory4, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)
    for root, dirs, files in os.walk(directory5, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path ,stat.S_IWRITE)
            os.rmdir(dir_path)


delete_directory_contents()