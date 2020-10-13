# https://datarebellion.com/blog/intro-to-python-preface-the-journey-ahead/

from string import ascii_lowercase
from itertools import cycle

puzzle1 = """(dmsp rm rfc dmsprf nmucp) kglsq (rfpcc rgkcq lglcrccl)
((rcl rm rfc rfgpb nmucp) njsq mlc fslbpcb qgvrw mlc) bgtgbcb zw ruclrw qctcl
(rum rgkcq rfpcc rgkcq rfpcc rgkcq ruclrw rfpcc rgkcq rfpcc rgkcq rum fslbpcb rfgprw rfpcc rgkcq dmprw rfpcc) kglsq dgtc
rfc ufmjc lskzcp md rfc npmbsar md rfc yzmtc rfpcc gq rfc icw"""

def rot(puzzle, rotation):
  result = []
  for character in puzzle:
    if character not in ascii_lowercase:
      result.append(character)
      continue
    index = ascii_lowercase.index(character)
    new_index = (index + rotation) % 26
    result.append(ascii_lowercase[new_index])
  return ''.join(result)
#for n in range(26):
#  print(rot(puzzle1, n))
#  print()
print(rot(puzzle1, 2))

a= (4**4) - (3*19)
b = ((10**3) + 161) / 27
c = (2*3*3*23*3*233*43) - 5
d = a*b*c
print(d)
print()


puzzle2 = [
r"----|---------------------------------------------------------------------0---",
r"  \_/                                                                         ",
r"  / | \   0                           0                     0                 ",
r"  \_|_/                                                                       ",
r"    | |                                                                       ",
r"-|-/|--|-----------------------------------------------------------0----------",
r"----|-\-----------------------------------------------------------------------",
r"----|/-----------0------0-----------------------------------------------------",
r"---/|----------------------------------------0------0-------------------------",
r"    |                          0                                              ",
r"    |\                                                                        ",
]

#rows = str(int(d))[::2]
#indexes = str(int(d))[1::2]
#for row, index in zip(rows, indexes):
#  print(puzzle2[int(row)][int(index)])
  
#for row in puzzle2:
#  for index in str(int(d)):
#    print(row[int(index)], end='')
#  print()

indexes = [10, 6, 4, 7, 9, 8, 2, 5, 3, 0, 1]
for index in indexes:
  print(puzzle2[index])
  print()
  

ch2="""Each line is a string
That should be extended
So multiply by 43
Oh that would be splendid
Put the strings in a list
Multiply it just the same
Then use the string and list indices
To solve this game"""

raw_indices = """[107][733], [137][898:902], [152][682:685], [187][864], [238][1301:1303], [253][957], [296][847:849], [334][-1], [-4][-2]"""

def parse_indices(raw_indices):
    indices = []
    for pair in raw_indices.split(', '):
        first, second = pair.split('][')
        first, second = first[1:], second[:-1]
        indices.append([parsing_helper(first), parsing_helper(second)])
    return indices
        
def parsing_helper(string):
    if ":" not in string:
        return int(string)
    return slice(*(int(pos) for pos in string.split(":")))

indices = parse_indices(raw_indices)
print(indices)
multiplied = [line * 43 for line in ch2.split('\n')] * 43
print(len(multiplied), len(multiplied[0]))
for first, second in indices:
    print(multiplied[first][second], end='')
print('\n')


ch3num = 998877665544
divisors = [99, 77, 66, 55, 33]
for divisor in divisors:
    print(str(divisor) in str(ch3num), (ch3num % divisor) == 0)
print()


ch4 = [[41, 29, 17, 7], [37, 23, 13, 5], [31, 19, 11, 3]]
def ceiling(seq):
    return (((seq[0] + seq[1]) * seq[2]) ** seq[3])
print(sum(ceiling(seq) for seq in ch4))
print()


puzzle3 = """ro ncdm oyy mn, ahz ro dueho qax xem
ymnudrn pm ddbigwj, amc yiq'pe zoplkycghna oscbdsm
ncaqqahcc ar hmjhgec, cewenhdq lcgc tgd snwpt
sgeh wlsvdr ndc rhcdfa, ync aamg gn xnul wpt"""

# hints: convert to numbers; convert binary to decimal

#cabbage = cycle("cabbage")
#for c in puzzle3:
#    print((ord(c)+ ord(next(cabbage))), end='')

#for c in puzzle3:
#    try:
#        print(int(c, 35))
#    except ValueError:
#        print(c)

cabbage = cycle([ascii_lowercase.index(c) for c in 'cabbage'])
puzzle3nums = []
for c in puzzle3:
    try:
        puzzle3nums.append(ascii_lowercase.index(c) + next(cabbage))
    except ValueError:
        puzzle3nums.append(c)
print(puzzle3nums)
for i in puzzle3nums:
    try:
        print(ascii_lowercase[i % 26], end='')
    except TypeError:
        print(i, end='')
print('\n')
    


puzzle4 = """8813191238677333954665809213349646122194
3015595667663245206677258662604239718836
4431428926159036858913586646934493387784
2415423905479477475303429332505714485112
4090836065842116455582237940320444861841
8887593350492294228220622241460000717294
4955847547957801429318355097534895447954
7342296922244600793814495300151499126757
3076802599544010948629349194265749217345
4001893903317176122546504003906815939962
8428796996691959920597351056958454461881
4732394077366853306860112237237386161021
7871126702127244170489561553519315838470
2693690437372649049215349703278652470600
3015221909596231574709960176130567639024
0092004721669881955529429225102279034207
1330193718198499866240480029222396978969
9281228432921674821577765850343057221329
2779929871766974307119561522080156771664
7095071241828310135078223629923028803912
5453455582923797217620833928427273736063
7822533797916494440084693015546738131130
2640275104782204063786790634519992766829
2989314882818234607337721281487409823167
5734588734584493380447926820353540224813
5824663370552369365250850730508000154790
81377112162403735240993"""

#even_singles = ''.join(c for c in puzzle4.replace('\n', '') if not int(c) % 2)
#print(even_singles)
#even_lines = [num for num in puzzle4.split() if not int(num) % 2]
#print(even_lines)
binary = ''.join(str(int(not (int(c) % 2))) for c in puzzle4.replace('\n', ''))
print(binary)
decimal = int(binary, 2)
print(decimal)


puzzle5 = """pv-shwsub-hbbs-wbwuvffgs-uh-sosb-vdph-or
-huibtc-sw--wwucjhhss--hhousvjhgsapc-b-i
ooas-fgr-b-gvhohqwsarsa-wsfhus-hsuogsjsv
ibc--chg-rwab-qigro-zhwszrt-vsjohwfuo--w
vsgsh-h-csgbrr-ow-baccg-wigbqqsgp-gggbcz
asc-uhjrwossc-shhvg--q-fawouko-orb-oh-zz
vg-bsrckfs-n-froctwkmfchbto-iwfhbcrvsk-t
hmodvoh--fswzrvrzh--ssfhgo--susjudfhwb-s"""

dec = str(decimal)
runs = [dec[start:start+10] for start in range(0, len(dec), 10)]
print(runs)
rearranged = []
for n, run in enumerate(runs):
    for i in range(10):
        index = run.index(str(i))
        pos = n * 10 + index 
        rearranged.append(puzzle5.replace('\n', '')[pos])
rotated = ''.join(rearranged)
print()
#for n in range(26):
#    print(n)
#    print(rot(rotated, n))
#    print()
print(rot(rotated, 12).replace('-', ' '))
