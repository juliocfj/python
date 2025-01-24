import random

# Lista de raças e seus bônus
races = {
    "Humano": {},
    "Elfo": {"Destreza": 2, "Inteligência": 1},
    "Anão": {"Constituição": 2, "Força": 1},
    "Halfling": {"Destreza": 2, "Carisma": 1},
    "Tiefling": {"Inteligência": 1, "Carisma": 2},
    "Dragonborn": {"Força": 2, "Carisma": 1},
    "Gnomo": {"Inteligência": 2},
    "Orc": {"Força": 2, "Constituição": 1},
    "Tabaxi": {"Destreza": 2, "Carisma": 1},
    "Aarakocra": {"Destreza": 2, "Sabedoria": 1}
}

# Lista de classes
classes = [
    "Guerreiro", "Mago", "Ladino", "Clérigo", "Paladino", "Druida",
    "Bárbaro", "Bardo", "Feiticeiro", "Bruxo", "Ranger", "Monge", "Artífice"
]

# Atributos principais
attributes = ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]

def roll_attributes():
    """Gera atributos aleatórios entre 8 e 18."""
    return {attr: random.randint(8, 18) for attr in attributes}

def apply_race_bonus(base_attributes, race):
    """Aplica os bônus da raça escolhida nos atributos."""
    bonuses = races[race]
    for attr, bonus in bonuses.items():
        base_attributes[attr] += bonus
    return base_attributes

def create_character():
    """Cria um personagem com base nas escolhas do jogador ou aleatoriamente."""
    print("Bem-vindo ao Gerador de Personagens de RPG!")
    
    # Escolha ou geração aleatória de raça
    print("Escolha uma raça ou digite 'aleatório' para gerar automaticamente:")
    for race in races.keys():
        print(f"- {race}")
    chosen_race = input("Raça: ").capitalize()
    if chosen_race not in races.keys() and chosen_race != "Aleatório":
        print("Raça inválida. Gerando aleatoriamente.")
        chosen_race = "Aleatório"
    if chosen_race == "Aleatório":
        chosen_race = random.choice(list(races.keys()))

    # Escolha ou geração aleatória de classe
    print("\nEscolha uma classe ou digite 'aleatório' para gerar automaticamente:")
    for cls in classes:
        print(f"- {cls}")
    chosen_class = input("Classe: ").capitalize()
    if chosen_class not in classes and chosen_class != "Aleatório":
        print("Classe inválida. Gerando aleatoriamente.")
        chosen_class = "Aleatório"
    if chosen_class == "Aleatório":
        chosen_class = random.choice(classes)

    # Geração de atributos
    base_attributes = roll_attributes()
    final_attributes = apply_race_bonus(base_attributes, chosen_race)

    # Exibir resultado
    print("\nSeu personagem foi criado!")
    print(f"Raça: {chosen_race}")
    print(f"Classe: {chosen_class}")
    print("Atributos:")
    for attr, value in final_attributes.items():
        print(f"  {attr}: {value}")

    return {
        "Raça": chosen_race,
        "Classe": chosen_class,
        "Atributos": final_attributes
    }

if __name__ == "__main__":
    while True:
        create_character()
        cont = input("\nDeseja criar outro personagem? (s/n): ").lower()
        if cont != "s":
            print("Até a próxima!")
            break
