import itertools

def validate_part2_subseq(val):
    safe_list = val + [-1]
    i = 0
    while i < 6:
        digit = safe_list[i]
        i = i + 1
        run = 1
        while i < 6 and safe_list[i] == digit:
            run = run + 1
            i = i + 1

        if run == 2:
            return True

    return False 


def validate_part1(val):
    digits = list(map(int, str(val)))
    consec_fn = lambda x : digits[x] == digits[x + 1]
    leq_fn = lambda x : digits[x] <= digits[x + 1]
    
    return any(map(consec_fn, range(5))) and all(map(leq_fn, range(5)))

def validate_part2(val):
    digits = list(map(int, str(val)))
    leq_fn = lambda x : digits[x] <= digits[x + 1]
    
    return validate_part2_subseq(digits) and all(map(leq_fn, range(5)))



if __name__ == "__main__":
    input = (256310, 732736)
    part1 = sum(map(validate_part1, range(input[0], input[1])))
    part2 = sum(map(validate_part2, range(input[0], input[1])))

    print(f"part1: {part1}")
    print(f"part2: {part2}")
