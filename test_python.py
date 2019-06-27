def calculate_subs(numb_list):

    if [i for i in numb_list if i > 100]:
        separ = numb_list.index(max(numb_list))
        mid = numb_list[separ]
        ll = calculate_subs(numb_list[:separ])
        rr = calculate_subs(numb_list[separ+1:])
        return (ll * mid) + rr

    else:
        sub_val = 0
        for i in numb_list:
            if i % 100 == 0:
                sub_val *= i
            else:
                sub_val += i

        return sub_val


def convert_text_to_number (textnum):

    STOP_LITERALS = ('and',)
    STOP_DELIM = ('-',)

    units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
    ]

    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]

    text_to_num_dict = {}

    for idx, word in enumerate(units):
        text_to_num_dict[word] = idx

    for idx, word in enumerate(tens):
        text_to_num_dict[word] = 10 * (idx + 2)

    for idx, word in enumerate(scales):
        text_to_num_dict[word] = (10 ** (idx * 3 or 2))

    replace_endings = (('ieth', 'y'), ('th', ''))

    literal_list = []
    for i in textnum.split():

        for ends, repl in replace_endings:
            if i.endswith(ends):
                i.replace(ends, repl)

        for delim in STOP_DELIM:
            if delim in i:
                i = i.replace(delim, " ")

        if " " in i:
            literal_list.extend(i.split())

        elif i not in STOP_LITERALS:
            literal_list.append(i)

    print(literal_list)

    cur_val = []

    for word in literal_list:
        word = word.lower()
        cur_val.append(text_to_num_dict[word])

    print(cur_val)

    return calculate_subs(cur_val)

print(convert_text_to_number("One million and one hundred and twenty-four thousand three hundred and fifty"))
print(convert_text_to_number("six hundred twenty three million twenty one thousand forty one"))
print(convert_text_to_number("fifty five thousand six"))