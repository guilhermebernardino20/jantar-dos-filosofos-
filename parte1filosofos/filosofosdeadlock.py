"""
(com deadlock)
Cada filosofo tenta pegar primeiro o garfo da esquerda e depois o da
direita. Uma barreira forca todos os filosofos a pegarem o garfo da
esquerda quase ao mesmo tempo, e uma pequena pausa antes de tentar o
garfo da direita aumenta bastante a chance de deadlock (espera circular).
Se nenhuma thread terminar dentro do tempo limite, um "watchdog" detecta
e relata o deadlock, mostrando quais filosofos ficaram bloqueados.
"""

import threading
import time
import random

N = 5 
TIMEOUT_WATCHDOG = 8

forks = [threading.Lock() for _ in range(N)]
nomes = [f"Filosofo-{i}" for i in range(N)]
estado = ["pensando"] * N


def log(p, msg):
    print(f"[{time.strftime('%H:%M:%S')}] {nomes[p]}: {msg}")


def filosofo_naive(p, barreira, rodadas=2):
    esquerda = p
    direita = (p + 1) % N

    for _ in range(rodadas):
        estado[p] = "pensando"
        log(p, "pensando")
        time.sleep(random.uniform(0.05, 0.15))

        estado[p] = "com fome"
        log(p, "com fome, vou tentar o garfo esquerdo")

    
        barreira.wait()

        forks[esquerda].acquire()
        log(p, f"pegou o garfo {esquerda} (esquerdo)")
        time.sleep(0.2) 

        log(p, f"tentando o garfo {direita} (direito)...")
        forks[direita].acquire()  

        estado[p] = "comendo"
        log(p, "pegou os dois garfos, comendo")
        time.sleep(random.uniform(0.05, 0.1))

        forks[direita].release()
        forks[esquerda].release()
        estado[p] = "pensando"
        log(p, "terminou de comer, liberou os garfos")


def main():
    barreira = threading.Barrier(N)
    threads = [
        threading.Thread(target=filosofo_naive, args=(i, barreira), name=nomes[i], daemon=True)
        for i in range(N)
    ]

    for t in threads:
        t.start()

    inicio_espera = time.time()
    for t in threads:
        restante = TIMEOUT_WATCHDOG - (time.time() - inicio_espera)
        t.join(timeout=max(restante, 0))

    travadas = [t for t in threads if t.is_alive()]

    print("\n" + "=" * 60)
    if travadas:
        print("Teve Deadlock")
        print(f"{len(travadas)} threads ainda bloqueada apos {TIMEOUT_WATCHDOG}s de espera")
        print("Threads presas, espera circular pelos garfos:")
        for t in travadas:
            print(f"  - {t.name}")
        print(
            "\nExplicacao: cada filosofo travado esta com o garfo esquerdo em "
            "maos e aguardando o garfo direito, que pertence ao vizinho  "
            "tambem travado da mesma forma. Isso forma um ciclo de espera "
            "espera circular, uma das quatro condicoes de Coffman."
        )
    else:
        print("Todos os filosofos terminaram sem deadlock nesta execucao.")
        print(
            "(Pode acontecer ocasionalmente dependendo do timing do SO; "
            "execute novamente para observar o travamento.)"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()