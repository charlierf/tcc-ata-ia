"""
YouTube Audio Scraper para Reuniões CONSU e CONEPE - UFS
========================================================

Este módulo é responsável por baixar áudios das reuniões dos Conselhos Superiores
da UFS (CONSU e CONEPE) disponíveis no canal da TV UFS no YouTube.

Padrão de títulos esperados:
- "Sala dos Conselhos | DD/MM/AAAA | Sessão CONEPE | #XX"
- "Sala dos Conselhos | DD/MM/AAAA | Sessão CONSU | #XX"

Estrutura de saída:
- data/raw/audio/consu/AAAA-MM-DD_consu_#XX.wav
- data/raw/audio/conepe/AAAA-MM-DD_conepe_#XX.wav

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

import os
import re
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yt_dlp
from urllib.parse import urlparse


class YouTubeScraper:
    """Scraper para baixar áudios das reuniões CONSU e CONEPE do canal TV UFS."""
    
    CHANNEL_URL = "https://www.youtube.com/@TVUFS/streams"
    
    # Regex simples para identificar vídeos da "Sala dos Conselhos"
    TITULO_PATTERN = re.compile(
        r"^Sala dos Conselhos",
        re.IGNORECASE
    )
    
    # Regex detalhado para extrair informações (quando possível)
    TITULO_DETALHADO = re.compile(
        r"Sala dos Conselhos\s*\|\s*(\d{1,2}/\d{1,2}/\d{4})\s*\|\s*Sessão\s+(CONEPE|CONSU)\s*\|\s*#?(\d+)",
        re.IGNORECASE
    )
    
    def __init__(self, base_dir: str = None):
        """
        Inicializa o scraper.
        
        Args:
            base_dir: Diretório base do projeto. Se None, detecta automaticamente.
        """
        if base_dir is None:
            # Detectar o diretório raiz do projeto automaticamente
            # A partir de qualquer lugar, procura pela pasta que contém requirements.txt
            current_path = Path(__file__).resolve()
            
            # Procurar pela raiz do projeto (que contém requirements.txt)
            for parent in [current_path] + list(current_path.parents):
                if (parent / "requirements.txt").exists():
                    base_dir = parent
                    break
            else:
                # Fallback: assumir que está em src/services/ e ir 2 níveis acima
                base_dir = Path(__file__).parent.parent.parent
        
        self.base_dir = Path(base_dir)
        self.audio_dir = self.base_dir / "data" / "raw" / "audio"
        self.consu_dir = self.audio_dir / "consu"
        self.conepe_dir = self.audio_dir / "conepe"
        self.metadata_file = self.audio_dir / "metadata.json"
        
        # Criar diretórios necessários
        self._setup_directories()
        
        # Configurar logging
        self._setup_logging()
        
        # Carregar metadados existentes
        self.metadata = self._load_metadata()
    
    def _setup_directories(self):
        """Cria os diretórios necessários para organizar os áudios."""
        for directory in [self.consu_dir, self.conepe_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Diretórios criados em: {self.audio_dir}")
    
    def _setup_logging(self):
        """Configura o sistema de logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / 'scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_metadata(self) -> Dict:
        """Carrega metadados dos downloads anteriores."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Erro ao carregar metadados: {e}")
                return {"downloads": [], "last_update": None}
        return {"downloads": [], "last_update": None}
    
    def _save_metadata(self):
        """Salva os metadados dos downloads."""
        self.metadata["last_update"] = datetime.now().isoformat()
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Erro ao salvar metadados: {e}")
    
    def _parse_title(self, title: str) -> Optional[Tuple[str, str, str]]:
        """
        Extrai informações do título do vídeo.
        
        Args:
            title: Título do vídeo
            
        Returns:
            Tupla com (data, conselho, numero) ou None se não encontrar padrão
        """
        # Primeiro verificar se é um vídeo da "Sala dos Conselhos"
        if not self.TITULO_PATTERN.search(title):
            return None
        
        # Tentar extrair informações detalhadas
        match = self.TITULO_DETALHADO.search(title)
        if match:
            data_str, conselho, numero = match.groups()
            return data_str, conselho.lower(), numero
        
        # Se não conseguir extrair informações detalhadas, 
        # criar valores padrão baseados no título
        self.logger.warning(f"Título não segue padrão esperado: {title}")
        
        # Tentar identificar pelo menos o conselho
        conselho = "unknown"
        if "CONSU" in title.upper():
            conselho = "consu"
        elif "CONEPE" in title.upper():
            conselho = "conepe"
        
        # Usar timestamp atual como fallback para data
        data_atual = datetime.now().strftime("%d/%m/%Y")
        numero_fallback = "000"
        
        return data_atual, conselho, numero_fallback
    
    def _format_filename(self, data_str: str, conselho: str, numero: str) -> str:
        """
        Formata o nome do arquivo de saída.
        
        Args:
            data_str: Data no formato DD/MM/AAAA
            conselho: Nome do conselho (consu ou conepe)
            numero: Número da sessão
            
        Returns:
            Nome do arquivo formatado
        """
        # Converter data de DD/MM/AAAA para AAAA-MM-DD
        dia, mes, ano = data_str.split('/')
        data_iso = f"{ano}-{mes}-{dia}"
        return f"{data_iso}_{conselho}_#{numero}.wav"
    
    def _get_output_path(self, data_str: str, conselho: str, numero: str) -> Path:
        """
        Determina o caminho completo de saída do arquivo.
        
        Args:
            data_str: Data no formato DD/MM/AAAA
            conselho: Nome do conselho (consu ou conepe)
            numero: Número da sessão
            
        Returns:
            Path completo para o arquivo de saída
        """
        filename = self._format_filename(data_str, conselho, numero)
        if conselho == 'consu':
            return self.consu_dir / filename
        else:
            return self.conepe_dir / filename
    
    def _is_already_downloaded(self, video_id: str) -> bool:
        """
        Verifica se um vídeo já foi baixado anteriormente.
        
        Args:
            video_id: ID do vídeo no YouTube
            
        Returns:
            True se já foi baixado, False caso contrário
        """
        return any(download.get('video_id') == video_id 
                  for download in self.metadata['downloads'])
    
    def get_channel_videos(self, limit: int = 50) -> List[Dict]:
        """
        Obtém lista de vídeos do canal da TV UFS.
        
        Args:
            limit: Número máximo de vídeos para processar
            
        Returns:
            Lista de dicionários com informações dos vídeos
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': limit,
        }
        
        videos = []
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info(f"Buscando vídeos do canal: {self.CHANNEL_URL}")
                
                # Extrair informações do canal/playlist
                info = ydl.extract_info(self.CHANNEL_URL, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry and 'title' in entry:
                            # Verificar se é uma reunião do CONSU ou CONEPE
                            parsed = self._parse_title(entry['title'])
                            if parsed:
                                videos.append({
                                    'video_id': entry['id'],
                                    'title': entry['title'],
                                    'url': entry['url'],
                                    'data': parsed[0],
                                    'conselho': parsed[1],
                                    'numero': parsed[2],
                                    'parsed_info': parsed
                                })
                                self.logger.info(f"Encontrado: {entry['title']}")
                            else:
                                self.logger.debug(f"Título ignorado: {entry['title']}")
                
        except Exception as e:
            self.logger.error(f"Erro ao buscar vídeos do canal: {e}")
            
        self.logger.info(f"Total de reuniões encontradas: {len(videos)}")
        return videos
    
    def download_audio(self, video_info: Dict) -> bool:
        """
        Baixa o áudio de um vídeo específico.
        
        Args:
            video_info: Dicionário com informações do vídeo
            
        Returns:
            True se o download foi bem-sucedido, False caso contrário
        """
        video_id = video_info['video_id']
        
        # Verificar se já foi baixado
        if self._is_already_downloaded(video_id):
            self.logger.info(f"Vídeo {video_id} já foi baixado anteriormente")
            return True
        
        # Determinar caminho de saída
        output_path = self._get_output_path(
            video_info['data'],
            video_info['conselho'],
            video_info['numero']
        )
        
        # Verificar se arquivo já existe
        if output_path.exists():
            self.logger.info(f"Arquivo já existe: {output_path}")
            # Adicionar aos metadados se não estiver lá
            self.metadata['downloads'].append({
                'video_id': video_id,
                'title': video_info['title'],
                'output_path': str(output_path),
                'download_date': datetime.now().isoformat(),
                'conselho': video_info['conselho'],
                'data_reuniao': video_info['data'],
                'numero_sessao': video_info['numero']
            })
            return True
        
        # Configurações do yt-dlp para download de áudio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_path.with_suffix('')),  # Sem extensão, yt-dlp adiciona
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-ar', '16000',  # Sample rate 16kHz (bom para speech recognition)
                '-ac', '1',      # Mono
            ],
            'ignoreerrors': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info(f"Baixando: {video_info['title']}")
                self.logger.info(f"Salvando em: {output_path}")
                
                ydl.download([video_info['url']])
                
                # Verificar se o arquivo foi criado
                if output_path.exists():
                    file_size = output_path.stat().st_size
                    self.logger.info(f"Download concluído: {output_path} ({file_size/1024/1024:.1f} MB)")
                    
                    # Adicionar aos metadados
                    self.metadata['downloads'].append({
                        'video_id': video_id,
                        'title': video_info['title'],
                        'output_path': str(output_path),
                        'download_date': datetime.now().isoformat(),
                        'conselho': video_info['conselho'],
                        'data_reuniao': video_info['data'],
                        'numero_sessao': video_info['numero'],
                        'file_size_mb': round(file_size/1024/1024, 1)
                    })
                    
                    return True
                else:
                    self.logger.error(f"Arquivo não foi criado: {output_path}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Erro ao baixar {video_info['title']}: {e}")
            return False
    
    def run_scraper(self, limit: int = 50, download_limit: int = None) -> Dict:
        """
        Executa o processo completo de scraping.
        
        Args:
            limit: Número máximo de vídeos para buscar
            download_limit: Número máximo de downloads (None = sem limite)
            
        Returns:
            Dicionário com estatísticas do processo
        """
        self.logger.info("Iniciando processo de scraping...")
        
        # Buscar vídeos
        videos = self.get_channel_videos(limit)
        
        if not videos:
            self.logger.warning("Nenhum vídeo de reunião encontrado")
            return {"videos_found": 0, "downloads_attempted": 0, "downloads_successful": 0}
        
        # Filtrar vídeos já baixados
        videos_to_download = [
            v for v in videos 
            if not self._is_already_downloaded(v['video_id'])
        ]
        
        self.logger.info(f"Vídeos para download: {len(videos_to_download)}")
        
        # Aplicar limite de downloads se especificado
        if download_limit:
            videos_to_download = videos_to_download[:download_limit]
            self.logger.info(f"Limitando downloads a: {download_limit}")
        
        # Baixar áudios
        successful_downloads = 0
        for i, video in enumerate(videos_to_download, 1):
            self.logger.info(f"Download {i}/{len(videos_to_download)}")
            if self.download_audio(video):
                successful_downloads += 1
            
            # Salvar metadados a cada download
            self._save_metadata()
        
        # Salvar metadados finais
        self._save_metadata()
        
        stats = {
            "videos_found": len(videos),
            "downloads_attempted": len(videos_to_download),
            "downloads_successful": successful_downloads,
            "total_downloaded": len(self.metadata['downloads'])
        }
        
        self.logger.info(f"Scraping concluído: {stats}")
        return stats
    
    def get_download_statistics(self) -> Dict:
        """
        Retorna estatísticas dos downloads realizados.
        
        Returns:
            Dicionário com estatísticas detalhadas
        """
        downloads = self.metadata.get('downloads', [])
        
        if not downloads:
            return {"total": 0, "consu": 0, "conepe": 0}
        
        consu_count = sum(1 for d in downloads if d.get('conselho') == 'consu')
        conepe_count = sum(1 for d in downloads if d.get('conselho') == 'conepe')
        
        total_size = sum(d.get('file_size_mb', 0) for d in downloads)
        
        return {
            "total": len(downloads),
            "consu": consu_count,
            "conepe": conepe_count,
            "total_size_mb": round(total_size, 1),
            "last_update": self.metadata.get('last_update')
        }
    
    def get_all_sala_conselhos_videos(self, limit: int = 100) -> List[Dict]:
        """
        Lista TODOS os vídeos que começam com "Sala dos Conselhos" para análise.

        Args:
            limit: Número máximo de vídeos para processar
            
        Returns:
            Lista com todos os vídeos encontrados, mesmo os com padrão diferente
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': limit,
        }

        todos_videos = []
        videos_padrao = []
        videos_diferentes = []

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info(f"Analisando vídeos do canal: {self.CHANNEL_URL}")
                
                info = ydl.extract_info(self.CHANNEL_URL, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry and 'title' in entry:
                            title = entry['title']
                            
                            # Verificar se é da "Sala dos Conselhos"
                            if self.TITULO_PATTERN.search(title):
                                video_info = {
                                    'video_id': entry['id'],
                                    'title': title,
                                    'url': entry['url']
                                }
                                
                                # Tentar fazer parse
                                parsed = self._parse_title(title)
                                if parsed and parsed[2] != "000":  # Se conseguiu extrair info real
                                    video_info.update({
                                        'data': parsed[0],
                                        'conselho': parsed[1],
                                        'numero': parsed[2],
                                        'status': 'padrao_ok'
                                    })
                                    videos_padrao.append(video_info)
                                else:
                                    video_info.update({
                                        'status': 'padrao_diferente'
                                    })
                                    videos_diferentes.append(video_info)
                                
                                todos_videos.append(video_info)
                                self.logger.info(f"[{video_info['status']}] {title}")

        except Exception as e:
            self.logger.error(f"Erro ao analisar vídeos: {e}")

        self.logger.info(f"=== ANÁLISE COMPLETA ===")
        self.logger.info(f"Total 'Sala dos Conselhos': {len(todos_videos)}")
        self.logger.info(f"Padrão correto: {len(videos_padrao)}")
        self.logger.info(f"Padrão diferente: {len(videos_diferentes)}")

        return todos_videos


def main():
    """Função principal para executar o scraper via linha de comando."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Scraper para reuniões CONSU e CONEPE")
    parser.add_argument('--limit', type=int, default=50, 
                       help='Número máximo de vídeos para buscar (padrão: 50)')
    parser.add_argument('--download-limit', type=int, 
                       help='Número máximo de downloads por execução')
    parser.add_argument('--stats-only', action='store_true',
                       help='Mostrar apenas estatísticas sem fazer downloads')
    parser.add_argument('--base-dir', type=str,
                       help='Diretório base do projeto')
    
    args = parser.parse_args()
    
    # Inicializar scraper
    scraper = YouTubeScraper(base_dir=args.base_dir)
    
    if args.stats_only:
        # Mostrar apenas estatísticas
        stats = scraper.get_download_statistics()
        print("\n=== ESTATÍSTICAS DOS DOWNLOADS ===")
        print(f"Total de reuniões baixadas: {stats['total']}")
        print(f"Reuniões CONSU: {stats['consu']}")
        print(f"Reuniões CONEPE: {stats['conepe']}")
        print(f"Tamanho total: {stats['total_size_mb']} MB")
        if stats['last_update']:
            print(f"Última atualização: {stats['last_update']}")
    else:
        # Executar scraping
        results = scraper.run_scraper(
            limit=args.limit,
            download_limit=args.download_limit
        )
        
        print("\n=== RESULTADOS DO SCRAPING ===")
        print(f"Vídeos encontrados: {results['videos_found']}")
        print(f"Downloads tentados: {results['downloads_attempted']}")
        print(f"Downloads bem-sucedidos: {results['downloads_successful']}")
        print(f"Total acumulado: {results['total_downloaded']}")


if __name__ == "__main__":
    main()
