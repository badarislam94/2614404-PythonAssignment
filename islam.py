import string
import re

def read_values(filename):
   # Read values from a value file and return them as a dictionary.
    values = {}
    with open(filename, 'r') as file:
        for line in file:
            letter, value = line.strip().split()
            # Check if the letter is alpha
            if letter.isalpha():
                values[letter] = int(value)
    return values

def read_names(filename):
    #Read names from a file and return them as a list.
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def read_cost_map(filename):
    #Read cost map values from a file and return them as a dictionary.
    cost_map = {}
    with open(filename, 'r') as file:
        for line in file:
            letter, value = line.strip().split()
            cost_map[letter] = int(value)
    return cost_map



def calculating_score(abb, name_list, cost_map):
    first, last, score = "", "", 0
    for i in name_list:
        if len(i) > 1:
            last += i[-1]
        first += i[0]

    for j in abb[1:]:
        if j in first:
            score += 0
            first = first[first.index(j):]

        elif j in last:
            if j == "E":
                score += 20
            else:
                score += 5
            last = last[last.index(j):]
        else:
            l = []
            for i in name_list:
                if j in i:
                    l.append(min(i.index(j), 3))
            if j in cost_map:
                score += min(l) + cost_map[j]
            else:
                # Handle the case when the key is not present in cost_map
                score += min(l)
    return score

def abbreviations_generator(name_list, values, cost_map):
    #Generate abbreviations for a given list of words.
    common_new = set()  # You can replace this with the actual set of common abbreviations if available
    name = "".join(name_list)
    n = len(name)
    abbreviations = set()

    for i in range(1, n):
        for j in range(i + 1, n):
            temp = name[0] + name[i] + name[j]
            if temp in common_new:  # Skip common abbreviations
                continue
            else:
                score = calculating_score(temp, name_list, cost_map)
                abbreviations.add((temp.upper(), score))

    return abbreviations

def excluding_used_abbre(abbreviations, all_names):
    #Filter out abbreviations which are already used.
    disallowed_abbreviations = set()
    used_abbreviations = set()

    for name_list in all_names:
        abbrevs = abbreviations_generator(name_list, {}, {})  # Pass empty dictionaries for values and cost_map since they're not used here
        for abbr, _ in abbrevs:
            if abbr in used_abbreviations:
                disallowed_abbreviations.add(abbr)
            else:
                used_abbreviations.add(abbr)

    return [(abbr, score) for abbr, score in abbreviations if abbr not in disallowed_abbreviations]

def choose_abbreviation(abbreviations):
    #Choose the abbreviation with the lowest score.
    if not abbreviations:
        return ""

    min_score = min(abbreviations, key=lambda x: x[1])[1]
    min_abbreviations = [abbr for abbr, score in abbreviations if score == min_score]
    return min_abbreviations[0]

def process_file(input_file, values_file):
    #Process the input files for names and values and generate abbreviations.
    names = [list(filter(str.isalpha, re.split(r'\W+', line.strip()))) for line in open(input_file, 'r')]
    values = read_values(values_file)
    cost_map = read_cost_map(values_file)

    all_abbreviations = []
    for name_list in names:
        abbreviations = abbreviations_generator(name_list, values, cost_map)
        filtered_abbreviations = excluding_used_abbre(abbreviations, names)
        chosen_abbreviation = choose_abbreviation(filtered_abbreviations)
        all_abbreviations.append(chosen_abbreviation)

    return all_abbreviations

def generate_output(surname, input_file, original_names, chosen_abbreviations):
    #Write the original names and chosen abbreviations to the output file.
    output_file = f"{surname.lower()}_{input_file}_abbrevs.txt"

    with open(output_file, 'w') as file:
        for original_name, abbreviation in zip(original_names, chosen_abbreviations):
            file.write(original_name + "\n")
            if abbreviation:
                file.write(abbreviation + "\n")
            else:
                file.write("\n")

    print(f"Results saved to {output_file}")

def main():
    input_file = input("Enter the name of the input file (e.g., testfile.txt): ")
    values_file = input("Enter the name of the values file (e.g., values.txt): ")
    surname = input("Enter your surname: ")

    abbreviations = process_file(input_file, values_file)
    original_names = read_names(input_file)
    print(f"Original names and chosen abbreviations:")
    generate_output(surname, input_file, original_names, abbreviations)

if __name__ == "__main__":
    main()
