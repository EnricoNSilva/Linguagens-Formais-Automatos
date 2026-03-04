from dataclasses import dataclass

@dataclass
class AFD:
	# Representação de um AFD completo em memória.
	
	estados: list[str] # conjunto de estados possíveis (q0, q1, ...)
	estado_inicial: str # estado inicial (ex.: q0)
	estados_aceitacao: set[str] # conjunto de estados de aceitação (ex.: {q1, q2})
	alfabeto: list[str] # conjunto de símbolos válidos (ex.: [0, 1] ou [a, b])
	transicoes: dict[str, dict[str, str]] # função de transição δ: estado_origem -> (simbolo -> estado_destino)
	testes: list[str] # palavras de teste para esse AFD
	nome: str | None = None


def parse_afds(texto: str) -> list[AFD]:
	# Quebra o texto em linhas e ignora linhas em branco.
	# Isso permite colar blocos com espaçamento entre eles.
	linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
	afds: list[AFD] = []
	i = 0

	while i < len(linhas):
		# Opcionalmente, aceita um rótulo de bloco como "a1:".
		nome = None
		if linhas[i].endswith(":"):
			nome = linhas[i][:-1]
			i += 1

		if i >= len(linhas):
			break

		# Lê as 4 linhas-base da definição do AFD:
		# 1) estados, 2) estado inicial, 3) estados de aceitação, 4) alfabeto.
		estados = linhas[i].split()
		i += 1
		estado_inicial = linhas[i].split()[0]
		i += 1
		estados_aceitacao = set(linhas[i].split())
		i += 1
		alfabeto = linhas[i].split()
		i += 1

		# Constrói a função de transição dinamicamente conforme o alfabeto.
		# Para cada estado, espera: estado_origem + 1 destino para cada símbolo.
		transicoes: dict[str, dict[str, str]] = {}
		for _ in range(len(estados)):
			partes = linhas[i].split()
			i += 1

			if len(partes) != len(alfabeto) + 1:
				raise ValueError(
					f"Linha de transição inválida: '{' '.join(partes)}'. "
					f"Esperado: estado + {len(alfabeto)} destinos."
				)

			estado_origem = partes[0]
			destinos = partes[1:]
			# Faz o pareamento símbolo -> destino na ordem do alfabeto.
			# Ex.: alfabeto [0,1] e linha "q0 q1 q0" vira:
			# transicoes["q0"] = {"0": "q1", "1": "q0"}
			transicoes[estado_origem] = {
				simbolo: destino for simbolo, destino in zip(alfabeto, destinos)
			}

		# Última linha do bloco: palavras de teste separadas por espaço.
		testes = linhas[i].split() if i < len(linhas) else []
		i += 1

		afds.append(
			AFD(
				estados=estados,
				estado_inicial=estado_inicial,
				estados_aceitacao=estados_aceitacao,
				alfabeto=alfabeto,
				transicoes=transicoes,
				testes=testes,
				nome=nome,
			)
		)

	return afds


def aceita(afd: AFD, palavra: str) -> bool:
	# Simulação clássica de AFD:
	# percorre a palavra símbolo a símbolo, atualizando o estado atual.
	estado_atual = afd.estado_inicial

	for simbolo in palavra:
		# Se aparecer símbolo fora do alfabeto do AFD, rejeita imediatamente.
		if simbolo not in afd.alfabeto:
			return False
		# Aplica a função de transição δ(estado_atual, simbolo).
		estado_atual = afd.transicoes[estado_atual][simbolo]

	# Aceita apenas se terminar em um estado final.
	return estado_atual in afd.estados_aceitacao


def main() -> None:
	# Entrada livre por múltiplas linhas para facilitar colar o enunciado inteiro.
	print("Digite a definição do(s) AFD(s). Finalize com Ctrl+Z e Enter (Windows).")
	texto_entrada = []
	try:
		while True:
			texto_entrada.append(input())
	except EOFError:
		pass

	# Faz o parsing de todos os blocos de AFD encontrados no texto.
	afds = parse_afds("\n".join(texto_entrada))

	# Para cada AFD, executa todas as palavras de teste e imprime verdadeiro/falso.
	for indice, afd in enumerate(afds, start=1):
		titulo = afd.nome if afd.nome else f"AFD {indice}"
		print(f"\n{titulo}:")
		for palavra in afd.testes:
			resultado = "verdadeiro" if aceita(afd, palavra) else "falso"
			print(f"{palavra}: {resultado}")


if __name__ == "__main__":
	main()
