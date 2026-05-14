# Sistema de Atas Escolares Disciplinares

Sistema web em Python/FastAPI para geração automática de atas escolares disciplinares, com regras baseadas no Regimento Interno Escolar da Escola Estadual São José.

## Rodar localmente no Windows

No PowerShell, a partir da pasta `D:\Projetos\Atas`:

```powershell
cd ata_system
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Rodar em servidor Linux

Exemplo em `/opt/ata_system`:

```bash
cd /opt/ata_system
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
nano .env
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Para gerar textos com IA local, instale e mantenha o Ollama em execução. O sistema usa o Ollama apenas para reescrever o texto base gerado pelo próprio sistema; artigo, inciso, gravidade e sanção continuam definidos pelo motor de regras fixo.

Exemplo com Ollama no mesmo servidor:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT_SECONDS=60
SESSION_SECRET_KEY=troque-por-uma-chave-grande-e-aleatoria
```

Exemplo com uma IA em outro servidor da rede:

```env
OLLAMA_BASE_URL=http://192.168.1.50:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT_SECONDS=60
SESSION_SECRET_KEY=troque-por-uma-chave-grande-e-aleatoria
```

Para conferir se o Ollama está respondendo:

```bash
systemctl status ollama
ollama pull qwen2.5:7b
ollama list
curl http://localhost:11434/api/tags
curl http://localhost:11434/api/chat \
  -d '{"model":"qwen2.5:7b","messages":[{"role":"user","content":"Responda apenas OK"}],"stream":false}'
```

Se o servidor tiver pouca memória, use um modelo menor, por exemplo `llama3.2:3b`, e ajuste:

```env
OLLAMA_MODEL=llama3.2:3b
```

Exemplo de serviço `systemd`:

```ini
[Unit]
Description=Sistema de Atas Disciplinares
After=network.target

[Service]
WorkingDirectory=/opt/ata_system
EnvironmentFile=/opt/ata_system/.env
ExecStart=/opt/ata_system/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
User=www-data
Group=www-data

[Install]
WantedBy=multi-user.target
```

O cliente do Ollama fica em `services/ollama_client.py`. Ali você pode ajustar:

- modelo padrão;
- instruções de escrita;
- regras obrigatórias do prompt;
- validação mínima da resposta antes de aceitar o texto gerado.

Acesse:

```text
http://127.0.0.1:8000
```

Usuário inicial:

```text
usuario: admin
senha: admin123
```

## Observações

- O banco SQLite é criado automaticamente em `ata_system/atas.db`.
- Os arquivos Word exportados ficam em `ata_system/exports`.
- A opção "Gerar com IA local" usa `OLLAMA_BASE_URL`/`OLLAMA_MODEL`. Se o Ollama falhar, estiver offline ou demorar demais, o sistema usa o gerador local como fallback.
- A chave de sessão em `main.py` deve ser alterada antes de uso em produção.
- Para alterar a senha do administrador, atualize o registro na tabela `usuarios` ou ajuste a rotina `criar_admin_padrao` em `auth.py` antes do primeiro start.
