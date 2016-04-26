source = open('dev.en', 'r')

for l, line in enumerate(source.readlines()):
    f_main = open(str(l) + '.txt', 'w')
    f_os = open(str(l) + "_OS.txt", 'w')
    s_main = ''
    s_os = '<eps> 0\n'
    for w, word in enumerate(line.split(' ')):
        word = word.rstrip()
        s_main = s_main + '{0} {1} {2} {3}\n'.format(str(w), str(w+1), str(w+1), word)
        s_os = s_os + '{0} {1}\n'.format(word,str(w+1))
        last_w = w
    s_main = s_main + str(last_w)
    f_main.write(s_main)
    f_os.write(s_os)