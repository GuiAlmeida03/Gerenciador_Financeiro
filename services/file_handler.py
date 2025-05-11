import json
import os
from typing import Dict, Any, Optional


class FileHandler:
    def __init__(self, file_path: str):
        """
        Inicializa o manipulador de arquivo.
        
        Args:
            file_path: Caminho para o arquivo JSON
        """
        self.file_path = file_path
        
        # Cria o diretório se não existir
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Cria o arquivo se não existir
        if not os.path.exists(file_path):
            self.save_data({})
    
    def load_data(self) -> Dict[str, Any]:
        """
        Carrega os dados do arquivo JSON.
        
        Returns:
            Dicionário com os dados carregados
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Retorna um dicionário vazio se o arquivo estiver vazio ou não existir
            return {}
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """
        Salva os dados no arquivo JSON.
        
        Args:
            data: Dicionário com os dados a serem salvos
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)