"""
Template para o Problema do Produtor-Consumidor
================================================

INSTRUÇÕES:
Complete este template seguindo o checklist da atividade.
Preencha as seções marcadas com TODO.

Nome do Aluno: Rodrigo Soares
Data: 01/02/2026
"""

import threading
import time
import random
from threading import Semaphore, Lock

# ============================
# CONFIGURAÇÕES
# ============================

TAMANHO_BUFFER = 10           # Capacidade máxima do buffer
NUM_PRODUTORES = 2            # Número de threads produtoras
NUM_CONSUMIDORES = 2          # Número de threads consumidoras
NUM_ITENS_POR_THREAD = 10     # Quantos itens cada produtor/consumidor processa

# ============================
# ESTRUTURAS DE DADOS COMPARTILHADAS
# ============================

buffer = []

# Semáforo para itens disponíveis (inicializado com 0)
itens_disponiveis = Semaphore(0)

# Semáforo para espaços vazios (inicializado com o tamanho máximo)
espacos_vazios = Semaphore(TAMANHO_BUFFER)

# Lock para proteger o acesso ao buffer (Região Crítica)
lock = Lock()

# ============================
# FUNÇÃO PRODUTOR
# ============================

def produtor(id_produtor):
    """
    Função executada por cada thread produtora.
    """
    for i in range(NUM_ITENS_POR_THREAD):
        # Gera um item aleatório entre 1 e 100
        item = random.randint(1, 100)
        
        # Aguarda por um espaço vazio no buffer
        espacos_vazios.acquire()
        
        # Adquira o lock para acessar o buffer de forma exclusiva
        lock.acquire()
        
        try:
            # Adiciona o item ao final da lista
            buffer.append(item)
            print(f"📦 Produtor {id_produtor} produziu item {item}. Buffer: {len(buffer)}/{TAMANHO_BUFFER}")
        finally:
            # Libera o lock sempre, mesmo se houver erro
            lock.release()
        
        # Sinalize que há um novo item disponível para consumo
        itens_disponiveis.release()
        
        # Simula o tempo de produção
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"✅ Produtor {id_produtor} finalizou seu trabalho.")

# ============================
# FUNÇÃO CONSUMIDOR
# ============================

def consumidor(id_consumidor):
    """
    Função executada por cada thread consumidora.
    """
    for i in range(NUM_ITENS_POR_THREAD):
        # Aguarda por um item disponível no buffer
        itens_disponiveis.acquire()
        
        # Adquira o lock para acessar o buffer de forma exclusiva
        lock.acquire()
        
        try:
            # Remova o primeiro item do buffer (FIFO)
            item = buffer.pop(0)
            print(f"🍴 Consumidor {id_consumidor} consumiu item {item}. Buffer: {len(buffer)}/{TAMANHO_BUFFER}")
        finally:
            # Libera o lock
            lock.release()
        
        # Sinalize que liberou um espaço vazio no buffer
        espacos_vazios.release()
        
        # Simula o tempo de consumo
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"✨ Consumidor {id_consumidor} finalizou seu trabalho.")

# ============================
# PROGRAMA PRINCIPAL
# ============================

def main():
    """
    Função principal que inicializa e gerencia todas as threads.
    """
    print("=" * 60)
    print("PROBLEMA DO PRODUTOR-CONSUMIDOR - SINCRONIZAÇÃO")
    print("=" * 60)
    print()
    
    threads = []
    
    # Crie e inicie as threads produtoras
    for i in range(NUM_PRODUTORES):
        t = threading.Thread(target=produtor, args=(i,))
        threads.append(t)
        t.start()
    
    # Crie e inicie as threads consumidoras
    for i in range(NUM_CONSUMIDORES):
        t = threading.Thread(target=consumidor, args=(i,))
        threads.append(t)
        t.start()
    
    # Aguarda todas as threads terminarem para finalizar o programa
    for t in threads:
        t.join()
    
    print()
    print("=" * 60)
    print("Sucesso: Todos os itens foram produzidos e consumidos!")
    print("=" * 60)

# ============================
# PONTO DE ENTRADA
# ============================

if __name__ == "__main__":
    main()