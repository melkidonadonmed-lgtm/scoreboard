#!/usr/bin/env python3
"""
Script de automação para organizar a pasta do Google Drive do Scoreboard App.
Pasta Alvo: https://drive.google.com/drive/folders/1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z
ID: 1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z
"""

import json
import os
import subprocess
import sys
from typing import Optional
import requests

FOLDER_ID = "1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

MAPPING: dict[str, dict[str, str]] = {
    "App Calculadoras Médicas - Especificação Técnica e Modelagem de Banco de Dados.pdf": {
        "folder": "00_Plano_e_Arquitetura",
        "new_name": "Proposta_Original_Calculadoras_Medicas.pdf",
    },
    "__REVISÃO SISTEMÁTICA E EXHAUSTIVA DE ESCORES PROGNÓSTICOS E CALCULADORAS CLÍNICAS NA.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_01_Emergencia_Choque_UTI.pdf",
    },
    "Revisão Sistemática de Escores Cardiológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_02_Cardiologia_Hemodinamica.pdf",
    },
    "--- ### 16. EDSS (_Expanded Disability Status Scale_ - Esclerose Múltipla) #### 1. Identificação.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_03_Neurologia_Neurocirurgia.pdf",
    },
    "Chats com anexos (1).docx": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_03_Anexo_Dossie_Neurologia.docx",
    },
    "Guia Clínico de Escores Pneumológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_04_Pneumologia.pdf",
    },
    "Guia Clínico de Escores Cirúrgicos e Trauma.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_05_Cirurgia_Geral_Trauma.pdf",
    },
    "Revisão Sistemática de Escores Nefrológicos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_06_Nefrologia_Meio_Interno.pdf",
    },
    "Chats com anexos.docx": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_06_Anexo_Dossie_Nefrologia.docx",
    },
    "Revisão Sistemática de Escores em Hepatologia e Gastroenterologia.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_07_Hepatologia_Gastroenterologia.pdf",
    },
    "Guia Clínico de Escores Pediátricos.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_08_Pediatria_Neonatologia.pdf",
    },
    "Revisão de Escores em Hematologia.pdf": {
        "folder": "01_Especificacoes_Clinicas",
        "new_name": "Bloco_09_Hematologia_Reumatologia.pdf",
    },
    "frontcraft_master_v2_0_est_dio_reativo_de_design_system.html": {
        "folder": "02_Design_System_UI",
        "new_name": "frontcraft_master_v2_0_estudio_reativo.html",
    },
    "guia_e_laboratorio_front_end_master.html": {
        "folder": "02_Design_System_UI",
        "new_name": "guia_e_laboratorio_front_end_master.html",
    },
    "guia_visual_de_frontend_gerador_de_prompts.tsx": {
        "folder": "02_Design_System_UI",
        "new_name": "guia_visual_de_frontend_gerador_de_prompts.tsx",
    },
    "gemini-code-1790054955496.ts": {
        "folder": "02_Design_System_UI",
        "new_name": "componente_tokens_frontcraft.ts",
    },
    "gemini-code-1790054965786.md": {
        "folder": "02_Design_System_UI",
        "new_name": "especificacao_design_system_tokens.md",
    },
    "gemini-code-1790030040094.md": {
        "folder": "03_Protocolos_Prescricao_BIC",
        "new_name": "protocolo_mestre_prescricao_e_bic.md",
    },
}

DUPLICATES_TO_TRASH: list[str] = [
    "frontcraft_master_v2_0_est_dio_reativo_de_design_system (1).html",
    "gemini-code-1789963111869.md",
]

SUBFOLDERS: list[str] = [
    "00_Plano_e_Arquitetura",
    "01_Especificacoes_Clinicas",
    "02_Design_System_UI",
    "03_Protocolos_Prescricao_BIC",
]


def _has_drive_scope(token: str) -> bool:
    info_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
    t_info = requests.get(info_url, timeout=5).json()
    return "https://www.googleapis.com/auth/drive" in t_info.get("scope", "")


def _token_from_adc(adc_path: str) -> Optional[str]:
    if not os.path.exists(adc_path):
        return None
    try:
        with open(adc_path, "r", encoding="utf-8") as f:
            adc = json.load(f)
        if "client_id" not in adc or "refresh_token" not in adc:
            return None
        res = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": adc["client_id"],
                "client_secret": adc["client_secret"],
                "refresh_token": adc["refresh_token"],
                "grant_type": "refresh_token",
            },
            timeout=10,
        )
        token = res.json().get("access_token") if res.status_code == 200 else None
        return token if token and _has_drive_scope(token) else None
    except (OSError, ValueError, requests.RequestException) as exc:
        sys.stderr.write(f"[ADC Token Fallback] {exc}\n")
        return None


def get_access_token() -> Optional[str]:
    token = os.environ.get("GOOGLE_DRIVE_TOKEN") or os.environ.get("ACCESS_TOKEN")
    if token:
        return token

    adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    adc_token = _token_from_adc(adc_path)
    if adc_token:
        return adc_token

    try:
        res = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            text=True,
            check=True,
        )
        cli_token = res.stdout.strip()
        if cli_token and _has_drive_scope(cli_token):
            return cli_token
    except (OSError, subprocess.SubprocessError, requests.RequestException) as exc:
        sys.stderr.write(f"[gcloud Token Fallback] {exc}\n")
    return None


def _ensure_subfolders(files: list[dict], headers: dict[str, str]) -> dict[str, str]:
    folder_ids: dict[str, str] = {}
    for sub in SUBFOLDERS:
        existing = [
            f for f in files
            if f["name"] == sub and f["mimeType"] == "application/vnd.google-apps.folder"
        ]
        if existing:
            folder_ids[sub] = existing[0]["id"]
            continue
        payload = {
            "name": sub,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [FOLDER_ID],
        }
        create_res = requests.post(f"{DRIVE_API_BASE}/files", headers=headers, json=payload, timeout=15)
        if create_res.status_code == 200:
            folder_ids[sub] = create_res.json()["id"]
    return folder_ids


def _move_and_clean_files(files: list[dict], folder_ids: dict[str, str], headers: dict[str, str]) -> None:
    for f in files:
        fname = f["name"]
        if fname in DUPLICATES_TO_TRASH:
            requests.patch(
                f"{DRIVE_API_BASE}/files/{f['id']}",
                headers=headers,
                json={"trashed": True},
                timeout=15,
            )
            continue
        target_info = MAPPING.get(fname)
        if not target_info:
            continue
        target_folder_id = folder_ids.get(target_info["folder"])
        if not target_folder_id:
            continue
        patch_url = (
            f"{DRIVE_API_BASE}/files/{f['id']}"
            f"?addParents={target_folder_id}&removeParents={FOLDER_ID}&fields=id,name,parents"
        )
        requests.patch(patch_url, headers=headers, json={"name": target_info["new_name"]}, timeout=15)


def main() -> None:
    print("Organizador Automatico do Google Drive - Scoreboard App")
    token = get_access_token()
    if not token:
        print("Permissao do Google Drive ausente no ambiente atual.")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    test_res = requests.get(f"{DRIVE_API_BASE}/files/{FOLDER_ID}?fields=id,name,mimeType", headers=headers, timeout=15)
    if test_res.status_code != 200:
        sys.exit(1)

    query = f"'{FOLDER_ID}' in parents and trashed = false"
    list_res = requests.get(f"{DRIVE_API_BASE}/files?q={query}&fields=files(id,name,mimeType)", headers=headers, timeout=15)
    if list_res.status_code != 200:
        sys.exit(1)

    files = list_res.json().get("files", [])
    folder_ids = _ensure_subfolders(files, headers)
    _move_and_clean_files(files, folder_ids, headers)
    print(f"Organizacao concluida: https://drive.google.com/drive/folders/{FOLDER_ID}")


if __name__ == "__main__":
    main()
