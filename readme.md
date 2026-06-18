Vídeo do YouTube: _[cole aqui o link do vídeo, em modo público ou não listado público]_
Integrantes: Guilherme Bernardino Czelusniak e Luana Estéfani
Linguagem escolhida: Python 3.10+ testado em Python 3.12

Como executar
Requer apenas Python 3.10+ (nenhuma biblioteca externa é usada — apenas
`threading` e `time`, da biblioteca padrão).

```bash
# Parte 1 — versão ingênua (deve travar e o próprio script detecta o deadlock)
python3 parte1filosofos/filosofosdeadlock.py

# Parte 1 — versão corrigida
python3 parte1filosofos/filosofoscor.py

# Parte 2 — contador concorrente
python3 parte2semaforo/contador.py

# Parte 3 — deadlock de dois locks
python3 parte3deadlock/deadlocktrav.py

# Parte 3 — versão corrigida
python3 parte3deadlock/deadlockcor.py
```


Parte 1, o problema dos filósofos
Cinco filósofos numa mesa redonda alternam entre pensar e comer. Pra
comer, cada um precisa dos dois garfos do lado, compartilhados com os
vizinhos. Se todo mundo pegar o garfo da esquerda ao mesmo tempo e
ficar esperando o da direita, ninguém solta o que tem e o sistema
trava, isso é deadlock.
Inanição é diferente: o sistema continua rodando, só que um filósofo
específico nunca consegue comer porque os vizinhos sempre chegam
primeiro.

filosofosdeadlock.py, a versão que trava
cada filósofo pega o garfo da esquerda e depois tenta o da direita.
Usamos uma barreira pra forçar todos chegarem juntos no momento
crítico, garantindo que o travamento aconteça em toda execução.


filosofoscor.py — resolvendo o problema
Cada filósofo passa a pegar sempre o garfo de número menor primeiro e
o de número maior depois. Como todo mundo segue a mesma ordem, o
ciclo de espera nunca se forma.



 E a justiça?
 Na prática os tempos de pensar e comer variam um pouco a cada rodada,
o que evita que o mesmo filósofo fique sempre por último. Nos testes,
todos os cinco comeram o mesmo número de vezes.



Parte 2, o contador disputado entre threads
Condição de corrida
Aumentar um contador parece uma operação só, mas são três passos: ler
o valor, somar 1, escrever de volta. Se duas threads leem ao mesmo
tempo, uma sobrescreve o resultado da outra e incrementos se perdem.



Por que é difícil de ver no Python
O Python tem uma trava interna (o GIL) que normalmente esconde esse
problema. Pra deixar visível, separamos a leitura e a escrita com uma
pequena pausa entre elas.
O semáforo funciona como um cadeado: só uma thread por vez entra na
parte sensível do código, então o resultado sempre bate. O preço é
desempenho — a versão protegida ficou cerca de 8 vezes mais lenta.



Parte 3, dois cadeados travando um no outro
A Thread-1 pega o LOCK_A e tenta o LOCK_B. A Thread-2 faz o caminho
contrário. Com uma pequena pausa entre as tentativas, as duas ficam
cada uma segurando um lock e esperando o outro — deadlock.
A correção foi a mesma das outras partes: toda thread passa a pegar
sempre o LOCK_A antes do LOCK_B. O ciclo não tem como se formar se
todo mundo anda na mesma direção.
