

def read_input(filename):
    input = list()
    with open(filename) as ifp:
        for line in [x.strip() for x in ifp.readlines()]:
            ingredients, allergens = line.split('(')
            ingredients = ingredients.strip().split()
            allergens = [x.strip().rstrip(',') for x in allergens.split(')')[0].split()]
            allergens.remove('contains')
            input.append((set(ingredients), set(allergens)))
    return input


allergen_map = dict()
counter_map = dict()
identified_allergens = set()
seen_ingredients = set()

for ingredients, allergens in read_input("input.txt"):

    # print('')
    # print("{} -> {}".format(ingredients, allergens))

    for i in ingredients:
        counter_map[i] = 1 + counter_map.get(i, 0)
        seen_ingredients.add(i)

    remove_set = set()
    for a in identified_allergens:
        remove_set = remove_set.union(allergen_map[a])

    for a in allergens.difference(identified_allergens):
        a_i = allergen_map.get(a)
        if a_i:            
            allergen_map[a] = a_i.intersection(ingredients)
        else:
            allergen_map[a] = ingredients

    for a in set(allergen_map.keys()).difference(identified_allergens):
        i = allergen_map.get(a)
        if len(i) == 1:
            identified_allergens.add(a)
            remove_set = remove_set.union(i)

    for a in set(allergen_map.keys()).difference(identified_allergens):
        m = allergen_map[a].difference(remove_set)
        allergen_map[a] = m
        if len(m) == 1:
            identified_allergens.add(a)

    # print("remove_set:\t{}".format(remove_set))
    # print("identified_allergens:\t{}".format(identified_allergens))
    # print("allergens:\t{}".format(allergen_map))
    # print("counter:\t{}".format(counter_map))

for a in allergen_map:
    seen_ingredients = seen_ingredients.difference(allergen_map[a])

# print("clean ingredients:\t{}".format(seen_ingredients))


print(80 * "=")
print("result_a: {}".format(sum([counter_map[x] for x in seen_ingredients])))
print(80 * "=")
print(80 * "=")
print("result_b: {}".format(','.join(sum([list(allergen_map[x]) for x in sorted(identified_allergens)], []))))
print(80 * "=")

