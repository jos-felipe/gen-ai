import time
from time import sleep

def ft_progress(lst):
    start_time = time.time()
    total_length = len(lst)  # Armazena o comprimento total da lista

    for i, elem in enumerate(lst, start=1):  # Começa a contagem de 1
        current_time = time.time()  # Captura o tempo atual a cada iteração
        elapsed_time = current_time - start_time  # Tempo decorrido
        if i > 1:  # Para evitar divisão por zero
            iter_time = elapsed_time / i  # Tempo médio por iteração

        filled_length = int(i * 25 / total_length)  # Cálculo da parte preenchida da barra
        bar = '#' * filled_length + '-' * (25 - filled_length)  # Cria a barra

        # Cálculo da ETA
        eta = (total_length - i) * iter_time if i > 1 else 0

        # Impressão da barra de progresso
        print(
            "\rETA: {:5.2f} [{:>4.0%}] [{}] {}/{} | elapsed time {:.2f}s".format(
                eta,
                i / total_length,
                bar,
                i,
                total_length,
                elapsed_time
            ),
            end=""
        )
        yield elem  # Use 'elem' para manter a lógica intacta
        sleep(0.01)  # Simula um pequeno atraso

def main():
    a_list = range(1000)
    ret = 0
    for elem in ft_progress(a_list):
        ret += (elem + 3) % 5
    print()  # Para quebrar a linha após a barra de progresso
    print(ret)  # Exibe o resultado final

if __name__ == "__main__":
    main()
