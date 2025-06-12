# from subdirectory.filename import function_name
from functions.run_python_file import run_python_file

def main():
    result = run_python_file("calculator", "main.py")
    print(result)
    result = run_python_file("calculator", "tests.py")
    print(result)
    result = run_python_file("calculator", "../main.py")
    print(result)
    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    main()
