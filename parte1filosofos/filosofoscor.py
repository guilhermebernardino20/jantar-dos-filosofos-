"""
Cada filosofo passa a requisitar sempre o garfo de menor indice
primeiro e o de maior indice depois, independente de qual seja o
"esquerdo" ou "direito". Isso impoe uma ordem parcial fixa sobre os
recursos e elimina a espera circular: nunca existira um ciclo em que
cada filosofo espera o garfo que o proximo da fila esta segurando,
porque todos percorrem os garfos na mesma ordem global.
Condicao de Coffman negada, espera circular
Para discutir justica/inanicao: como os tempos de pensar/comer sao
levemente aleatorios, na pratica os filosofos nao ficam sempre na
mesma ordem de acesso aos garfos, o que reduz bastante a chance de um
filosofo especifico ser sistematicamente preterido. O contador de
refeicoes ao final serve para verificar empiricamente essa distribuicao.
"""

import threading
import time
import random

N = 5
RODADAS = 6

forks = [threading.Lock() for _ in range(N)]
nomes = [f"Filosofo-{i}" for i in range(N)]
estado = ["pensando"] * N
refeicoes = [0] * N


def log(p, msg):
    print(f"[{time.strftime('%H:%M:%S')}] {nomes[p]}: {msg}")


def filosofo_corrigido(p):
    garfo_esq = p
    garfo_dir = (p + 1) % N
    primeiro = min(garfo_esq, garfo_dir)
    segundo = max(garfo_esq, garfo_dir)

    for _ in range(RODADAS):
        estado[p] = "pensando"
        log(p, "pensando")
        time.sleep(random.uniform(0.03, 0.1))

        estado[p] = "com fome"
        log(p, f"com fome, requisitando garfo {primeiro} (menor indice)")
        forks[primeiro].acquire()

        log(p, f"requisitando garfo {segundo} (maior indice)")
        forks[segundo].acquire()

        estado[p] = "comendo"
        refeicoes[p] += 1
        log(p, f"comendo (refeicao numero {refeicoes[p]})")
        time.sleep(random.uniform(0.03, 0.08))

        forks[segundo].release()
        forks[primeiro].release()
        estado[p] = "pensando"
        log(p, "terminou, liberou os dois garfos")


def main():
    threads = [
        threading.Thread(target=filosofo_corrigido, args=(i,), name=nomes[i])
        for i in range(N)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n" + "=" * 60)
    print("Todos os filosofos terminaram sem deadlock.")
    print("Refeicoes por filosofo:", dict(zip(nomes, refeicoes)))
    print("=" * 60)


if __name__ == "__main__":
    main()