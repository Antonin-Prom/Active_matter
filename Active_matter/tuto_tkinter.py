from tkinter import*
fen = Tk()
fen.geometry('500x500')

fond = Canvas(fen,width=500,height=500,highlightthickness=0)
#bg = '' pour couleur
#highlightthickness = 0 enlève les bordures

fond.place(x=0,y=0)
#widget du canvas on appelle une méthode
#ligne :
ligne = fond.create_line(10,20,250,300,width=5,fill='red')
#rectangle prend que le coin en haut à gauche et en bas à droite
rectangle = fond.create_rectangle(10,20,250,300,width=5,outline = 'green')
#On crée un rectangle dont l'ovale touche tout les bords
oval = fond.create_oval(50,50,150,150)
#width pour epaisseur
#fill pour couleur
#outline pour bordure

#texte du canvas
#anchor positionne le texte par rapport au coordonnée
texte = fond.create_text(50,50,text='ceci',anchor='center')

#supprimer 
#fond.delete(ligne)
#tout supprimer
#fond.delete(ALL)
#modifier position :
fond.coords(texte,200,200)
#configurer 
fond.itemconfig(texte,text = "machin")
#récupérer contenu
print(fond.itemcget(texte,"text"))
#Gérer la profondeur
fond.tag_raise(ligne)
fond.tag_lower(oval)
fen.mainloop()

