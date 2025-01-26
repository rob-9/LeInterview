
def find_problem(company_name):
    import random
    file = open("templates/companies.txt", 'r')
    problems = []
    for line in file.readlines():
        if line.startswith(company_name):
            problems.append(line[len(company_name) + 1: -1])
    return random.choice(problems)

if __name__ == "__main__":
    print(find_problem("google"))