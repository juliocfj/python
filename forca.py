import random

def jogo_da_forca():
    # Lista de palavras para o jogo
    palavras = ["python", "java", "programacao", "algoritmo", "computador", "desafio", "inteligencia"]

    # Escolhe uma palavra aleatória
    palavra = random.choice(palavras)
    letras_descobertas = ["_"] * len(palavra)
    tentativas = 6
    letras_tentadas = set()

    print("=== Jogo da Forca ===")
    print("Voce tem 6 tentativas para adivinhar a palavra.\n")

    while tentativas > 0 and "_" in letras_descobertas:
        print("Palavra:", " ".join(letras_descobertas))
        print(f"Tentativas restantes: {tentativas}")
        print(f"Letras ja tentadas: {', '.join(sorted(letras_tentadas))}\n")

        chute = input("Digite uma letra: ").lower()

        if len(chute) != 1 or not chute.isalpha():
            print("Atenção: digite apenas UMA letra valida!\n")
            continue

        if chute in letras_tentadas:
            print("Atenção: voce ja tentou essa letra!\n")
            continue

        letras_tentadas.add(chute)

        if chute in palavra:
            print("Correto! A letra existe na palavra.\n")
            for i, letra in enumerate(palavra):
                if letra == chute:
                    letras_descobertas[i] = chute
        else:
            print("Errado! Essa letra nao existe na palavra.\n")
            tentativas -= 1

    if "_" not in letras_descobertas:
        print(f"Parabens! Voce adivinhou a palavra: {palavra}")
    else:
        print(f"Game Over! A palavra era: {palavra}")

if __name__ == "__main__":
    jogo_da_forca()
