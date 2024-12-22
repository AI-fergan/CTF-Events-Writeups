data = ""  # Global variable
words = []  # Global variable

def main():
    global data, words  # Declare that you are using the global variables
    
    with open("data.txt", "r") as dic:
        data = dic.read()
    
    print(data)

    words = [data[i:i+5] for i in range(0, len(data), 5)]

if __name__ == "__main__":
    main()
