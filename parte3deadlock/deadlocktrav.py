"""
Deadlock classico dois locks vTrava
Thread 1 adquire lockA e depois tenta lockB
Thread 2 adquire lockB e depois tenta lockB
Um pequeno sleep entre as duas aquisicoes torna o deadlock praticamente
garantido: cada thread fica presa segurando um lock e esperando o outro
Um watchdog com timeout detecta a situacao e imprime quais condicoes
de Coffman se manifestaram
"""

import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()
TIMEOUT_WATCHDOG = 5


def thread1_trava():
    print("Thread-1: tentando LOCK_A")
    LOCK_A.acquire()
    print("Thread-1: adquiriu LOCK_A")
    time.sleep(0.1)  # da tempo para a Thread-2 pegar o LOCK_B
    print("Thread-1: tentando LOCK_B...")
    LOCK_B.acquire()
    print("Thread-1: concluiu")
    LOCK_B.release()
    LOCK_A.release()


def thread2_trava():
    print("Thread-2: tentando LOCK_B")
    LOCK_B.acquire()
    print("Thread-2: adquiriu LOCK_B")
    time.sleep(0.1)
    print("Thread-2: tentando LOCK_A...")
    LOCK_A.acquire()
    print("Thread-2: concluiu")
    LOCK_A.release()
    LOCK_B.release()


def main():
    t1 = threading.Thread(target=thread1_trava, name="Thread-1", daemon=True)
    t2 = threading.Thread(target=thread2_trava, name="Thread-2", daemon=True)
    t1.start()
    t2.start()

    inicio_espera = time.time()
    t1.join(timeout=TIMEOUT_WATCHDOG)
    restante = TIMEOUT_WATCHDOG - (time.time() - inicio_espera)
    t2.join(timeout=max(restante, 0))

    print("\n" + "=" * 60)
    travadas = [t for t in (t1, t2) if t.is_alive()]
    if travadas:
        print("*** DEADLOCK DETECTADO ***")
        print(f"Threads ainda bloqueadas apos {TIMEOUT_WATCHDOG}s:")
        for t in travadas:
            print(f"  - {t.name}")
        print("\nCondicoes de Coffman presentes nesta execucao:")
        print("  1) Exclusao mutua    -> cada lock so pode ser detido por uma thread por vez")
        print("  2) Manter-e-esperar  -> cada thread mantem seu lock enquanto espera o outro")
        print("  3) Nao preempcao     -> nenhum lock pode ser tomado a forca de quem o detem")
        print("  4) Espera circular   -> Thread-1 espera LOCK_B (com Thread-2) e")
        print("                          Thread-2 espera LOCK_A (com Thread-1)")
    else:
        print("As threads terminaram sem deadlock nesta execucao (timing pode variar).")
    print("=" * 60)


if __name__ == "__main__":
    main()