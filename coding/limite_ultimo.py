def resistencia_calculo(pu, mu, ag, fyk, zx):
    print(' [bold]Verificação da resistência do perfil:')

    n_sd = abs(pu)
    n_rd = ag * (fyk / 10) / 1.10

    print(f' Força axial solicitante (Nsd): {n_sd:.2f} kN')
    print(f' Área do perfil (Ag): {ag:.2f} cm²')
    print(f' Resistência de escoamento (fyk): {fyk:.2f} MPa')
    print(f' Força axial resistente (Nrd): {n_rd:.2f} kN')

    m_sd = abs(mu)
    m_rd = zx * (fyk / 10) / (1.10 * 100)

    print(f' Momento fletor solicitante (Msd): {m_sd:.2f} kNm')
    print(f' Módulo de plastificação do perfil (Z): {zx:.2f} cm³')
    print(f' Resistência de escoamento (fyk): {fyk:.2f} MPa')
    print(f' Momento fletor resistente (Mrd): {m_rd:.2f} kNm')

    if n_sd > n_rd:
        print(' Atenção: solicitação maior que a resistência do perfil')

    if (n_sd / n_rd) >= 0.2:
        print(' Nsd / Nrd >= 0.2')
        x = (n_sd / n_rd) + ((8 / 9) * (m_sd / m_rd))
        print(f' (Nsd / Nrd) + (8 / 9) * (Msd / Mrd) = {x:.2f}')

    else:
        print(' Nsd / Nrd < 0.2')
        x = (n_sd / (2 * n_rd)) + (m_sd / m_rd)
        print(f' (Nsd / 2 Nrd) + (Msd / Mrd) = {x:.2f}')

    if x > 1:
        print('[italic] Atenção: Solicitação maior que a resistência do perfil')

    else:
        print('[italic] Resistência do perfil atende a solicitação')

    return x
