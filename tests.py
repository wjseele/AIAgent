# from subdirectory.filename import function_name
from functions.get_file_content import get_file_content

def main():
    # result = get_files_info("calculator", ".")
    # print(result)
    # result = get_files_info("calculator", "pkg")
    # print(result)
    # result = get_files_info("calculator", "/bin")
    # print(result)
    # result = get_files_info("calculator", "../")
    # print(result)
    # result = get_file_content("calculator", "lorem.txt")
    # print(result)
    result = get_file_content("calculator", "main.py")
    print(result)
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    result = get_file_content("calculator", "/bin/cat")
    print(result)

if __name__ == "__main__":
    main()
