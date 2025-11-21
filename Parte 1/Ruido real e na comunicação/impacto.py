import numpy as np
import matplotlib.pyplot as plt
from functions.funcoes import *

mensagem_bits = "10001101010011001011110"
num_bits = len(mensagem_bits)

modulacoes = {
    "NRZ": (encode_nrz, decode_nrz),
    "Manchester": (encode_manchester, decode_manchester)
}

## Faixa
SNR_values = np.arange(20, -201, -1)

resultados = {}

for nome, (encode, decode) in modulacoes.items():
    print(f"\nModulação {nome}")

    sinal_limpo = encode(mensagem_bits)
    num_erros_mod = []
    primeiros_bits_snr = None
    todos_bits_snr = None
    bits_comprometidos = np.zeros(num_bits, dtype=bool)

    for snr in SNR_values:

        sinal_ruidoso = adicionar_ruido(sinal_limpo, snr_db=snr)
        mensagem_decodificada = decode(sinal_ruidoso, num_bits)

        erros = sum(a != b for a, b in zip(mensagem_bits, mensagem_decodificada))
        num_erros_mod.append(erros)

        #bits com falhas
        for i, (o, d) in enumerate(zip(mensagem_bits, mensagem_decodificada)):
            if o != d:
                bits_comprometidos[i] = True

        #Primeiro SNR - erros
        if primeiros_bits_snr is None and erros > 0:
            primeiros_bits_snr = snr

        #Primeiro SNR - com tods os bits comprometidos
        if todos_bits_snr is None and bits_comprometidos.all():
            todos_bits_snr = snr

    resultados[nome] = {
        "primeiros": primeiros_bits_snr,
        "todos": todos_bits_snr,
        "erros": num_erros_mod
    }

    print(f"   a) Primeiros erros em: {primeiros_bits_snr} dB")
    print(f"   b) Todos os bits comprometidos em: {todos_bits_snr} dB")

##GRÁFICO 

for nome in modulacoes.keys():
    plt.figure(figsize=(10,5))
    plt.plot(SNR_values, resultados[nome]["erros"], label=nome)

    plt.xlabel("SNR (dB)")
    plt.ylabel("Número de erros")
    plt.title(f"Gráfico: valor de SNR x número de erros — {nome}")
    plt.grid(True)
    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()

