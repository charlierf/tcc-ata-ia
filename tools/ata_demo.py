#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Geração Automática de Atas - UFS
Demonstração Interativa para Conselho Universitário

Este script implementa uma interface visual usando Gradio para demonstrar
o sistema de geração automática de atas de reunião desenvolvido para
a Universidade Federal de Sergipe (UFS).

Autor: [Seu Nome]
Data: Agosto 2025
"""

import gradio as gr
import whisper
import os
from openai import OpenAI
from pyannote.audio import Pipeline
import torch
from datetime import datetime
import json
import tempfile
from collections import defaultdict
import warnings
import argparse
import sys

warnings.filterwarnings('ignore')

class AtaSystemUFS:
    """Sistema de geração de atas da UFS"""
    
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.whisper_model = None
        self.diarization_pipeline = None
        self.client = None
        self.diarization_available = False
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def setup_models(self):
        """Configura todos os modelos necessários"""
        print("🔄 Iniciando configuração dos modelos...")
        
        # OpenAI Client
        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
            print("✅ Cliente OpenAI configurado!")
        else:
            print("❌ ERRO: Chave da OpenAI API não configurada")
            print("   Configure a variável de ambiente OPENAI_API_KEY")
            return False
        
        # Whisper
        try:
            print("🔄 Carregando modelo Whisper...")
            self.whisper_model = whisper.load_model("small")
            print("✅ Whisper carregado!")
        except Exception as e:
            print(f"❌ Erro ao carregar Whisper: {e}")
            return False
        
        # Diarização (opcional)
        try:
            print("🔄 Configurando pipeline de diarização...")
            print(f"   Dispositivo: {self.device}")
            self.diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1")
            self.diarization_pipeline.to(self.device)
            self.diarization_available = True
            print("✅ Pipeline de diarização configurado!")
        except Exception as e:
            print(f"⚠️ Diarização não disponível: {e}")
            print("   Sistema funcionará sem separação de speakers")
            self.diarization_available = False
        
        print("✅ Configuração concluída!")
        return True
    
    def perform_diarization(self, audio_path):
        """Realiza diarização do áudio"""
        if not self.diarization_available:
            return []
        
        try:
            diarization = self.diarization_pipeline(audio_path)
            speakers_info = []
            
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                speakers_info.append({
                    "speaker": speaker,
                    "start": turn.start,
                    "end": turn.end,
                    "duration": turn.end - turn.start
                })
            
            return speakers_info
        except Exception as e:
            print(f"Erro na diarização: {e}")
            return []
    
    def transcribe_with_diarization(self, audio_path, speakers_info):
        """Transcreve áudio com informações de diarização"""
        try:
            result = self.whisper_model.transcribe(audio_path, language="pt")
            full_transcription = result["text"]
            segments = result.get("segments", [])
            
            if not speakers_info or not segments:
                return [], full_transcription
            
            speaker_transcriptions = []
            
            for segment in segments:
                segment_center = (segment["start"] + segment["end"]) / 2
                assigned_speaker = "PARTICIPANTE"
                
                for speaker_info in speakers_info:
                    if speaker_info["start"] <= segment_center <= speaker_info["end"]:
                        assigned_speaker = speaker_info["speaker"]
                        break
                
                speaker_transcriptions.append({
                    "speaker": assigned_speaker,
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "duration": segment["end"] - segment["start"]
                })
            
            return speaker_transcriptions, full_transcription
        
        except Exception as e:
            print(f"Erro na transcrição: {e}")
            return [], ""
    
    def generate_speaker_stats(self, speaker_transcriptions):
        """Gera estatísticas dos participantes"""
        speaker_stats = defaultdict(lambda: {"total_time": 0, "segments": 0, "words": 0})
        
        for segment in speaker_transcriptions:
            speaker = segment["speaker"]
            speaker_stats[speaker]["total_time"] += segment["duration"]
            speaker_stats[speaker]["segments"] += 1
            speaker_stats[speaker]["words"] += len(segment["text"].split())
        
        return dict(speaker_stats)
    
    def generate_meeting_minutes(self, transcription, speaker_stats=None):
        """Gera ata de reunião usando OpenAI"""
        try:
            speaker_context = ""
            if speaker_stats:
                speaker_context = "\n\n=== PARTICIPANTES IDENTIFICADOS ===\n"
                for speaker, stats in speaker_stats.items():
                    speaker_context += f"- {speaker}: {stats['total_time']:.1f}s de fala, {stats['segments']} intervenções\n"
            
            system_prompt = """Você é um assistente especializado em gerar atas de reunião para o contexto universitário brasileiro.
            
            Sua tarefa é analisar a transcrição de uma reunião e criar uma ata formal e estruturada seguindo os padrões acadêmicos.
            
            A ata deve conter:
            1. CABEÇALHO - Data, participantes, tipo de reunião
            2. PAUTA - Principais tópicos discutidos
            3. DELIBERAÇÕES - Decisões tomadas e votações
            4. ENCAMINHAMENTOS - Ações futuras e responsáveis
            5. OBSERVAÇÕES - Informações adicionais relevantes
            
            Use linguagem formal, objetiva e organize as informações de forma clara e hierárquica.
            Identifique decisões importantes, pontos de consenso e discordância quando aplicável."""
            
            user_prompt = f"""TRANSCRIÇÃO DA REUNIÃO:
            {transcription}
            {speaker_context}
            
            Por favor, gere uma ata completa, formal e bem estruturada baseada nesta transcrição.
            Organize as informações de forma profissional adequada para o ambiente universitário."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Erro na geração da ata: {str(e)}"
    
    def process_audio_file(self, audio_file, progress=gr.Progress()):
        """Função principal que processa o arquivo de áudio"""
        if audio_file is None:
            return "❌ Nenhum arquivo de áudio foi enviado.", "", "", ""
        
        try:
            progress(0, desc="🎵 Carregando arquivo de áudio...")
            
            # Etapa 1: Diarização
            progress(0.1, desc="🎭 Identificando participantes (diarização)...")
            speakers_info = self.perform_diarization(audio_file)
            
            num_speakers = len(set([s['speaker'] for s in speakers_info])) if speakers_info else 1
            
            # Etapa 2: Transcrição
            progress(0.4, desc="🎤 Transcrevendo áudio...")
            speaker_transcriptions, full_transcription = self.transcribe_with_diarization(audio_file, speakers_info)
            
            if not full_transcription:
                return "❌ Erro na transcrição do áudio.", "", "", ""
            
            # Etapa 3: Estatísticas
            progress(0.6, desc="📊 Calculando estatísticas...")
            speaker_stats = self.generate_speaker_stats(speaker_transcriptions)
            
            # Etapa 4: Geração da ata
            progress(0.8, desc="📝 Gerando ata de reunião...")
            meeting_minutes = self.generate_meeting_minutes(full_transcription, speaker_stats)
            
            progress(1.0, desc="✅ Processamento concluído!")
            
            # Formatação dos resultados
            stats_text = f"""## 📊 Estatísticas da Reunião

**Participantes identificados:** {num_speakers}
**Duração da transcrição:** {len(full_transcription)} caracteres
**Processado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

### Participação por Speaker:
"""
            
            if speaker_stats:
                for speaker, stats in sorted(speaker_stats.items()):
                    stats_text += f"\n- **{speaker}**: {stats['total_time']:.1f}s ({stats['segments']} intervenções, {stats['words']} palavras)"
            else:
                stats_text += "\n- Não foi possível separar por participantes"
            
            # Transcrição formatada
            transcription_display = f"""## 🎤 Transcrição Completa

{full_transcription[:2000]}{'...' if len(full_transcription) > 2000 else ''}
"""
            
            # Ata formatada
            ata_display = f"""## 📋 Ata de Reunião Gerada

{meeting_minutes}
"""
            
            success_msg = f"""✅ **Processamento concluído com sucesso!**

🎯 **Arquivo processado:** {os.path.basename(audio_file)}
🕒 **Horário:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
👥 **Participantes:** {num_speakers} identificados
📄 **Transcrição:** {len(full_transcription)} caracteres
"""
            
            return success_msg, stats_text, transcription_display, ata_display
        
        except Exception as e:
            error_msg = f"❌ **Erro no processamento:** {str(e)}"
            return error_msg, "", "", ""
    
    def create_interface(self):
        """Cria a interface Gradio"""
        
        css = """
        .gradio-container {
            max-width: 1200px !important;
        }
        .header {
            text-align: center;
            background: linear-gradient(90deg, #1f4e79, #2e7d32);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        """
        
        with gr.Blocks(css=css, title="Sistema de Atas UFS") as interface:
            
            # Cabeçalho
            gr.HTML("""
            <div class="header">
                <h1>🎯 Sistema de Geração Automática de Atas</h1>
                <h2>Universidade Federal de Sergipe - UFS</h2>
                <p><strong>Demonstração para Conselho Universitário</strong></p>
            </div>
            """)
            
            gr.Markdown("""
            ### 📋 Como usar:
            1. **Faça upload** de um arquivo de áudio (.mp3, .wav, .m4a)
            2. **Clique em "Processar Áudio"** e aguarde
            3. **Visualize os resultados** nas abas abaixo
            
            > ⚡ O processamento pode levar alguns minutos dependendo do tamanho do arquivo
            """)
            
            # Input de áudio
            with gr.Row():
                audio_input = gr.Audio(
                    label="📁 Upload do Arquivo de Áudio",
                    type="filepath",
                    format="wav"
                )
            
            # Botão de processamento
            process_btn = gr.Button(
                "🚀 Processar Áudio",
                variant="primary",
                size="lg"
            )
            
            # Outputs organizados em abas
            with gr.Tabs():
                
                with gr.TabItem("📊 Status & Estatísticas"):
                    status_output = gr.Markdown(label="Status")
                    stats_output = gr.Markdown(label="Estatísticas")
                
                with gr.TabItem("🎤 Transcrição"):
                    transcription_output = gr.Markdown(label="Transcrição Completa")
                
                with gr.TabItem("📋 Ata Gerada"):
                    ata_output = gr.Markdown(label="Ata de Reunião")
            
            # Conectar o botão com a função
            process_btn.click(
                fn=self.process_audio_file,
                inputs=[audio_input],
                outputs=[status_output, stats_output, transcription_output, ata_output],
                show_progress=True
            )
            
            # Rodapé
            gr.HTML("""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
                <p><strong>🎓 Sistema desenvolvido para a UFS</strong></p>
                <p>Tecnologias: Whisper AI + PyAnnote + OpenAI GPT + Gradio</p>
                <p><em>Demonstração técnica - TCC Engenharia de Computação</em></p>
            </div>
            """)
        
        return interface
    
    def run(self, share=True, server_port=7860):
        """Executa a aplicação"""
        if not self.setup_models():
            print("❌ Falha na configuração. Encerrando.")
            return
        
        print("🎯 Iniciando Sistema de Geração de Atas - UFS")
        print("📱 A interface será aberta em uma nova aba/janela")
        print("🔗 Ou acesse o link que será exibido abaixo")
        print("\n" + "="*50)
        
        interface = self.create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=server_port,
            share=share,
            debug=False,
            show_error=True
        )


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Sistema de Geração Automática de Atas - UFS")
    parser.add_argument("--api-key", help="Chave da API OpenAI")
    parser.add_argument("--port", type=int, default=7860, help="Porta do servidor (padrão: 7860)")
    parser.add_argument("--no-share", action="store_true", help="Não criar link público")
    
    args = parser.parse_args()
    
    # Verificar chave da API
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERRO: Chave da OpenAI API não fornecida")
        print("\nOPÇÕES:")
        print("1. Use: python ata_demo.py --api-key SUA_CHAVE_AQUI")
        print("2. Ou defina: export OPENAI_API_KEY=SUA_CHAVE_AQUI")
        print("3. Ou configure a variável de ambiente OPENAI_API_KEY")
        sys.exit(1)
    
    # Criar e executar o sistema
    sistema = AtaSystemUFS(openai_api_key=api_key)
    sistema.run(share=not args.no_share, server_port=args.port)


if __name__ == "__main__":
    main()
