class Personne():

    def __init__(self, nom,prenom):
        self.nom=nom
        self.prenom=prenom
        self.tel = ""

    def presenter(self):
        print ("================")
        print("nom :", self.nom)
        print("prenom :", self.prenom)
        print("tel :", self.tel)
    #print("moyenne :", p.moyenne)

class Homme(Personne):
    def __init__(self, nom,prenom):
        super().__init__(nom,prenom)
        self.sexe="M"

    def presenter(self):
        super().presenter()
        print("sexe :", self.sexe)
        print("Bouyaaaaaa")

    def boxer(self):
        print ("et pan")

class Femme(Personne):
    def __init__(self, nom,prenom):
        super().__init__(nom,prenom)
        self.sexe="F"

    def presenter(self):
        super().presenter()
        print("sexe :", self.sexe)
        print("un peu de tenue svp")


personne1 = Homme("Ezzoubiri","Hamza")
personne1.tel = "0690333333"
#print ("son nom",personne1.nom)

personne2 = Homme("Bourgarel","Moise")
personne2.tel = "0690444444"
print ("Son sexe", personne2.sexe)

personne3 = Femme("MC","Lucette")

promo=[]
promo.append(personne1)
promo.append(personne2)
promo.append(personne3)

for personne in promo :
    personne.presenter()

promo[1].boxer()
