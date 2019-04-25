import zipfile
folder = zipfile.ZipFile('/Users/jeremylondon/Desktop/channel.zip')
nothing = '90052'
for i in range(909):
    info = folder.getinfo(nothing + '.txt')
    print(info.comment.decode(), end='')
    text = folder.read(nothing + '.txt').decode()
    #print(text)
    nothing = ""
    for c in text[-20:]:
        if c.isdigit():
            nothing += c
    #print(nothing)
    
