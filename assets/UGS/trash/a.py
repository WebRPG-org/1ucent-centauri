import os
import shutil

def main():
    base_dir = os.getcwd()
    script_name = os.path.basename(__file__)
    moved_count = 0

    for filename in os.listdir('.'):
        if filename == script_name or os.path.isdir(filename):
            continue
            
        lower_name = filename.lower()
        cl_index = lower_name.find('cl')
        
        if cl_index != -1 and len(lower_name) > cl_index + 2:
            third_char = lower_name[cl_index + 2]
            folder_name = f"{third_char}_unsorted"
            folder_dir = os.path.join(base_dir, folder_name)
            
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)
                
            src = filename
            dst = os.path.join(folder_dir, filename)
            
            if not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"Moved: {src} -> {folder_name}/{filename}")
                moved_count += 1

    print(f"\nDone! Sorted {moved_count} files into character folders.")

if __name__ == '__main__':
    main()
