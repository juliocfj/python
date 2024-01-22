def verificar_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

# Obter intervalo dos números a serem gerados aleatoriamente
inicio_intervalo = int(input("Digite o início do intervalo para os números aleatórios: "))
fim_intervalo = int(input("Digite o fim do intervalo para os números aleatórios: "))

# Gerar lista de números inteiros aleatórios dentro do intervalo especificado
import random
lista_numeros = [random.randint(inicio_intervalo, fim_intervalo) for _ in range(10)]

# Filtrar e exibir números primos
numeros_primos = [num for num in lista_numeros if verificar_primo(num)]
print("Lista de números aleatórios:", lista_numeros)
print("Números primos na lista:", numeros_primos)
