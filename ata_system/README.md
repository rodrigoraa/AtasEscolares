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

Para gerar textos com uma IA própria/local, configure no arquivo `.env` um endpoint compatível com OpenAI.

Exemplo com Ollama no mesmo servidor:

```env
AI_BASE_URL=http://localhost:11434/v1
AI_MODEL=llama3.1
AI_API_KEY=local
SESSION_SECRET_KEY=troque-por-uma-chave-grande-e-aleatoria
```

Exemplo com uma IA em outro servidor da rede:

```env
AI_BASE_URL=http://192.168.1.50:11434/v1
AI_MODEL=llama3.1
AI_API_KEY=local
SESSION_SECRET_KEY=troque-por-uma-chave-grande-e-aleatoria
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

O agente de IA do projeto fica em `services/agente_atas.py`. Ali você pode ajustar:

- nome do agente;
- modelo padrão;
- instruções de escrita;
- regras obrigatórias do prompt;
- validação mínima da resposta antes de aceitar o texto gerado.

Também é possível usar OpenAI se quiser, mas é opcional:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_MODEL=gpt-5.2
```

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
- A opção "Gerar texto com IA configurada" usa `AI_BASE_URL`/`AI_MODEL` para IA própria/local, ou `OPENAI_API_KEY` se você optar pela OpenAI. Se a IA falhar, o sistema usa o gerador local como fallback.
- A chave de sessão em `main.py` deve ser alterada antes de uso em produção.
- Para alterar a senha do administrador, atualize o registro na tabela `usuarios` ou ajuste a rotina `criar_admin_padrao` em `auth.py` antes do primeiro start.
