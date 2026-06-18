Vídeo do YouTube: _[cole aqui o link do vídeo, em modo público ou não listado público]_
Integrantes: Guilherme Bernardino Czelusniak e Luana Estéfani
Linguagem escolhida: Python 3.10+ (testado em Python 3.12

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


## Parte 1 — o problema dos filósofos

Cinco filósofos sentam numa mesa redonda e ficam alternando entre
pensar e comer. Pra comer, cada um precisa dos dois garfos do lado,
que são compartilhados com os vizinhos. Se todo mundo pegar primeiro
o garfo da esquerda e só depois tentar o da direita, pode acontecer
de todos pegarem o esquerdo ao mesmo tempo e ficarem esperando pra
sempre o direito — que está na mão do vizinho, esperando a mesma
coisa. Ninguém solta o que já tem, e como todos precisam dos dois
garfos pra comer, a coisa trava: um espera o outro, que espera o
outro, até fechar um ciclo. Isso é deadlock.

Inanição é diferente: o sistema continua rodando normalmente, só que
um filósofo específico nunca consegue comer porque os vizinhos
sempre chegam primeiro. Não trava nada, só é injusto com ele.

### `filosofos_deadlock.py` — a versão que trava

Cada filósofo pega o garfo da esquerda e depois tenta o da direita.
Pra garantir que o travamento aconteça de verdade (e não dependa de
sorte), usamos uma barreira que faz os cinco chegarem juntos no
momento de pegar o primeiro garfo, com uma pequena pausa antes de
tentar o segundo. O programa espera um tempo e, se ninguém terminou,
mostra quem travou e por quê.
[14:19:12] Filosofo-4: tentando o garfo 0 (direito)...

[14:19:12] Filosofo-3: tentando o garfo 4 (direito)...
============================================================

*** DEADLOCK DETECTADO ***

5 thread(s) ainda bloqueada(s) apos 8s de espera.

Threads presas (espera circular pelos garfos):

Filosofo-0
Filosofo-1
Filosofo-2
Filosofo-3
Filosofo-4

Explicacao: cada filosofo travado esta com o garfo esquerdo em maos e

aguardando o garfo direito, que pertence ao vizinho - tambem travado da

mesma forma. Isso forma um ciclo de espera (espera circular), uma das

quatro condicoes de Coffman.

Os cinco ficaram com o garfo esquerdo na mão esperando o direito do
vizinho — o ciclo se fechou.

### `filosofos_corrigido.py` — resolvendo o problema

A solução: em vez de pegar sempre o garfo da esquerda primeiro, cada
filósofo passa a pegar sempre o de número menor primeiro, e depois o
de número maior. Como todo mundo segue essa mesma ordem, o ciclo
nunca mais se forma — sempre tem alguém conseguindo o segundo garfo
livre.
primeiro = garfo de numero menor entre os dois do filosofo

segundo  = garfo de numero maior
pensa, pega o primeiro, pega o segundo, come, solta os dois

[14:19:20] Filosofo-4: com fome, requisitando garfo 0 (menor indice)

[14:19:20] Filosofo-0: terminou, liberou os dois garfos

[14:19:20] Filosofo-4: requisitando garfo 4 (maior indice)

[14:19:20] Filosofo-4: comendo (refeicao numero 6)

[14:19:20] Filosofo-4: terminou, liberou os dois garfos


Todos os filosofos terminaram SEM deadlock.

Refeicoes por filosofo: {'Filosofo-0': 6, 'Filosofo-1': 6, 'Filosofo-2': 6, 'Filosofo-3': 6, 'Filosofo-4': 6}

### E a justiça?

Isso resolve o travamento, mas não garante 100% que um filósofo nunca
fique sempre por último. Na prática, como os tempos de pensar e comer
variam um pouco, isso já evita que alguém fique sempre em
desvantagem — nos testes, todos os cinco comeram exatamente o mesmo
número de vezes.

---

## Parte 2 — o contador disputado entre threads

### Condição de corrida

Acontece quando duas threads usam a mesma informação ao mesmo tempo e
o resultado depende de quem chega primeiro. Aumentar o contador em 1
parece uma coisa só, mas são três passos: ler o valor, somar 1,
escrever de volta. Se a thread A lê antes de B escrever, a
atualização de B se perde.

### Por que isso é difícil de ver no Python

O Python tem uma trava interna (o GIL) que só deixa uma thread rodar
por vez, e isso normalmente esconde esse tipo de erro. Pra forçar o
problema a aparecer de verdade, separamos a leitura e a escrita do
contador e colocamos uma pequena pausa entre elas.

### Resultados reais (8 threads, 20 mil incrementos cada)

| Versão | Execução | Esperado | Obtido | Perdido | Tempo |
|---|---|---|---|---|---|
| Sem proteção | 1 | 160.000 | 20.010 | 139.990 | 1.618s |
| Sem proteção | 2 | 160.000 | 20.005 | 139.995 | 1.594s |
| Sem proteção | 3 | 160.000 | 20.003 | 139.997 | 1.580s |
| Com semáforo | 1 | 160.000 | 160.000 | 0 | 13.731s |
| Com semáforo | 2 | 160.000 | 160.000 | 0 | 13.835s |
| Com semáforo | 3 | 160.000 | 160.000 | 0 | 14.072s |

### Por que a versão sem proteção falha

Com a pausa entre ler e escrever, várias threads acabam lendo o mesmo
valor antes de qualquer uma escrever o resultado atualizado. Todas
escrevem "valor antigo + 1", e vários incrementos se perdem.

### Por que o semáforo resolve

O semáforo funciona como um cadeado: só uma thread entra na parte
sensível por vez. Ler e escrever sempre termina antes da próxima
thread começar, e o resultado final fica certo nas três execuções.

### O preço que se paga

A versão protegida ficou de 8 a 9 vezes mais lenta. Faz sentido: o
trabalho que seria paralelo passa a ser feito praticamente um por
vez. É o preço de garantir que o resultado está certo.

### E a visibilidade entre threads?

Em Java existe uma garantia formal de que o que uma thread escreve
antes de liberar o semáforo aparece certinho pra próxima thread que
pegar ele. No Python isso também acontece na prática, por causa do
próprio GIL e das travas do sistema por baixo dos panos.



Parte 3
Contexto
A Thread-1 pega o LOCK_A e tenta o LOCK_B. A Thread-2 pega o LOCK_B e
tenta o LOCK_A. Com uma pequena pausa entre as duas tentativas,
garantimos que as duas já estão com o primeiro lock antes de tentar o
segundo — o travamento fica praticamente garantido.


o programa percebe sozinho, depois de um tempo, que ninguém terminou
A solução: toda thread passa a pegar sempre o LOCK_A antes do LOCK_B,
nunca o contrário. Assim nunca existe uma esperando o B enquanto a
outra espera o A — o ciclo não se forma.
A Thread-2 chega a tentar o LOCK_A enquanto a Thread-1 ainda está com
ele, mas ela só espera a vez — não existe mais ninguém travando o que
o outro precisa.

---