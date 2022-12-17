# create a timesheet from the database "tp2bdd.db" using tkinter

import tkinter as tk
from tkinter import ttk
import sqlite3

# La base de données est composée de 7 tables :
# - APPRENANT : nomApprenant TEXT, prenomApprenant TEXT, idApprenant INTEGER, idClasse INTERGER
# - CLASSE : libelleClasse TEXT, idClasse INTEGER
# - COURS : jourCours TEXT, heureCours TEXT, idCours INTEGER, k_idClasse INTEGER, k_idEnseignant INTEGER, k_idMatiere INTEGER
# - ENSEIGNANT : idEnseignant INTEGER, nomEnseignant TEXT, prenomEnseignant TEXT
# - MATIERE : idMatiere INTEGER, libelleMatiere TEXT
# - MATIERE ENSEIGNANT : k_idMatiere INTEGER, k_idEnseignant INTEGER


class Bdd:
    def __init__(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM APPRENANT")
        self.result = self.cursor.fetchall()
        self.conn.close()

    def get_result(self):
        return self.result


# Class pour créer la fenêtre principale


class Main(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.title("Emploi du temps")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.bdd = Bdd()

        #faire un emploi du temps
        self.emploi_du_temps = tk.Button(self, text="Emploi du temps", command=self.refresh)
        self.emploi_du_temps.pack()

        self.tableau = Tableau(self, self.bdd.get_result())
        self.tableau.pack()
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Section élève", menu=self.file)
        self.file.add_command(label="Ajouter un élève", command=self.ajouter_apprenant)
        self.file.add_command(label="Supprimer un élève", command=self.supprimer_apprenant)
        self.file.add_command(label="Associer un élève à une classe", command=self.associer_apprenant_classe)
        self.file.add_command(label="Afficher la liste de tous les élèves", command=self.afficher_apprenant)
        self.file.add_command(label="Afficher les élèves d’une classe", command=self.afficher_apprenant_classe)

        self.enseigne = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Section enseignants", menu=self.enseigne)
        self.enseigne.add_command(label="Ajouter un enseignant", command=self.ajouter_enseignant)
        self.enseigne.add_command(label="Associer un enseignant à des matières", command=self.associer_enseignant_matiere)
        self.enseigne.add_command(label="Afficher la liste des enseignants avec leurs matières", command=self.afficher_enseignant_matiere)
        self.enseigne.add_command(label="Supprimer un enseignant", command=self.supprimer_enseignant)

        self.matiere = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Section matière", menu=self.matiere)
        self.matiere.add_command(label="Ajouter une matière", command=self.ajouter_matiere)
        self.matiere.add_command(label="Supprimer une matière", command=self.supprimer_matiere)

        self.cours = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Section cours", menu=self.cours)
        self.cours.add_command(label="Ajouter un cours", command=self.ajouter_cours)
        self.cours.add_command(label="Supprimer un cours", command=self.supprimer_cours)
        self.cours.add_command(label="Modifier un cours", command=self.modifier_cours)

        self.menu.add_command(label="Quitter", command=self.destroy)

    def ajouter_apprenant(self):
        AjouterApprenant(self)

    def supprimer_apprenant(self):
        SupprimerApprenant(self)

    def associer_apprenant_classe(self):
        AssocierApprenantClasse(self)

    def afficher_apprenant(self):
        AfficherApprenant(self)

    def afficher_apprenant_classe(self):
        AfficherApprenantClasse(self)

    def ajouter_enseignant(self):
        AjouterEnseignant(self)

    def associer_enseignant_matiere(self):
        AssocierEnseignantMatiere(self)

    def afficher_enseignant_matiere(self):
        AfficherEnseignantMatiere(self)

    def supprimer_enseignant(self):
        SupprimerEnseignant(self)

    def ajouter_matiere(self):
        AjouterMatiere(self)

    def supprimer_matiere(self):
        SupprimerMatiere(self)

    def ajouter_cours(self):
        AjouterCours(self)

    def supprimer_cours(self):
        SupprimerCours(self)

    def modifier_cours(self):
        ModifierCours(self)

    def refresh(self):
        self.bdd = Bdd()
        self.tableau = Tableau(self, self.bdd.get_result())
        self.tableau.pack()


# Class pour créer le tableau qui affiche les élèves
class Tableau(tk.Frame):
    def __init__(self, parent, result):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.result = result
        self.tableau = ttk.Treeview(self, columns=("ID", "Nom", "Prenom", "Classe"), show="headings")
        self.tableau.heading("ID", text="ID")
        self.tableau.heading("Nom", text="Nom")
        self.tableau.heading("Prenom", text="Prenom")
        self.tableau.heading("Classe", text="Classe")
        self.tableau.pack()
        self.afficher_tableau()

    def afficher_tableau(self):
        for row in self.result:
            self.tableau.insert("", "end", values=row)


# Class pour créer la fenêtre pour ajouter un élève
class AjouterApprenant(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Ajouter un élève")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_nom = tk.Label(self, text="Nom :")
        self.label_nom.pack()
        self.nom = tk.Entry(self)
        self.nom.pack()
        self.label_prenom = tk.Label(self, text="Prénom :")
        self.label_prenom.pack()
        self.prenom = tk.Entry(self)
        self.prenom.pack()
        self.label_classe = tk.Label(self, text="Classe :")
        self.label_classe.pack()
        self.classe = tk.Entry(self)
        self.classe.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO APPRENANT (nomApprenant, prenomApprenant, idClasse) VALUES (?, ?, ?)",
                           (self.nom.get(), self.prenom.get(), self.classe.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour supprimer un élève
class SupprimerApprenant(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Supprimer un élève")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM APPRENANT WHERE idEleve = ?", (self.id.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour associer un élève à une classe
class AssocierApprenantClasse(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Associer un élève à une classe")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.label_classe = tk.Label(self, text="Classe :")
        self.label_classe.pack()
        self.classe = tk.Entry(self)
        self.classe.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE APPRENANT SET idClasse = ? WHERE idEleve = ?", (self.classe.get(), self.id.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour ajouter une classe
class AjouterClasse(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Ajouter une classe")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_nom = tk.Label(self, text="Nom :")
        self.label_nom.pack()
        self.nom = tk.Entry(self)
        self.nom.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO CLASSE (NOM) VALUES (?)", (self.nom.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour supprimer une classe
class SupprimerClasse(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Supprimer une classe")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM CLASSE WHERE ID = ?", (self.id.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour associer une classe à un professeur
class AssocierClasseProfesseur(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Associer une classe à un professeur")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.label_professeur = tk.Label(self, text="Professeur :")
        self.label_professeur.pack()
        self.professeur = tk.Entry(self)
        self.professeur.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE CLASSE SET PROFESSEUR = ? WHERE ID = ?", (self.professeur.get(), self.id.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour ajouter un professeur
class AjouterEnseignant(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Ajouter un enseignant")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_nom = tk.Label(self, text="Nom :")
        self.label_nom.pack()
        self.nom = tk.Entry(self)
        self.nom.pack()
        self.label_prenom = tk.Label(self, text="Prenom :")
        self.label_prenom.pack()
        self.prenom = tk.Entry(self)
        self.prenom.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO ENSEIGNANT (nomEnseignant, prenomEnseignant) VALUES (?, ?)", (self.nom.get(),self.prenom.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


# Class pour créer la fenêtre pour supprimer un professeur
class SupprimerEnseignant(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Supprimer un enseignant")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM ENSEIGNANT WHERE idEnseignant = ?", (self.id.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()


class AfficherApprenant(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Afficher un élève")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()
        self.resultat = tk.Label(self, text="")
        self.resultat.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM APPRENANT WHERE idEleve = ?", (self.id.get(),))
        self.resultat["text"] = self.cursor.fetchone()
        self.conn.commit()
        self.conn.close()


#Afficher les apprenant selon la classe
class AfficherApprenantClasse(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Afficher un élève")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()
        self.resultat = tk.Label(self, text="")
        self.resultat.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM APPRENANT WHERE idClasse = ?", (self.id.get(),))
        self.resultat["text"] = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()

class AssocierEnseignantMatiere(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Associer un enseignant à une matière")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id_enseignant = tk.Label(self, text="ID enseignant :")
        self.label_id_enseignant.pack()
        self.id_enseignant = tk.Entry(self)
        self.id_enseignant.pack()
        self.label_id_matiere = tk.Label(self, text="ID matière :")
        self.label_id_matiere.pack()
        self.id_matiere = tk.Entry(self)
        self.id_matiere.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    #reste à voir pour la requête
    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE ENSEIGNANT SET idEnseignant = ? WHERE idMatiere = ?", (self.id_enseignant.get(), self.id_matiere.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()

class AfficherEnseignantMatiere(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Afficher un enseignant et ses matières")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id_enseignant = tk.Label(self, text="ID enseignant :")
        self.label_id_enseignant.pack()
        self.id_enseignant = tk.Entry(self)
        self.id_enseignant.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()
        self.resultat = tk.Label(self, text="")
        self.resultat.pack()

    #a voir
    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""SELECT * FROM ENSEIGNANT INNER JOIN MATIERE ON ENSEIGNANT = MATIERE.idMatiere""", (self.id_enseignant.get(),))
        self.resultat["text"] = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()

class AjouterCours(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Ajouter un cours")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id_matiere = tk.Label(self, text="ID matière :")
        self.label_id_matiere.pack()
        self.id_matiere = tk.Entry(self)
        self.id_matiere.pack()
        self.label_id_apprenant = tk.Label(self, text="ID apprenant :")
        self.label_id_apprenant.pack()
        self.id_apprenant = tk.Entry(self)
        self.id_apprenant.pack()
        self.label_date = tk.Label(self, text="Date :")
        self.label_date.pack()
        self.date = tk.Entry(self)
        self.date.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO COURS VALUES (?, ?, ?)", (self.id_matiere.get(), self.id_apprenant.get(), self.date.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()

class SupprimerCours(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Supprimer un cours")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM COURS WHERE idCours = ?", (self.id.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()

class AjouterMatiere(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Ajouter une matière")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_nom = tk.Label(self, text="Nom :")
        self.label_nom.pack()
        self.nom = tk.Entry(self)
        self.nom.pack()
        self.label_id_enseignant = tk.Label(self, text="ID enseignant :")
        self.label_id_enseignant.pack()
        self.id_enseignant = tk.Entry(self)
        self.id_enseignant.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO MATIERE VALUES (?, ?)", (self.nom.get(), self.id_enseignant.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()

class SupprimerMatiere(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Supprimer une matière")
        self.geometry("300x200")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM MATIERE WHERE ID = ?", (self.id.get(),))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()

class ModifierCours(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Modifier un cours")
        self.geometry("300x300")
        self.resizable(width=False, height=False)
        self.config(background="#FFFFFF")
        self.label_id = tk.Label(self, text="ID matiere :")
        self.label_id.pack()
        self.id = tk.Entry(self)
        self.id.pack()
        self.label_id_matiere = tk.Label(self, text="jours cours  :")
        self.label_id_matiere.pack()
        self.id_matiere = tk.Entry(self)
        self.id_matiere.pack()
        self.label_id_apprenant = tk.Label(self, text="heure cours :")
        self.label_id_apprenant.pack()
        self.id_apprenant = tk.Entry(self)
        self.id_apprenant.pack()
        self.label_date = tk.Label(self, text="Date :")
        self.label_date.pack()
        self.date = tk.Entry(self)
        self.date.pack()
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider)
        self.bouton_valider.pack()

    def valider(self):
        self.conn = sqlite3.connect("tp2bdd.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE COURS SET k_idMatiere = ?, joursCours = ?, heureCours = ? WHERE idCours= ?", (self.id_matiere.get(), self.id_apprenant.get(), self.date.get(), self.id.get()))
        self.conn.commit()
        self.conn.close()
        self.parent.refresh()
        self.destroy()
        ##

if __name__ == "__main__":
    app = Main()
    app.mainloop()





