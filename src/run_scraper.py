#!/usr/bin/env python3
"""
Script de execução do YouTube Scraper para reuniões CONSU e CONEPE
================================================================

Script simples para executar o scraper das reuniões dos conselhos da UFS.

Uso:
    python run_scraper.py                    # Download completo
    python run_scraper.py --limit 10         # Buscar apenas 10 vídeos mais recentes
    python run_scraper.py --stats            # Mostrar apenas estatísticas
    python run_scraper.py --download-limit 5 # Baixar no máximo 5 vídeos

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

import sys
import argparse
from pathlib import Path

# Adicionar o diretório src ao path para imports
sys.path.append(str(Path(__file__).parent))

from services.youtube_scraper import YouTubeScraper


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Baixar áudios das reuniões CONSU e CONEPE do canal TV UFS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_scraper.py                    # Download completo
  python run_scraper.py --limit 20         # Buscar apenas 20 vídeos mais recentes  
  python run_scraper.py --stats            # Mostrar apenas estatísticas
  python run_scraper.py --download-limit 3 # Baixar no máximo 3 vídeos por execução
  python run_scraper.py --test             # Modo teste (buscar mas não baixar)
        """
    )
    
    parser.add_argument(
        '--limit', 
        type=int, 
        default=100, 
        help='Número máximo de vídeos para buscar no canal (padrão: 100)'
    )
    
    parser.add_argument(
        '--download-limit', 
        type=int, 
        help='Número máximo de downloads por execução (útil para testes)'
    )
    
    parser.add_argument(
        '--stats', 
        action='store_true',
        help='Mostrar apenas estatísticas dos downloads existentes'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Modo teste: buscar vídeos mas não fazer downloads'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Mostrar logs detalhados'
    )
    
    parser.add_argument(
        '--analyze', 
        action='store_true',
        help='Analisar todos os vídeos da Sala dos Conselhos (sem baixar)'
    )
    
    args = parser.parse_args()
    
    # O diretório base será detectado automaticamente pelo YouTubeScraper
    # Não precisamos mais especificar manualmente
    
    try:
        # Inicializar scraper (detecta automaticamente o diretório raiz)
        print("🎥 YouTube Scraper - Reuniões CONSU e CONEPE")
        print("=" * 50)
        
        scraper = YouTubeScraper()  # Detecta automaticamente o diretório raiz
        
        if args.analyze:
            # Análise completa dos vídeos
            videos = scraper.get_all_sala_conselhos_videos(100)
            
            padrao_ok = [v for v in videos if v.get('status') == 'padrao_ok']
            padrao_diferente = [v for v in videos if v.get('status') == 'padrao_diferente']
            
            print(f"\n📊 ANÁLISE COMPLETA - 'Sala dos Conselhos'")
            print(f"{'='*50}")
            print(f"✅ Padrão correto: {len(padrao_ok)}")
            print(f"❓ Padrão diferente: {len(padrao_diferente)}")
            
            if padrao_diferente:
                print(f"\n❓ TÍTULOS COM PADRÃO DIFERENTE:")
                for video in padrao_diferente:
                    print(f"  - {video['title']}")
            
        if args.stats:
            # Mostrar estatísticas
            stats = scraper.get_download_statistics()
            print("\n📊 ESTATÍSTICAS DOS DOWNLOADS")
            print("-" * 30)
            print(f"Total de reuniões: {stats['total']}")
            print(f"Reuniões CONSU: {stats['consu']}")
            print(f"Reuniões CONEPE: {stats['conepe']}")
            print(f"Tamanho total: {stats['total_size_mb']} MB")
            if stats['last_update']:
                print(f"Última atualização: {stats['last_update']}")
            else:
                print("Nenhum download realizado ainda")
                
        elif args.test:
            # Modo teste - apenas buscar vídeos
            print(f"\n🔍 MODO TESTE - Buscando vídeos (limite: {args.limit})")
            print("-" * 50)
            
            videos = scraper.get_channel_videos(args.limit)
            
            if videos:
                print(f"\n✅ Encontradas {len(videos)} reuniões:")
                for i, video in enumerate(videos, 1):
                    print(f"{i:2d}. [{video['conselho'].upper()}] {video['data']} - #{video['numero']}")
                    print(f"     {video['title']}")
                    print(f"     ID: {video['video_id']}")
                    print()
            else:
                print("❌ Nenhuma reunião encontrada")
                
        else:
            # Executar scraping completo
            print(f"\n⬇️  INICIANDO DOWNLOADS")
            print(f"Limite de busca: {args.limit}")
            if args.download_limit:
                print(f"Limite de downloads: {args.download_limit}")
            print("-" * 50)
            
            results = scraper.run_scraper(
                limit=args.limit,
                download_limit=args.download_limit
            )
            
            print("\n📊 RESULTADOS")
            print("-" * 20)
            print(f"Vídeos encontrados: {results['videos_found']}")
            print(f"Downloads tentados: {results['downloads_attempted']}")
            print(f"Downloads bem-sucedidos: {results['downloads_successful']}")
            print(f"Total acumulado: {results['total_downloaded']}")
            
            if results['downloads_successful'] > 0:
                print(f"\n✅ {results['downloads_successful']} áudios baixados com sucesso!")
                print(f"📁 Arquivos salvos em: {scraper.audio_dir}")
            elif results['downloads_attempted'] == 0:
                print("\n💡 Todos os vídeos já foram baixados anteriormente")
            else:
                print("\n❌ Houveram falhas nos downloads. Verifique os logs.")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Operação cancelada pelo usuário")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
