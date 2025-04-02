import os

def dateset_choose(dirs):
    for i, d in enumerate(dirs):
        print(f"{i + 1}. {d}:")
        for j, x in enumerate(os.listdir(d)):
            print(f"({j + 1}) {x}")

def dataset_check(dirs):
    while 1:
        try:
            s = input("Choose the dataset: ")
            nums = [int(num) for num in s.split(".") if num.isdigit()]
            if (len(nums) == 2 and
                nums[0] >= 0 and
                nums[1] >= 0 and
                nums[0] <= 2 and
                ((nums[0] == 1 and nums[1] <= 11) or (nums[0] == 2 and nums[1] <= 3))):
                return f"{dirs[nums[0] - 1]}/{os.listdir(dirs[nums[0] - 1])[nums[1] - 1]}"
            else:
                print ("Try again")
        except ValueError:
            print("Try again")

def algotithm_choose():
    alg = ["BFS", "DFS", "Random Search", "Greedy Search", "A*"]
    for i, x in enumerate(alg):
        print(f"{i+1}. {x}")

def algorithm_check():
    while 1:
        try:
            a = int(input("Choose the algorithm: "))
            if 1 <= a <= 5:
                return a
            else:
                print("Try again")
        except ValueError:
            print("Try again")

def start():
    dirs = ["dataset", "testovaci_data"]
    dateset_choose(dirs)
    path = dataset_check(dirs)
    algotithm_choose()
    alg = algorithm_check()
    return path, alg