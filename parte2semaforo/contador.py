"""Desafio: contador concorrente
Demonstra uma condicao de corrida ao incrementar um contador
compartilhado a partir de varias threads sem sincronizacao, e depois
corrige o problema com um semaforo binario (1 permissao).
"""

import threading
import time

T = 8       
M = 20_000  


def tarefa_sem_sincronizacao(contador):
    for _ in range(M):
        valor_lido = contador[0]
        time.sleep(0) 
        contador[0] = valor_lido + 1


def tarefa_com_semaforo(contador, sem):
    for _ in range(M):
        sem.acquire()
        try:
            valor_lido = contador[0]
            time.sleep(0)  
            contador[0] = valor_lido + 1
        finally:
            sem.release()


def rodar_sem_sincronizacao():
    contador = [0]
    threads = [
        threading.Thread(target=tarefa_sem_sincronizacao, args=(contador,))
        for _ in range(T)
    ]
    inicio = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.perf_counter()
    return contador[0], fim - inicio


def rodar_com_semaforo():
    contador = [0]
    sem = threading.Semaphore(1) 
    threads = [
        threading.Thread(target=tarefa_com_semaforo, args=(contador, sem))
        for _ in range(T)
    ]
    inicio = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.perf_counter()
    return contador[0], fim - inicio


def main():
    esperado = T * M
    print(f"Threads (T) = {T} | Incrementos por thread (M) = {M}")
    print(f"Valor esperado (T x M) = {esperado}\n")

    print("=== VERSAO 1: SEM SINCRONIZACAO ===")
    for i in range(3):
        obtido, tempo = rodar_sem_sincronizacao()
        perda = esperado - obtido
        print(f"Execucao {i+1}: obtido={obtido}  perda={perda}  tempo={tempo:.3f}s")

    print("\n=== VERSAO 2: COM SEMAFORO BINARIO ===")
    for i in range(3):
        obtido, tempo = rodar_com_semaforo()
        print(f"Execucao {i+1}: obtido={obtido}  (correto={obtido == esperado})  tempo={tempo:.3f}s")


if __name__ == "__main__":
    main()