row = '^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^.......'

def next_row(row):
    row = f'.{row}.'
    next = []
    for i in range(2, len(row)):
        relevant = f'{row[i-2]}{row[i]}'
        next.append('.^'[relevant in ('^.', '.^')])
    return ''.join(next)

safe = row.count('.')
for _ in range(400000-1):
    if not _ % 1000:
        print(_)
    row = next_row(row)
    safe += row.count('.')
print(safe)
