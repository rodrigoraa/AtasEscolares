import os
from dataclasses import dataclass


class AgenteAtaIndisponivel(RuntimeError):
    pass


@dataclass(frozen=True)
class AgenteAtas:
    nome: str = "Agente de Atas Disciplinares"
    modelo_padrao: str = "llama3.1"

    @property
    def instrucoes(self) -> str:
        return (
            "Você é um agente especializado em atas escolares disciplinares da Escola Estadual São José. "
            "Sua função é transformar dados objetivos de uma ocorrência em uma minuta formal, clara, "
            "prudente e adequada ao Regimento Interno Escolar. Você deve preservar os fatos informados, "
            "não inventar detalhes, não intensificar indevidamente a conduta, não fazer juízo moral e não "
            "alterar o enquadramento regimental recebido do sistema. Entregue apenas o texto final da ata."
        )

    def montar_entrada(self, dados: dict, regra) -> str:
        responsavel = "sim" if dados["responsavel_convocado"] else "não"
        reincidencia = "sim" if dados["reincidencia"] else "não"
        observacoes = dados.get("observacoes_adicionais") or "nenhuma"
        nome_responsavel = dados.get("nome_responsavel") or "não informado"

        return f"""
Tarefa: redigir uma ata escolar disciplinar em português do Brasil.

Formato desejado:
- Parágrafo corrido, no estilo de ata escolar formal.
- Data por extenso.
- Descrição objetiva dos fatos.
- Registro da atuação da direção/coordenação.
- Citação expressa do Regimento Interno Escolar, artigo, inciso, gravidade e sanção.
- Orientação pedagógica e providências adotadas.
- Ciência ou convocação do responsável quando aplicável.
- Fechamento formal para acompanhamento e providências cabíveis.

Restrições:
- Não inclua título, número da ata, cabeçalho, assinaturas ou linhas de assinatura.
- Não use markdown, tópicos ou comentários.
- Não invente nomes, falas, testemunhas, objetos, datas, horários ou providências.
- Não omita o enquadramento regimental.
- Se o relato estiver simples, melhore a redação sem criar fatos novos.

Dados da ocorrência:
- Data: {dados["data_ocorrencia"].strftime("%d/%m/%Y")}
- Período/horário: {dados["periodo"]}
- Local: {dados["local"]}
- Estudante(s): {dados["alunos"]}
- Turma: {dados["turma"]}
- Tipo de ocorrência: {dados["tipo_ocorrencia"]}
- Relato simples dos fatos: {dados["relato_simples"]}
- Providências tomadas: {dados["providencias"]}
- Responsável convocado: {responsavel}
- Nome do responsável: {nome_responsavel}
- Reincidência: {reincidencia}
- Observações adicionais: {observacoes}

Enquadramento definido pelo sistema:
- Regimento: Regimento Interno Escolar
- Artigo: {regra.artigo}
- Inciso: {regra.inciso}
- Gravidade: {regra.gravidade}
- Sanção: {regra.sancao}
- Orientação regimental/pedagógica: {regra.orientacao}
""".strip()

    def modelo(self) -> str:
        return os.getenv("AI_MODEL") or os.getenv("OPENAI_MODEL") or self.modelo_padrao

    def base_url(self) -> str | None:
        return os.getenv("AI_BASE_URL") or os.getenv("OPENAI_BASE_URL")

    def api_key(self) -> str | None:
        if self.base_url():
            return os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY") or "local"
        return os.getenv("OPENAI_API_KEY")

    def validar_saida(self, texto: str, regra) -> str:
        texto = texto.strip()
        if not texto:
            raise AgenteAtaIndisponivel("A IA retornou texto vazio.")

        termos_obrigatorios = [
            "Regimento Interno Escolar",
            f"Art. {regra.artigo}",
            f"inciso {regra.inciso}",
        ]
        faltantes = [termo for termo in termos_obrigatorios if termo not in texto]
        if faltantes:
            raise AgenteAtaIndisponivel(
                "A IA não citou corretamente o enquadramento regimental."
            )

        return texto

    def gerar_ata(self, dados: dict, regra) -> str:
        api_key = self.api_key()
        if not api_key:
            raise AgenteAtaIndisponivel(
                "configure AI_BASE_URL para uma IA própria/local ou OPENAI_API_KEY para OpenAI."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AgenteAtaIndisponivel("Pacote openai não instalado.") from exc

        base_url = self.base_url()
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        try:
            if base_url:
                response = client.chat.completions.create(
                    model=self.modelo(),
                    messages=[
                        {"role": "system", "content": self.instrucoes},
                        {"role": "user", "content": self.montar_entrada(dados, regra)},
                    ],
                )
                texto = response.choices[0].message.content or ""
            else:
                response = client.responses.create(
                    model=self.modelo(),
                    instructions=self.instrucoes,
                    input=self.montar_entrada(dados, regra),
                )
                texto = response.output_text
        except Exception as exc:
            raise AgenteAtaIndisponivel(
                f"falha ao chamar a API de IA ({exc})."
            ) from exc

        return self.validar_saida(texto, regra)


agente_atas = AgenteAtas()
