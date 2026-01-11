import random
import time
import sys
import os

# --- Classe du Joueur ---
class Sujet47:
    def __init__(self, nom):
        self.nom = nom
        self.pv = 80
        self.faim = 40
        self.soif = 30
        self.stress = 30
        self.infection = 0
        self.relations = 50
        self.inventaire = ["Couteau rouillé", "Lampe torche (batterie: 30%)"]
        self.objets_spéciaux = []
        self.jour = 1
        self.zone_actuelle = "Rues en ruine"
        self.postits = []
        self.est_en_vie = True
        self.a_trouvé_remède = False
        self.a_tué_gardien = False

    def mettre_a_jour_stats(self):
        # Faim/Soif = perte de PV
        if self.faim >= 70:
            self.pv -= 3
            print(f"🍖 {self.nom} a trop faim ! (-3 PV)")
        if self.soif >= 60:
            self.pv -= 4
            self.stress += 10
            print(f"💧 {self.nom} a soif ! (-4 PV, +10 stress)")
        # Infection
        if self.infection > 0:
            self.pv -= 2
            self.stress += 15
            print(f"🦠 Infection : -2 PV, +15 stress.")
        # Stress = folie
        if self.stress >= 100:
            print(f"🧠 {self.nom} SOMBRE DANS LA FOLIE. GAME OVER.")
            self.est_en_vie = False
        # Relations
        if self.relations <= 10:
            print(f"👥 Tout le monde vous déteste. Les PNJ vous attaquent à vue.")
        # PV = mort
        if self.pv <= 0:
            print(f"💀 {self.nom} est mort. GAME OVER.")
            self.est_en_vie = False

    def boire(self, source):
        if source == "eau sale":
            self.soif = max(0, self.soif - 20)
            if random.random() < 0.8:  # 80% de chance d'infection
                self.infection += 15
                print(f"🦠 L'eau était contaminée ! Infection +15.")
        elif source == "eau pure":
            self.soif = max(0, self.soif - 40)
            print(f"💧 Vous buvez une eau pure. Soif: {self.soif}.")
        self.mettre_a_jour_stats()

    def manger(self, nourriture):
        if nourriture == "ration militaire":
            self.faim = max(0, self.faim - 30)
            if random.random() < 0.5:  # 50% de chance d'être avariée
                self.pv -= 10
                print(f"🍖 La ration était avariée ! -10 PV. Faim: {self.faim}.")
            else:
                print(f"🍖 Manger une ration. Faim: {self.faim}.")
        elif nourriture == "champignon mutant":
            self.faim = max(0, self.faim - 50)
            self.pv -= random.randint(15, 25)
            self.stress += 20
            print(f"🍄 Champignon toxique ! Faim: {self.faim}, -{random.randint(15, 25)} PV, +20 stress.")
        elif nourriture == "potion de soin":
            self.pv = min(80, self.pv + 20)
            self.inventaire.remove("potion de soin")
            print(f"💊 Potion utilisée ! PV: {self.pv}.")
        self.mettre_a_jour_stats()

    def dormir(self):
        print(f"😴 {self.nom} tente de dormir...")
        if random.random() < 0.7:  # 70% de cauchemars
            self.stress += 25
            print(f"⚠️ Cauchemars ! +25 stress.")
        else:
            self.stress = max(0, self.stress - 20)
            print(f"😌 Repos réparateur. Stress: {self.stress}.")
        self.jour += 1
        self.faim += 25
        self.soif += 30
        self.mettre_a_jour_stats()

    def trouver_postit(self):
        postit = random.choice([
            "TOUTE L'EAU EST EMPOISONNÉE. MÊME CELLE QUE TU VIENS DE BOIRE.",
            "LE GARDIEN EST UNE PARTIE DE TOI. TU NE PEUX PAS LE TUER.",
            "Tu es le sujet #47. Les autres ont tenu 2 jours max.",
            "Ne dors pas. NE DORS JAMAIS. ILS ARRIVENT QUAND TU DORS.",
            "Les champignons te rendent plus fort... ou te tuent. (Ils te tueront.)",
            "Le couteau est inutile. Comme ton espoir. Comme toi.",
            "Éteins la lampe. ILS TE VOIENT AVEC LA LUMIÈRE. ILS TE VOIENT SANS ELLE.",
            "Tu as déjà essayé 12 fois. Tu vas encore mourir. Comme toujours.",
            "La sortie n'existe pas. C'est une boucle. Comme toi.",
            "NE FAIS CONFIANCE À PERSONNE. PAS MÊME À CE MESSAGE."
        ])
        self.postits.append(postit)
        print(f"\n📝 POST-IT TROUVÉ : '{postit}'")

    def afficher_stats(self):
        print(f"""
        === JOUR {self.jour} - {self.zone_actuelle} ===
        🩸 PV: {self.pv}
        🍖 Faim: {self.faim}
        💧 Soif: {self.soif}
        🧠 Stress: {self.stress}
        🦠 Infection: {self.infection}
        👥 Relations: {self.relations}
        🎒 Inventaire: {', '.join(self.inventaire)}
        📝 Post-it: {len(self.postits)}
        """)

# --- Zones du Jeu ---
zones = {
    "Rues en ruine": {
        "description": "Des bâtiments effondrés. Des ombres bougent. *Ils t'observent.*",
        "ressources": ["ration militaire", "eau sale", "champignon mutant", "batterie usagée"],
        "ennemis": ["Mutant affamé", "Drone corrompu", "Ombre"],
        "événements": ["trouver_postit", "rencontre_pnj", "piège", "hallucination", "rien"]
    },
    "Hôpital abandonné": {
        "description": "Odeur de mort. Des cris étouffés. *Quelque chose respire derrière toi.*",
        "ressources": ["antibiotiques", "eau pure", "seringue", "potion de soin"],
        "ennemis": ["Infirmière mutante", "Chirurgien fou", "Patient 0"],
        "événements": ["trouver_postit", "hallucination", "piège", "combat_boss", "rien"]
    },
    "Usine de traitement": {
        "description": "Machines rouillées. Un bourdonnement sinistre. *Tu entends ton nom.*",
        "ressources": ["batterie", "circuits", "arme improvisée", "clé USB"],
        "ennemis": ["Robot de sécurité", "IA corrompue", "Gardien (mini-boss)"],
        "événements": ["trouver_postit", "combat_boss", "piège", "hallucination", "rien"]
    },
    "Égouts": {
        "description": "Obscurité totale. *Quelque chose respire dans le noir.*",
        "ressources": ["champignon mutant", "clé rouillée", "eau sale"],
        "ennemis": ["Créature des égouts", "Rats mutants", "L'Ombre qui te suit"],
        "événements": ["trouver_postit", "hallucination", "rencontre_pnj", "piège", "rien"]
    },
    "Laboratoire secret": {
        "description": "Lumière bleutée. Des écrans affichent 'PROTOCOLE ÉCHEC : SUJET #47'.",
        "ressources": ["remède", "données classifiées", "arme énergétique"],
        "ennemis": ["LE GARDIEN"],
        "événements": ["fin_du_jeu"]
    }
}

# --- Ennemis ---
class Ennemi:
    def __init__(self, nom, pv, attaque, dialogue):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.dialogue = dialogue

    def attaquer(self, joueur):
        dégats = random.randint(5, self.attaque)
        joueur.pv -= dégats
        joueur.stress += random.randint(15, 25)
        print(f"{self.nom} vous attaque ! {dégats} dégâts, +{random.randint(15, 25)} stress.")
        joueur.mettre_a_jour_stats()

class MutantAffamé(Ennemi):
    def __init__(self):
        super().__init__("Mutant affamé", 60, 20, ["*Un rire déformé...*"])

class ChirurgienFou(Ennemi):
    def __init__(self):
        super().__init__("Chirurgien fou", 90, 25, ["'Un nouveau cobaye !'"])

class Gardien(Ennemi):
    def __init__(self):
        super().__init__("LE GARDIEN", 300, 40, ["'Tu ne passes pas.'", "*Son visage se déforme...*"])

class Ombre(Ennemi):
    def __init__(self):
        super().__init__("L'Ombre", 1, 30, ["*Tu sens une présence derrière toi...*"])

# --- PNJ ---
class PNJ:
    def __init__(self, nom, dialogue, relation_bonus, objet_donné=None):
        self.nom = nom
        self.dialogue = dialogue
        self.relation_bonus = relation_bonus
        self.objet_donné = objet_donné

    def interagir(self, joueur):
        for ligne in self.dialogue:
            print(ligne)
            time.sleep(1)
        joueur.relations += self.relation_bonus
        if self.objet_donné and random.random() < 0.5:  # 50% de chance de donner l'objet
            joueur.inventaire.append(self.objet_donné)
            print(f"🎁 {self.nom} vous donne: {self.objet_donné}.")
        else:
            print(f"👥 {self.nom} ne vous donne rien. Il/elle vous regarde avec mépris.")
        print(f"👥 Relations: {joueur.relations}")

class MédecinRebelle(PNJ):
    def __init__(self):
        super().__init__(
            "Dr. Elena",
            [
                "'Je peux vous aider... mais ça va vous coûter.'",
                "'Prenez ça. C'est tout ce qu'il me reste.'",
                "*Elle chuchote : 'Ne fais pas confiance au Chirurgien.'*"
            ],
            10,
            "potion de soin"
        )

class SurvivantFou(PNJ):
    def __init__(self):
        super().__init__(
            "L'Homme aux yeux vides",
            [
                "'Ils nous observent...'",
                "'Ne va pas dans les égouts. J'AI VU DES CHOSES LA-BAS.'",
                "*Il rit hystériquement, puis se met à pleurer.*"
            ],
            -20,
            None
        )

# --- Combat ---
def combat(joueur, ennemi):
    print(f"\n⚔️ COMBAT : {joueur.nom} vs {ennemi.nom} ⚔️")
    for ligne in ennemi.dialogue:
        print(ligne)
        time.sleep(1)
    while joueur.pv > 0 and ennemi.pv > 0 and joueur.est_en_vie:
        joueur.afficher_stats()
        print(f"{ennemi.nom} : {ennemi.pv} PV")
        print("1. Attaquer (50% de réussite)")
        print("2. Fuir (40% de réussite)")
        print("3. Utiliser un objet")
        choix = input("Que faire ? ").strip()
        if choix == "1":
            if random.random() < 0.5:  # 50% de réussite
                dégats = random.randint(5, 12)
                ennemi.pv -= dégats
                print(f"✅ Vous infligez {dégats} dégâts !")
            else:
                print("❌ *Vous ratez votre attaque.*")
        elif choix == "2":
            if random.random() < 0.4:  # 40% de réussite
                print("✅ Vous fuyez !")
                joueur.stress += 15
                break
            else:
                print("❌ L'ennemi vous bloque !")
        elif choix == "3":
            print(f"Inventaire: {', '.join(joueur.inventaire)}")
            objet = input("Utiliser quel objet ? ").strip()
            if objet in joueur.inventaire:
                if objet == "potion de soin":
                    joueur.manger("potion de soin")
                elif objet == "arme improvisée":
                    dégats = random.randint(10, 20)
                    ennemi.pv -= dégats
                    joueur.inventaire.remove(objet)
                    print(f"✅ Vous infligez {dégats} dégâts avec l'arme improvisée !")
                elif objet == "arme énergétique":
                    dégats = random.randint(25, 40)
                    ennemi.pv -= dégats
                    print(f"✅ Vous infligez {dégats} dégâts avec l'arme énergétique !")
        # L'ennemi attaque toujours
        ennemi.attaquer(joueur)
        # Événement aléatoire
        if random.random() < 0.3:
            événement = random.choice(["hallucination", "piège", "renforts"])
            if événement == "hallucination":
                print("\n⚠️ *Votre vision se trouble... Vous voyez des choses.*")
                joueur.stress += 25
            elif événement == "piège":
                print("\n💣 *Un piège explose !* -15 PV.")
                joueur.pv -= 15
            elif événement == "renforts":
                print(f"\n⚠️ Un {random.choice(['Mutant', 'Drone'])} arrive en renfort !")
                combat(joueur, MutantAffamé())
    if ennemi.pv <= 0:
        print(f"\n{ennemi.nom} est vaincu !")
        if isinstance(ennemi, Gardien):
            joueur.a_tué_gardien = True
            print("\n🔴 *Le Gardien s'effondre... Une porte rouge apparaît.*")
            print("'Félicitations. Tu as terminé le protocole.'")
            joueur.a_trouvé_remède = True
    else:
        print(f"\n💀 {joueur.nom} est vaincu.")

# --- Exploration ---
def explorer(joueur):
    zone = zones[joueur.zone_actuelle]
    print(f"\n--- {joueur.zone_actuelle} ---")
    print(zone["description"])
    événement = random.choice(zone["événements"])
    if événement == "trouver_postit":
        joueur.trouver_postit()
    elif événement == "rencontre_pnj":
        pnj = random.choice([MédecinRebelle(), SurvivantFou()])
        pnj.interagir(joueur)
    elif événement == "piège":
        print("\n💣 *Un piège se déclenche !* -20 PV.")
        joueur.pv -= 20
    elif événement == "hallucination":
        print("\n🌀 *Tu entends des chuchotements... 'Abandonne.'* +25 stress.")
        joueur.stress += 25
    elif événement == "combat_boss":
        combat(joueur, Gardien())
    elif événement == "rien":
        print("\n*Rien ne se passe. Mais tu sens que quelque chose ne va pas.*")
    # Ressources aléatoires
    if random.random() < 0.4:  # 40% de chance de trouver une ressource
        ressource = random.choice(zone["ressources"])
        joueur.inventaire.append(ressource)
        print(f"\n🎒 Vous trouvez: {ressource}.")
    # Ennemis aléatoires
    if random.random() < 0.7 and joueur.zone_actuelle != "Laboratoire secret":
        ennemi = random.choice([
            MutantAffamé(),
            ChirurgienFou(),
            Ombre()
        ])
        combat(joueur, ennemi)
    # Mise à jour des stats
    joueur.faim += random.randint(15, 25)
    joueur.soif += random.randint(20, 30)
    joueur.stress += random.randint(5, 15)
    joueur.mettre_a_jour_stats()

# --- Fin du Jeu ---
def fin_du_jeu(joueur):
    print("\n=== ÉVALUATION FINALE ===")
    if joueur.pv <= 0:
        print("💀 TU ES MORT. Comme les 46 sujets avant toi.")
    elif joueur.stress >= 100:
        print("🧠 TON ESPRIT A CÉDÉ. La simulation continue sans toi.")
    elif joueur.a_trouvé_remède:
        print("🌌 TU AS TROUVÉ LA SORTIE.")
        print("'Protocole Échec terminé. Sujet #47: Réussi.'")
        print("'Mais était-ce réel ?'")
    else:
        print("⏳ TEMPS ÉCOULÉ. Tu n'as pas trouvé la sortie à temps.")
    print("\n🔄 Voulez-vous recommencer ? (O/N)")
    if input().strip().lower() == "o":
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        print("'Fin de la simulation.'")
        sys.exit()

# --- Boucle Principale ---
def main():
    print("""
    🔥🔥🔥 NÉO-TERRA : PROTOCOLE ÉCHEC ABSOLU 🔥🔥🔥
    --- UNE SIMULATION CONÇUE POUR TE DÉTRUIRE ---
    """)
    joueur = Sujet47(input("Nom du sujet : "))
    while joueur.est_en_vie and joueur.jour <= 7:
        joueur.afficher_stats()
        print("\n1. Explorer la zone")
        print("2. Boire")
        print("3. Manger")
        print("4. Dormir")
        print("5. Lire les post-it")
        print("6. Changer de zone")
        print("7. Voir les objets spéciaux")
        choix = input("Que faire ? ").strip()
        if choix == "1":
            explorer(joueur)
        elif choix == "2":
            if "eau pure" in joueur.inventaire:
                joueur.boire("eau pure")
            elif "eau sale" in joueur.inventaire:
                joueur.boire("eau sale")
            else:
                print("❌ Rien à boire.")
        elif choix == "3":
            if "ration militaire" in joueur.inventaire:
                joueur.manger("ration militaire")
            elif "champignon mutant" in joueur.inventaire:
                joueur.manger("champignon mutant")
            elif "potion de soin" in joueur.inventaire:
                joueur.manger("potion de soin")
            else:
                print("❌ Rien à manger.")
        elif choix == "4":
            joueur.dormir()
        elif choix == "5":
            print("\n📝 POST-IT TROUVÉS :")
            for postit in joueur.postits:
                print(f"- {postit}")
        elif choix == "6":
            print("\n🚪 Zones disponibles :")
            for i, zone in enumerate(zones.keys()):
                print(f"{i+1}. {zone}")
            nouvelle_zone = input("Où aller ? (1-5) ").strip()
            if nouvelle_zone in ["1", "2", "3", "4", "5"]:
                joueur.zone_actuelle = list(zones.keys())[int(nouvelle_zone)-1]
                print(f"\n🚪 Vous entrez dans {joueur.zone_actuelle}...")
                if joueur.zone_actuelle == "Laboratoire secret":
                    combat(joueur, Gardien())
            else:
                print("❌ Choix invalide.")
        elif choix == "7":
            print(f"\n🔹 Objets spéciaux: {', '.join(joueur.objets_spéciaux)}")
        # Vérifier les conditions de game over
        if not joueur.est_en_vie or joueur.jour > 7:
            break
    fin_du_jeu(joueur)

if __name__ == "__main__":
    main()
