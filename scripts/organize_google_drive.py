#!/usr/bin/env python3
"""
Script de automação para organizar a pasta do Google Drive do Scoreboard App.
Pasta Alvo: https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z
ID: 1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z
"""

import os
import sys
import json
import subprocess
import requests

FOLDER_ID = "1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

# Mapeamento dos nomes originais para as novas pastas e nomes limpos
MAPPING = {
    # 00 - Arquitetura
    "App Calculadoras Médicas - Especificação Técnica e Modelagem de Banco de Dados.pdf": {
        "folder": "00_Plano_e_Arquitetura",
        "new_name": "Proposta_Original_Calculadoras_Medicas.pdf"
    },
    # 01 - Especificações Clínicas
    "__REVISÃO SISTEMÁTICA E EXHAUSTIVA DE ESCORES PROGNÓSTICOS E CALCULADORAS CLÍNICAS NA.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_01_Emergencia_Choque_UTI.pdf"
    },
    "Revisão Sistemática de Escores Cardiológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_02_Cardiologia_Hemodinamica.pdf"
    },
    "--- ### 16. EDSS (_Expanded Disability Status Scale_ - Esclerose Múltipla) #### 1. Identificação.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_03_Neurologia_Neurocirurgia.pdf"
    },
    "Chats com anexos (1).docx": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_03_Anexo_Dossie_Neurologia.docx"
    },
    "Guia Clínico de Escores Pneumológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_04_Pneumologia.pdf"
    },
    "Guia Clínico de Escores Cirúrgicos e Trauma.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_05_Cirurgia_Geral_Trauma.pdf"
    },
    "Revisão Sistemática de Escores Nefrológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_06_Nefrologia_Meio_Interno.pdf"
    },
    "Chats com anexos.docx": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_06_Anexo_Dossie_Nefrologia.docx"
    },
    "Revisão Sistemática de Escores em Hepatologia e Gastroenterologia.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_07_Hepatologia_Gastroenterologia.pdf"
    },
    "Guia Clínico de Escores Pediátricos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_08_Pediatria_Neonatologia.pdf"
    },
    "Revisão de Escores em Hematologia.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_09_Hematologia_Reumatologia.pdf"
    },
    # 02 - Design System
    "frontcraft_master_v2_0_est_dio_reativo_de_design_system.html": {
        "folder": "02_Design_System_UI",
        "new_name": "frontcraft_master_v2_0_estudio_reativo.html"
    },
    "guia_e_laboratorio_front_end_master.html": {
        "folder": "02_Design_System_UI",
        "new_name": "guia_e_laboratorio_front_end_master.html"
    },
    "guia_visual_de_frontend_gerador_de_prompts.tsx": {
        "folder": "02_Design_System_UI",
        "new_name": "guia_visual_de_frontend_gerador_de_prompts.tsx"
    },
    "gemini-code-1790054955496.ts": {
        "folder": "02_Design_System_UI",
        "new_name": "componente_tokens_frontcraft.ts"
    },
    "gemini-code-1790054965786.md": {
        "folder": "02_Design_System_UI",
        "new_name": "especificacao_design_system_tokens.md"
    },
    # 03 - Protocolos BIC
    "gemini-code-1790030040094.md": {
        "folder": "03_Protocolos_Prescricao_BIC",
        "new_name": "protocolo_mestre_prescricao_e_bic.md"
    }
}

DUPLICATES_TO_TRASH = [
    "frontcraft_master_v2_0_est_dio_reativo_de_design_system (1).html",
    "gemini-code-1789963111869.md"
]

SUBFOLDERS = [
    "00_Plano_e_Arquitetura",
    "01_Especificacoes_Clinicas",
    "02_Design_System_UI",
    "03_Protocolos_Prescricao_BIC"
]

def get_access_token():
    # 1. Variável de ambiente direta
    token = os.environ.get("GOOGLE_DRIVE_TOKEN") or os.environ.get("ACCESS_TOKEN")
    if token:
        return token

    # 2. Tentar ADC refresh token se tiver scope de drive
    adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    if os.path.exists(adc_path):
        try:
            with open(adc_path, "r") as f:
                adc = json.load(f)
            if "client_id" in adc and "refresh_token" in adc:
                res = requests.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": adc["client_id"],
                        "client_secret": adc["client_secret"],
                        "refresh_token": adc["refresh_token"],
                        "grant_type": "refresh_token"
                    },
                    timeout=10
                )
                if res.status_code == 200:
                    token = res.json().get("access_token")
                    if token:
                        # Verificar se o token tem escopo de drive
                        t_info = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={token}", timeout=5).json()
                        scopes = t_info.get("scope", "")
                        if "https://www.googleapis.com/auth/drive" in scopes:
                            return token
        except Exception:
            pass

    # 3. Fallback: gcloud auth print-access-token
    try:
        res = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True)
        token = res.stdout.strip()
        t_info = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={token}", timeout=5).json()
        scopes = t_info.get("scope", "")
        if "https://www.googleapis.com/auth/drive" in scopes:
            return token
    except Exception:
        pass

    return None

def main():
    print("=========================================================")
    print("🚀 Organizador Automático do Google Drive — Scoreboard App")
    print("=========================================================")
    print(f"Pasta Alvo: https://drive.google.com/drive/folders/{FOLDER_ID}\n")

    token = get_access_token()
    if not token:
        print("❌ Permissão do Google Drive ausente no ambiente atual.")
        print("\nPara permitir que este script organize seu Google Drive automaticamente,")
        print("execute o seguinte comando no seu terminal:\n")
        print('  gcloud auth application-default login --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive"\n')
        print("Em seguida, execute novamente:")
        print("  python3 scripts/organize_google_drive.py\n")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Testar acesso à pasta
    test_res = requests.get(f"{DRIVE_API_BASE}/files/{FOLDER_ID}?fields=id,name,mimeType", headers=headers)
    if test_res.status_code != 200:
        print(f"❌ Erro ao acessar a pasta raiz ({test_res.status_code}): {test_res.text}")
        sys.exit(1)

    print("✅ Conectado com sucesso ao Google Drive!\n")

    # 2. Listar arquivos existentes na pasta
    print("🔍 Listando arquivos existentes na pasta...")
    query = f"'{FOLDER_ID}' in parents and trashed = false"
    list_res = requests.get(f"{DRIVE_API_BASE}/files?q={query}&fields=files(id,name,mimeType)", headers=headers)
    if list_res.status_code != 200:
        print(f"❌ Erro ao listar arquivos ({list_res.status_code}): {list_res.text}")
        sys.exit(1)

    files = list_res.json().get("files", [])
    print(f"   Encontrados {len(files)} itens na pasta raiz.\n")

    # 3. Criar ou identificar subpastas
    folder_ids = {}
    print("📁 Verificando/Criando subpastas estruturadas...")
    for sub in SUBFOLDERS:
        # Verificar se já existe
        existing = [f for f in files if f["name"] == sub and f["mimeType"] == "application/vnd.google-apps.folder"]
        if existing:
            folder_ids[sub] = existing[0]["id"]
            print(f"   ✓ Subpasta já existe: {sub}")
        else:
            payload = {
                "name": sub,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [FOLDER_ID]
            }
            create_res = requests.post(f"{DRIVE_API_BASE}/files", headers=headers, json=payload)
            if create_res.status_code == 200:
                f_id = create_res.json()["id"]
                folder_ids[sub] = f_id
                print(f"   ➕ Criada subpasta: {sub}")
            else:
                print(f"   ❌ Falha ao criar subpasta {sub}: {create_res.text}")

    print("\n📦 Movendo e renomeando arquivos...")

    # 4. Tratar duplicatas
    for f in files:
        if f["name"] in DUPLICATES_TO_TRASH:
            print(f"   🗑️ Movendo duplicata para lixeira: {f['name']}")
            requests.patch(f"{DRIVE_API_BASE}/files/{f['id']}", headers=headers, json={"trashed": True})

    # 5. Mover e renomear arquivos mapeados
    for f in files:
        fname = f["name"]
        if fname in MAPPING:
            target_info = MAPPING[fname]
            target_sub = target_info["folder"]
            new_name = target_info["new_name"]
            target_folder_id = folder_ids.get(target_sub)

            if target_folder_id:
                print(f"   ➜ Movendo e renomeando:")
                print(f"     De:   '{fname}'")
                print(f"     Para: '{target_sub}/{new_name}'")

                # Atualizar nome e pais
                patch_url = f"{DRIVE_API_BASE}/files/{f['id']}?addParents={target_folder_id}&removeParents={FOLDER_ID}&fields=id,name,parents"
                patch_res = requests.patch(patch_url, headers=headers, json={"name": new_name})
                if patch_res.status_code == 200:
                    print(f"     ✅ Sucesso!")
                else:
                    print(f"     ❌ Erro: {patch_res.text}")

    print("\n🎉 Organização do Google Drive concluída com sucesso!")
    print(f"Confira os arquivos organizados em: https://drive.google.com/drive/folders/{FOLDER_ID}")

if __name__ == "__main__":
    main()
