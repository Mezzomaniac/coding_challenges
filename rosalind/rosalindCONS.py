from collections import Counter

def cons(data):
    iter_positions = zip(*(''.join(line for line in string.split('\n')[1:] if line).replace('\n', '') for string in data.split('\n>')))
    counts = [Counter(position) for position in iter_positions]
    consensus = ''.join(count.most_common(1)[0][0] for count in counts)
    print(consensus)
    for base in 'ACGT':
        base_counts = ' '.join(str(count[base]) for count in counts)
        print(f'{base}: {base_counts}')

data ='''>Rosalind_0366
TGCGTGGTTTATTCGAGTAACTGCAGAGGATGTTCTCCGGTCTGCGAAAAATTCAGCTAA
CTGAATACAACGGGCTGCCGCGGTCGATTCTTTTACTGTGGATGGGCGGAGCCCAGTATG
TATTATATGATGTAAACGCTCAGCTCATAAATCAGCCGCGAGCTGTATTACCTAGACAAC
GTAAAGGGCCTGCTTCGCCGATGTGTATGCCATACCACTAAGGCGGACCGTCAGCCTAAT
ACAGTCCCGGCGTGTTGGCCAGGCCCCTTTAACCGACAGTAAACATGGACGCCTTCAAGA
ACCTGTCTTGCCGATCAATCTGAGCGTTCGGCGTAATACCTTGCATTGCGACGTACCTGA
TAGAACATTTGAACCAATCCGTTTTATATCCAATATGGCCGATTTATGACTAAGAAATAA
GTCCTGGTTCCGCGTCTTTTGGTATACAGCCGACTAAGATGCAAAGATAATCTCCGGGTC
GATTAAAGCGCTTCCCCTAGATGTGGTGGCCACCTGACTATTATGCCAGTCATAACGACC
TCCCCCAACGCCTTCCGATTCTACCTGACCCAAGACAATACAAACTACGCTACAGTGGAC
TGCCCCCGTCAGCAGGGTGGTTGGCTGTCGTTCACGGGGGAAGGTGGAAGCGTAAATACC
CCGTAAACGTGCTTCTGGAAGATTCTAATAGTAGGTAACGGCCATATCTATCACGGCGCT
GAGCTTTAATCTTGCACGTCTACACTTTATCAACGGACTTTCGCGGGATGCCCGCGGATG
ACGAAGCGAATAGTACGCAGAATGAGTGCCAGTTCTGCGTTAGCTTCCTTCATGCCGATA
GATGGACTAACTTGAGTTTGGTAGGGTATCGCCAAGACTGTTCGAAGCCTATCTACCAGG
AGACTCTAAGATGGTGCAGGAATAAGCACGTCGGTATCAGGTCTGGTACCCCGAAAGGAT
ATATTTCGTCTAGCGGTCAAGCCTAC
>Rosalind_4121
CGTTAAGGAGTGTAACGGAGAGGGGGCCTCCCTAATCTACAGTAACGGGCGTGGGTCGGT
TGCGGGTGGAGCGTTCGTTCGATCGTTTTCGGTGAGCCTCCATAAGGGGTGATATAATAC
GGGTTGCCTCAAAAATGACGGCCGGAACCTTGTGCAATCGTTGCGGAGAATCAAGCGCTA
TAGTCATGAGGACTCCGGGGGAATGGAAGTCGTGCAGTTGCCTGACTTACACAAGCTGGA
TTACTGCGTGCCCGTGTATGACTAGGCGACGAGCTTCCCTAATCGATAACCGCGGGATCG
TTTTAGCTAGCGGGGAAGCCAAGTAACAACTAACTTGGTGGACTAAGGTTGATCAAGGTT
GGCGTGAGCGTACTGCTTAGCTAGTTGACTGATGTTTCTAGAGGCACCTACATTGCTTTT
TATCCCTTGCATCAAGTGTGTCAATAGCTGGCTCCGGAATTGCGGCTTAATTGGAAGGAT
ATTGACTAGAGACGTCGGCTTCCGACCGGACTGGGTGACTTTCTCCACCAGAGTCCCTCA
CCGCAAGATACAGCCGGGTTAATGTAGCGTTGTTACACCTATATTTTTCAAGCATAACCC
TAATAGTAGACCCTGGTGGTTCTGTGTGACGGTAGTTTAGTAGCAGACTAAATTTTGATA
TGAATCCATATCCACCGGATTGAGCGGATGTGTAGCTCCCGGTCACTACTATCGTTTCGG
AGCACAAGCTCAGTCTGACCCATGTGTAAGGGCTAGTTTGCTAGCGATCAGCCCGAGTAA
ATTCATGCCTCAGGGCATCTCCATCCTCGTTAGGCGACTTAGAGCTAGGCACTCGCTTTG
CGAACGAGGGGATTGCCGAGACAATAACGCCTGGGCGTTCAAACGTGAAAACTTATCTCA
CGGTGGTCAACATTATGCAAGGGGTTCACGGTCATTGGGATTGTCTAGGTTTTTTCTAAA
GCTAACGGTAGTAAGGTTTTAAGCAC
>Rosalind_6771
CACTTTTGAGCTGTAAAATCCCTGTGAATATGTGCGTCGGTGTTCTACGTACCGCCGTCG
TGGAAGTGATGGGCCCGCATCTGCATGAAATGGTCCAGTGTACTGTTTGTATGCTGCGAC
TATCCAATGAGTGGACTTGGGTGAAACTTACCGTGCCGAACAACCAGGACACTCGCCGAG
CGTTTCATGGATAGTCCGATAGCAAAGCTCCAATTAGACAGATCCCGTCATTTAGTAGAC
AGTTGCTTCTACGTTAAACCATGAGGTCACAAGAGTACCTACCACGGGTCGACGCCGGAG
TCAACGTAGAGCCGGTGATTGGTCTAGGTTTTACTTATCAAGCTTCGTTTACTGAGTGTG
ATATAATTCGTCCTCTCCTCGTAAAACTACATGTTTATGACTCTTACCTACTAGTGCGAT
CTACCCATTTGCGAATTGACACACACTAGAGTCGGGTTGGGTGTAGTGTCCTATAGACGT
TGTGACTTAACATCACAATATTGTTATCGATCATCCGTTACCCGGGATTTCCCGTAGTGA
TGCGTCCAAAAAGTGTGTATGAGCCCAATTAGAGCTAATGGAGAAGCGCATAGGTCTAGT
TGGGAAAGCCCGAAAATAGCACAGTTGGAGGCTCCTTCTAACCGAGCCATGGTGTTTCGA
TAACTGTGCAACCACTTCCCGCAGTTGGCCAGATTTGGTGACTCGACAGCCCGCTTGACA
TATTTGTGCGATCAAACCTGACCGATAAGTGATAGGTGACGCCTCGAGGAACTACTTAGC
CTCGGGCACGGGCTCCGCATGCGTTGGTTCGACGGACCGCCATAGCCTCCGTATTCTATA
CCTTACCTAGCCGTAGTCGTGACATTCAGACACTACTAGCATGCCACGTTACTGACTTTA
ATAACGGGTAACTTATCATGCGATACAACTGGGGCTCATCTGTTCATTGAGTCAGTTCTT
CGATTGAAACGTGGATTTCTCACCGT
>Rosalind_3385
ACTCGATAGTTCTATTTTTACGTGCAAGGTTCCGTAGAAACTTGAGAGACAGGACGTCTC
GATCACACCTCAGGTAGCCATTTTCTCTTAAAACACGATGGCAACTTCCATTAGGATACG
TCTCCATGGGGGCGCATATGGCGACTGCGCCTTTACTCCCATACCACTGGCGTAAGACCG
TACAGAGATTTGGCACTTCGAGGGATACAAACCGATCCAGATTATTTGCACTATTGTACG
CCAGTAGCTTACCAGATTGGGAACCACATAAGGATGCGGTAATTATTAGGTTAGATGCAA
CTCCGCCGAAGTGTGACTACGCGAGAGGGGGCTAGTTCCTGCCTTTATTGGTATTTTTGC
CGGGTCTATCTGAAGCGTGAATGTTTACCATGCTTTGGGCCTCAGGTCTCTTTCGAAGTC
TGCACGGACTAGCGTATAATCGACGGTGCCGCCCGGGGATCCAAATAAAGACTCCGCGCA
GGACGTACAGGGGAGCGGTTACATTGCATTCTGAAATCAACCTACGCGTGTGCTCGCGGC
CAGCGAATCCTTTCAACACTAGACGCACTATTAAGGTTCAGGATACCAACGGACTCATTC
CACCGGCGAGCAGGTAAAATAGGTTCGTTCGCCCCTTTCCCGCGCAGGAGTCTTGCCATA
ACGCCCGTCCAGCCTTAGCAAGACAAGTGCTTGATTCTGTGAGTCATATTAAGGAAGACA
TACTCACTAACCAAGGGAGCTTCAATCGACACTACCCCTGACGCTCTGGGCATGAGCAGT
CATGAGGTAACGACAGACAAGGGTTACTTTTGAGGGCATGTGCGTCTTAGACGGGTGCAG
CACCCTTGACTAGTCACTTTGTGTGACCTCGGCGGATAACGGCGCTATCCGGATCCAATA
GTGTGATGACCCTTATTGACGGTGGATCACTAGGTAATTGGGGGACGACATGACGTACCC
AGACGCCGGTTGGCTATTACTATGCT
>Rosalind_8830
CTTATTAGCCACTCTGGATCTCAAGTGTCAAGTCACCTTCAATGGTTTCCTCGTCGCTTT
TACTGGGATTGCTACTGGCCTGGAGTTGTATATCGGTGTACCCGGGGCTACGACTTCACA
TGTCGCCACGCATCTTGGAACGGTCATCGCGGACGGATCGGCGACCCAGCGCGAGTATTG
TGACTATCCTTTTTGTCCCTTGGTCTAGTCTGGCAGCATTTTAGGATTTTACTTTGTATA
TACCCTATTTCAATAACGTTTGTCTATCGCGATTACATATACTCGGATCGGGTCTGCGGG
CCTCGGGTAGAGTCTACATTAAATGACACGTCAGGCTCTACGACACATCCTAGTCCGTAG
AACACGATTATACTAAACCAGCAACCTGACCACCCTCCACTATGACATTTAAATGCTTTC
CTAGTAGCATTAATAACCAAACGTCTAGGTTGTTGGCTATCCAGTGAGTTGCAGCGCCCA
CTAGGGTAGGCGGTCTACTCCGTAACCAAACCACTAACCATTGCACATAATTTGCCCTAG
AGACTCGGGAATTTTGCTGCAAGTGCATAAATCGGTAGGTACGCATGATCAGGGTAGGGC
CTAAAGCTTCTGTGTCCAGGCCGGGTAAATACTAGTAGGTTTATGGAGTCTGCTCTTGAT
CTGTCAACACGAGCTCTAGAATATCGCTACCGGGACGCGCCTCGCTGCCAGGCAAGTGTA
CGCCAGTGTCAGGTTTAGCTCAATTGAGAGATCACCAAATAGCGTATATGTAACAGCGTT
ATATAGCCTAATCAGAGAATGAGAGTTATGCCGAATTGCTGATGATTAGGCCCTAGAGTC
ACGGGATTGATTAGCCACAGTCGGTGCTTGCACACCTCTTTAGTAGCTTAGAGTTACTAA
GTTCACAGGACTGGTCCCAGATGGACCTGTAAGCCAGCACCCGACCGCACAGTAGCAGCG
GTGTTAGATCGCATAGTGGAGGGTCA
>Rosalind_4921
AGACGCAATTCTCCATTCCAAGTCCAGGCTGCGTACACATTGTATGGTCGTATTTTTATA
GGAACCTAACCCGGCCGTCGTGTGTGCAGGCTACAGTATGGAGTTAAACTTGTAGGGGGA
GATTTGAGTCGCAATCCGCCGAGTCAGCTTGCAATATTAATGGTTCATTGTAACCGGCAA
AGGTTGGTCTCTCTTTGTAATAGCAAACCCTTTTCCATCGTTCAGCAGCATGGTCATTTA
CAGTCGACTGCCGTAGGCCCCCAAACGGTGTCGGCGTATTCTGGACCGGATTAAAAATTC
ATGGCCCGGACACGGCTAGTTGGAACGGGGGTGGAGCTATCTGATCATATCTGTACCTCT
ATGCATTAACCGGTACTGGCATGGATGCAACTATTGAAGTGTAAATCATTGACTCCTCAG
CTTATGTGCGCACGCCTGAAGGCTCGTCGCGCTGACTACGGAATCTTGACACTATACTTC
ATTGTGGGTGAACATGCTGACCTAGCGTTTACTAGGAGACTAAGCGCCTACAGTCCGCCC
CCCCCCTAGTTCTGTACGCGGGCGCGCTTTGTAATGCCGTGTATACCTTACCGCTGACGC
CCAGCACCTGTCGGTGCTGTGTGACGCTATAGTATTCCCCGTGTGGTGCTCGAGGGTATC
TTAGGAGGCTTAATGAGGTTCGTTACTCCTATCAATGCTGGGGCGAGGGCGGGAGCGTGG
TGATGCTGGGGGTTCGGAAATTCCTCGTGGACCGCTTCAGGCGCCCAGCTAGTGTCGCGT
GGGCCGGCCTTTCTCGATGACCTTAACTCCACACAGTAATAAGAACTCCTTGTATGCTGC
GAAGACGTGCACTAACAGACTGCTAGCCAAGCTGCCTTAACAGGACCTCAGCTTAGGTTC
AGTATTCAATGAGAACTGACTGCGAACCTTAGAATCTAGGAGTTGGATACTCTCCCCGGA
TTCCGCCAACGCCTGGGGATGTTTCA
>Rosalind_5317
CAGGTTGGCGAGACCCCACGTAACAGGCAGGTATGGGTCCGGGATTTCAACGTATCCACC
ATATTCCTGGAGAAGTACTCGTGCTATTCCTACGGTGGGTTCCCAGGAATGTTGTTGACT
GGGTTCGAACTCCTTGAATGCAATACCAGTTGCCTCGAGGGATTTACGGACGCGATGAGG
CAGCGCAGATGACATATGAACGCTGATTCCAGAGCATATGCACCGGTCTTTGCCCTGCCG
CTACTACTTATTCTGAAATTCGTTTCACTCGGCAATCAGGTGAAACTTACCCATCAGGGA
TGGTGGGGCCTTAGTCCATGCCGCTGAGTTCCGTGAATCTACCGGCCTTGGTACCAAGAA
TGACTCAACGCAACTAAGATCTTCCCATGCCTCTACTGAGTTGATCTGAGGTTTCCTTGG
AGGGACCAGGGCCGGGGCGGAATAGCCACGTTAATACGCTAATAGTCGTGATATTCCGTA
ATATTATCCGCCGCGCGCACAGGATAGACGATATCTGATACTTCTGGGATGTTGTAGACA
AGTCGAGGGTGTGCCAAGCTTGATACATTAGATTTAAGAAAGCCTTAGTCACACCTCGAA
GCTGACTGACGGTCCGTACAAACAGATTCACGGGGGTACTCGCAGGCAAAACGGCAAGCG
GGTAGAGGTAGATTTTGTAATGGGAATTCCCTAAAACAGCCTCGCGGGGCTGAACTTCAT
CCCCATCCGAACTTTGTGGGTAATTGATATGGCTATCATCTATGAAGTCTAATCAGGCCA
TGTCTCGATATTGGTCGGGTCATTGATCACACGGCAATCAAATTACGCCTTCGGTAACAC
TCCGGCAGCCAAACCGCATCCAAGGCCCTTCGAGTTGGCAAAAACTGGCCATTGTATTGC
GGACAACCAACGCTGAGACACAAACCATACGGACTAGGGTTCCAGCCGCAACCCTCGGCG
TCCTTGAGGTTAGGTCGAGTTTGAGC
>Rosalind_7878
TACGCTTCTAAGGTTTCGCTCAGGGCTTCCACCAGGGAGACGACCGGGTCACAGAAGGCG
GGATCCGGGCTTACGTATGCACTGCAGTCAACCAAGTAAACAGTGTGATACACCACGTCC
GTAGCCTCACTCAAAGCAGCACGCAATCTTGTCAACGAGGGTACTGCATCAGAAGCTTTG
TTGTGCCCGACGTAAGCGCAGATAAGGGCCCAGTTCTGCTGAATGTGAACCTGGACGATC
CTATTCATCAGCCTGCTACGTCAGGACCCACCAAGAACACTCACACCCGTCTCATACTGT
CGGGAAGCCAGGGGATCACTAGTATATTCGATAATGGGTGTGGTGCTCGAGTAACCTACT
ATTGTATTTTACTATATTCGGAATCCATAAGGGATCCTATTTCATAGATCACTTTACTAG
TCCGGTTCGCTGTTGACCCTAAAGACGCCCGAGCTCAATAAATAACGGCGCATTTGAATC
CCCAGGTAAGTGTTCTGTGCGTACGGGTGACCACCAATAGAGCAGCATTGTGACAAGACC
GCCATTAAAAGATAGTAGTGGTATACCGGGTAGGCCAAGCTATTGGACTGCATATCATTT
CCCTGCTCCCAACCACTAAGCCCGCGAGTTCTTCCGGCTTAGGCCCGGCCAACCCAAGTG
CTCCATGGTAGTCTACAGAGAGAGCATGCTAACAACCTGGCAGGTCACAATATTGCAATA
TCAGCTCATGGTTCAAGTAACTTAAGTGGGGTGCGGAATGGATTAAAAGTTTCGGTGGGT
AAGAGAGGGCTGTCTCGGGGCATTTGAGGTGATTGCAAATACGGGCCGCCTCTCCGTGGG
TGTGGTTACAGACGGCTTCTACACTAATGCTTAGCGAACTTCAGACGGTGCCGGAGCTGA
CGCTCCCATCATAGATAAACGTCGCTTCGGAAGGACGGTACCACATAGACATGCCTTTCG
CGCACAGCCCTAGGGGGCCCTCTGTA
>Rosalind_5379
GCGGAACCACGCTACACTCTCTCAGCACCGTAACTAACCGTGGTCCTTTGAACGTTAAAG
GTGGGAGGTCGTCCCCAGTGGACTCGCAACACTTTGTGGGCTTCATAGTGTCGGTATTCG
CATCTCAGCTTTACGGGAGTGCTAGTTTACCCGATTAGCGAAGCGCGACGTTCTCTCAGC
CCCTAAACTAATTAACTTCGGATTGGCATCTGGAGCCCACTACAGATAAGTGTGAGCATC
TGCATGGCTGAAGCAGAGATGGGATTTAGGATATTTTCAAGGACCAAGGTCAAGGCTATC
AGTTGGTCAAGGCAGACTCTAGATGGGGCACAGACCGTTAGTCTGGTTCTTACCTTTACA
AAGGCAGTTAGAATTTATTCCGCTATTGTGTTAAGTGGGTCCCACCGAGACGAGGACCTA
TTCGAGTTAGTTCACCGAGGCGTTGCTCCTACCTCGCCCAGTCATCGTTATACTCCAGAT
GGTAAAAATCCTCGGTGTTATTTGATATCGAGTATAGTCTAATTATGCTACAAGTTAGTC
GCCCAACGTTGGCTTTGGGCCTGGAAGAGCTTGTGCATACTAGAACCAGGAATATCGGAA
CAAAACCACCTGGTAGTCTCATCACTGGCAGGTGCCAGCATCACACCCCCTCCCGTACCC
GACTAGGTGACTTAATACACCGACTTGTTAGCATACTGAGAGATAAAGTCGTTTCAATAA
GGTGCGAAAATAAGGCTTTGTTTGGATCAATACCACGTAAAATGGGCAGAAATACTATCT
GGAGTTCTGATCTTTCAAGGTATGTCGGACGGGAGACAATAAGGATACTGCTTAGGGGCA
ACTAACTTTTCTGGTCACCACCCGAGTGTTTCCTAGTAGTGACGTATGGGATAATTAGCG
AGTGTTACCACTTTTCTGCTGGAGTCACTAACTCGCTAACCTTACGACTTACGCCCGCGA
CGCACCGGCTTGCCGTTTCCGCCGCC
>Rosalind_2286
TGGGGTCTCCTCGTTGGACAGGATGTAGTCCCGTCGATTCGTGCCTCGCTCATAATGGCT
TTTCCGGCTGAGACAAAGCCAGATTCAGTCCTAAAGAAGCCGGGGTATAACTAGGACGCG
ATGTTGTGGCCCACCAAGTTGCCGTGCAGCTTCATTTACTGACAGTCTGAGAAAGTGAAA
TCTTCATACCTGCTTCTAGTCTAACCTATACAATTAAACGTGCTGTGTATTTGGCGTACG
AGTAATGGCGGATCAAGGTACTTGCTCAACCGTGATTGAGTTTACCAGTTAGCCCCACGA
CACATCAGCAGGTGCCGGTCTTTTAATGGTTCGCTCACCCGAGGACGGAAAGATATGCGA
TTATACGCTTAGGAGCACCAGGGAGACGGGTCTTATAGTGATATGATCGAACCGCCCAGA
TATCGCATGTCACTAGATTCGGGACCAAACACTGCACTAGTCAGAGCTGATGCACCAGTG
ATTACCGCTCGTCATTTACAAGAGCACCAACACCAGCGTTTCTAACAATAATCGCGCAAT
AGTGGAAGGCCTTTTCAACTGAAAAACAAGTGATCTCCGCCATTGCGGCTCTCCGTGGGC
ATCACAAATCAGCATCCCGGCCGGCTACGACAGCTGCACCCTCTGATTATATGCACACGT
CAGTGTAAGTCAACTTCTCCGGTGGTTCAGCCCTACCTTTACAGCGGGATTCATCCTAGG
ACAGCCAGAAAACTCCGCAACGATGCATCCGTCGACGGATCAGCCTGTTCATAATAACCT
TCGGTTTACAGCTAGTTTAGAGACGTTGGAATCGACAAAGAACTATTCAATACTTCGAAA
CATTGCCCTCCGACGGAGCTTACGCAGATGGTCAAAGGAGTTCATTCTTTCCGTCGTGGT
CTTGTTGCACATCCTTTCAAGATCTCCGACATCTCATGACTCCTCCGCGCATATACGTTT
GTGGACTCATACGCGTCGTAGGACTA'''
cons(data)