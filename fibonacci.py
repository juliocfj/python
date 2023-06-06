def fibonacci(n):
    """Calcula e retorna a sequência de Fibonacci até o número n."""
    sequence = [0, 1]  # Inicia com os primeiros dois números da sequência
    while sequence[-1] < n:
        next_number = sequence[-1] + sequence[-2]
        sequence.append(next_number)
    return sequence

# Exemplo de uso:
number = int(input("Digite um número limite para a sequência de Fibonacci: "))
fib_sequence = fibonacci(number)
print(fib_sequence)
