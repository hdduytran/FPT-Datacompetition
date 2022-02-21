with open('leader_board.txt','r') as f:
    lines = f.readlines()
check = set()
i = 1
for line in lines:
    na = line.split()[1]
    if not na in check:
        print(f'{i}: {na}')
        i +=1
        check.add(na)