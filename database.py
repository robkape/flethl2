import sqlite3
import shutil
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_name='crud_flet.db'):
        self.db_name = db_name
        self.db_path = os.path.abspath(db_name)
        self.criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def criar_tabela(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cotacoestab (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_registro TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    projeto TEXT NOT NULL,
                    so TEXT,
                    urgencia INTEGER DEFAULT 0,
                    modal TEXT,       
                    descricao TEXT NOT NULL,
                    prazo_final TEXT,
                    contato TEXT,
                    origem TEXT,
                    destino TEXT,       
                    dimensoes TEXT,                                               
                    peso TEXT,
                    observacao TEXT,
                    followup TEXT
                )
            ''')
            conn.commit()

    def listar_cotacoes(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cotacoestab ORDER BY id DESC")
            return cursor.fetchall()

    def inserir_cotacao(self, data_registro, cliente, projeto, so, urgencia, modal, descricao, prazo_final,
                        contato, origem, destino, dimensoes, peso, observacao, followup):
        
        # CORREÇÃO: Garante que a descrição nunca vá como None (Null) para o banco
        if descricao is None:
            descricao = ""

        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cotacoestab 
                (data_registro, cliente, projeto, so, urgencia, modal, descricao, prazo_final,
                 contato, origem, destino, dimensoes, peso, observacao, followup)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data_registro, cliente, projeto, so, urgencia, modal, descricao, prazo_final,
                  contato, origem, destino, dimensoes, peso, observacao, followup))
            conn.commit()
            return cursor.lastrowid

    def atualizar_cotacao(self, cotacao_id, cliente, projeto, so, urgencia, modal, descricao, prazo_final,
                          contato, origem, destino, dimensoes, peso, observacao, followup):
        
        # CORREÇÃO: Garante que a descrição nunca vá como None (Null) na atualização
        if descricao is None:
            descricao = ""

        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE cotacoestab 
                SET cliente = ?, projeto = ?, so = ?, urgencia = ?, modal = ?, descricao = ?, prazo_final = ?,
                    contato = ?, origem = ?, destino = ?, dimensoes = ?, peso = ?, observacao = ?, followup = ?
                WHERE id = ?
            ''', (cliente, projeto, so, urgencia, modal, descricao, prazo_final,
                  contato, origem, destino, dimensoes, peso, observacao, followup, cotacao_id))
            conn.commit()

    def deletar_cotacao(self, cotacao_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cotacoestab WHERE id = ?', (cotacao_id,))
            conn.commit()

    # ---------- MÉTODO DE BACKUP ----------
    def backup(self) -> tuple[bool, str]:
        if not os.path.exists(self.db_path):
            return False, f"Arquivo do banco de dados não encontrado em: {self.db_path}"

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_cotacoes_{now}.db"

        home = Path.home()
        desktop = None

        possiveis_desktops = [
            home / "Desktop",
            home / "Área de Trabalho",
            home / "OneDrive" / "Desktop",
            home / "OneDrive" / "Área de Trabalho",
        ]

        for p in possiveis_desktops:
            if p.exists():
                desktop = p
                break

        if desktop is None:
            desktop = home

        backup_path = desktop / backup_name

        try:
            shutil.copy2(self.db_path, backup_path)
            return True, f"Backup salvo em: {backup_path}"
        except Exception as e:
            return False, f"Erro ao fazer backup: {str(e)}"
