f = open('nubmers.txt','w')
l = ['10','11','12']

for index in l:
    f.write(index + '\n')

f.close()

f = open('nubmers.txt','r')

l = [line.strip() for line in f]

l = [int(i) for i in l]
print(l)

f.close()