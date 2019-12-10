import itertools

if __name__ == "__main__":
    with open("inputs/day8.txt") as f:
        layers = []
        img_dim = (25, 6)
        data = list(f.read())
        size_2d = img_dim[0] * img_dim[1]
        for i in range(int(len(data) / size_2d)):
            layers.append(data[i * size_2d : (i + 1) * size_2d])

        v = min(layers, key = lambda x : x.count('0'))
        part1 = v.count('1') * v.count('2')
        print(f"part1: {part1}")

        img = []
        for i in range(size_2d):
            img.append(next(filter(lambda x : x != '2', [ l[i] for l in layers ])))

        col = { '0' : ' ', '1' : 'X' }
        img = list(map(lambda x : col[x], img))

        print("part2: ")
        for i in range(img_dim[1]):
            print("".join(img[i*img_dim[0] : (i + 1)*img_dim[0]]))
                