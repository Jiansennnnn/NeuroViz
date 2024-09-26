import os

def create_and_check_directory(id):
    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.join(current_dir, 'knowledgebase_file')
    

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    

    has_content = len(os.listdir(parent_dir)) > 0
    
    
    new_dir = os.path.join(parent_dir, str(id))
    os.makedirs(new_dir, exist_ok=True)
    
    return has_content, new_dir

'''
external_id = '123456'
has_content, new_dir = create_and_check_directory(external_id)

print(f"Has content: {has_content}")
print(f"New directory created: {new_dir}")
'''