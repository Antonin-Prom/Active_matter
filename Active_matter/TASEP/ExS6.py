mot1 = input()
mot2 = input()
mot3 = input()

liste = [mot1,mot2,mot3]
def retourne_sans(mots):
    word = []
    for i in range (1,len(mots)):
        word.append(mots[i])
    sting = ''.join(word)
    print(sting)
        
    
for i in liste :
    retourne_sans(i)