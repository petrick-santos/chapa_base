def entrada_dim(pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, a2_a1, grade, n_chumb, lig):
    print(' Dados de entrada:')
    print(' Solicitações:')
    print(f' Força axial (Pu): {pu} kN')
    print(f' Cortante (Vu): {vu} kN')
    print(f' Momento fletor (Mu): {mu} kN.m')

    print('\n Informações do perfil:')
    print(f' Nome do perfil: {nome}')
    print(f' Altura do perfil (d): {d} mm')
    print(f' Largura do perfil (bf): {bf} mm')
    print(f' Espessura da alma (tw): {tw} mm')
    print(f' Espessura da mesa (tf): {tf} mm')
    print(f' Área da seção do perfil (Ag): {ag:.1f} cm²')
    print(f' Resistência do aço (fy): {fyk} MPa')

    print(f'\n Base de concreto:')
    print(f' Resistência do concreto (fc): {fc} MPa')
    print(f' Proporção área de concreto e área de chapa (A2/A1): {a2_a1}')

    print('\n Chapa base:')
    print(f' Resistência do aço (fy): {fy} MPa')

    print(f'\n Chumbadores:')
    if lig == "e":
        print(' Ligação de base engastada')
    elif lig == "r":
        print(' Ligação de base rotulada')
    print(f' Número de chumbadores da ligação {n_chumb:.0f}')
    print(f' Material dos chumbadores: ASTM F1554 {grade}')

def entrada_verif(pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, a2, n_ch, b_ch, tp, grade, chumb_nome, dist_a1,
                  dist_a2, a1, n_chumb, lig, hef):
    print(' Dados de entrada:')
    print(' Solicitações:')
    print(f' Força axial (Pu): {pu} kN')
    print(f' Cortante (Vu): {vu} kN')
    print(f' Momento fletor (Mu): {mu} kN.m')

    print('\n Informações do perfil:')
    print(f' Nome do perfil: {nome}')
    print(f' Altura do perfil (d): {d} mm')
    print(f' Largura do perfil (bf): {bf} mm')
    print(f' Espessura da alma (tw): {tw} mm')
    print(f' Espessura da mesa (tf): {tf} mm')
    print(f' Área da seção do perfil (Ag): {ag:.1f} cm²')
    print(f' Resistência do aço (fy): {fyk} MPa')

    print(f'\n Base de concreto:')
    print(f" Resistência do concreto (f'c): {fc} MPa")
    print(f' Área de concreto (A2): {a2} cm²')

    print('\n Chapa base:')
    print(f' Resistência do aço (fy): {fy} MPa')
    print(f' Comprimento da chapa base (N): {n_ch} mm')
    print(f' Largura de chapa base (B): {b_ch} mm')
    print(f' Espessura de chapa base (tp): {tp} mm')
    print(f' Área de chapa base (A1): {a1:.2f} cm²')

    print(f'\n Chumbadores:')
    if lig == "e":
        print(' Ligação de base engastada')
    elif lig == "r":
        print(' Ligação de base rotulada')
    print(f' Número de chumbadores da ligação {n_chumb}')
    print(f' Diâmetro dos chumbadores: {chumb_nome}')
    print(f' Embutimento dos chumbadores {hef} mm')
    print(f' Material dos chumbadores: ASTM F1554 {grade}')
    print(f' Distância (a1): {dist_a1} mm')
    print(f' Distânci (a2): {dist_a2} mm')
