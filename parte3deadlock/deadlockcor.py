"""
Deadlock classico com dois locks vCorreta, hierarquia
Regra global aplicada a TODAS as threads: sempre adquirir lock A antes
de lock B, nunca na ordem inversa
condicao de Coffman quebrada: espera cirucular. Como toda thread segue a
mesma ordem de aquisicao, nunca existira uma thread que segura LOCK_B
e espera lock A enquanto outra segura lock A e espera lock B o ciclo
de espera simplesmente nao pode se formar
"""

import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def tarefa(nome):
    print(f"{nome}: tentando LOCK_A")
    LOCK_A.acquire()
    print(f"{nome}: adquiriu LOCK_A")
    time.sleep(0.1)

    print(f"{nome}: tentando LOCK_B")
    LOCK_B.acquire()
    print(f"{nome}: adquiriu LOCK_B, executando secao critica")
    time.sleep(0.05)

    LOCK_B.release()
    LOCK_A.release()
    print(f"{nome}: concluiu e liberou os dois locks")


def main():
    t1 = threading.Thread(target=tarefa, args=("Thread-1",), name="Thread-1")
    t2 = threading.Thread(target=tarefa, args=("Thread-2",), name="Thread-2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("\n" + "=" * 60)
    print("Ambas as threads terminaram SEM deadlock.")
    print("=" * 60)


if __name__ == "__main__":
    main()