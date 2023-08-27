import math
import ch_dim
import chumbadores
import ch_ver
import converter


# IMPORTA LISTA DE CHUMBADORES DE "ancor_rod", VAMOS USAR PARA VERIFICAR DIMENSÕES DAS CHAPAS E CHUMBADORES
lista_chumbadores = [chumbadores.d3_4, chumbadores.d7_8, chumbadores.d1_0, chumbadores.d1__1_8,
                   chumbadores.d1__1_4, chumbadores.d1__1_2, chumbadores.d1__3_4, chumbadores.d2_0, chumbadores.d2__1_4,
                   chumbadores.d2__1_2, chumbadores.d2__3_4, chumbadores.d3_0, chumbadores.d3__1_4, chumbadores.d3__1_2,
                   chumbadores.d2__3_4, chumbadores.d4_0]

# FUNÇÃO QUE VAI RECEBER O CODIGO E VAI EXECUTAR APENAS AS FUNÇÕES NECESSARIAS PARA CADA MÉTODO


def dimensionamento(pu, vu, mu, fc, fy, d, bf, tw, tf, a2_a1, fyb, gr, phi, n_chumb, lig):
    if pu >= 0 and mu == 0 and vu != 0:
        for chumbador in lista_chumbadores:
            try:
                n_ch, b_ch, a1, a2, pp, tp, m, n, x, lmbd, lmbd_n, l, chumb_a1, chumb_a2 = ch_dim.compressao(pu, fc, fy, d, bf, tw, tf, phi, a2_a1, chumbador.a1, chumbador.a2, n_chumb, lig)
            except ValueError:
                print("\n Não é possível dimensionar ligação rotulada")
                print(" Distância entre mesas menor do que distância mínima dos chumbadores")
                return None

            fv, fnv, ft, fnt_lin, fta, fnt, fnt2 = ch_dim.cortante(0, vu, n_chumb, 2, chumbador.area, gr)
            if fv <= (0.975 * fnv) and ft <= fnt_lin:

                print('\n[bold] Dimensionamento da chapa de base:')
                print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.0f} mm')
                print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.0f} mm')
                print(f' Área de chapa (A1): {converter.in2_to_cm2(a1):.0f} cm²')
                print(f' Área de concreto (A2): {converter.in2_to_cm2(a2):.0f} cm²')
                print(f' Força resistente de compressão (pp): {converter.kips_to_kn(pp):.2f} kN')
                print(f' Força solicitante de compressão (pu): {converter.kips_to_kn(pu):.2f} kN')

                # print da espessura da chapa
                print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
                print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')
                print(f' X: {converter.in_to_mm(x):.2f} mm')
                print(f' \u03BB: {converter.in_to_mm(lmbd):.2f} mm')
                print(f" \u03BBn': {converter.in_to_mm(lmbd_n):.2f} mm")
                print(f' Dimensão crítica do balanço da chapa base (l): {converter.in_to_mm(l):.2f} mm')
                print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')

                # print cortante
                print('\n[bold] Verificação do cisalhamento nos chumbadores:')
                print(f' Diâmetro dos chumbadores {chumbador.nome}')
                print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
                print(f' Tensão resistente de cisalhamento (Fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')
                print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
                print(f' Tensão de tração total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
                print(f' Tensão resistente de tração (Fnt): {converter.ksi_to_mpa(fnt2):.2f} MPa')
                print(f' Tensão resistente de tração reduzida (\u03D5Fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
                print(f" Tensão resistente de tração final (\u03D5F'nt): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")

                hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, 0, fyb, gr)

                print(f'\n[bold] Resultados:')
                print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
                print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
                print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
                print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
                print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
                print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
                print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
                print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')

                return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef

            if chumbador.area == 12.6:  # O ÚLTIMO CHUMBADOR DA LISTA DE CHUMBADORES TEM ÁREA DE 12.6 in², OU SEJA, SE O "FOR" PASSAR POR TODOS OS CHUMBADORES E NENHUM ATENDER FT < FNT_LIN, ENTÃO ENTRAMOS NESSE IF
                print("\n Não é possível dimensionar ligação, nenhum chumbador atendeu às solicitações")
                return None

    elif pu >= 0 and mu == 0 and vu == 0:  # CÓDIGO 1002 É COMPRESSÃO, SEM CORTANTE E SEM MOMENTO
        for chumbador in lista_chumbadores:
            try:
                n_ch, b_ch, a1, a2, pp, tp, m, n, x, lmbd, lmbd_n, l, chumb_a1, chumb_a2 = ch_dim.compressao(pu, fc, fy, d, bf, tw, tf, phi,
                                                                                     a2_a1, chumbador.a1, chumbador.a2,
                                                                                     n_chumb, lig)
            except ValueError:
                print("\n Não é possível dimensionar ligação rotulada")
                print(" Distância entre mesas menor do que distância mínima dos chumbadores")
                return None

            print('\n[bold] Dimensionamento da chapa de base:')
            print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.0f} mm')
            print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.0f} mm')
            print(f' Área de chapa (A1): {converter.in2_to_cm2(a1):.0f} cm²')
            print(f' Área de concreto (A2): {converter.in2_to_cm2(a2):.0f} cm²')
            print(f' Força resistente de compressão (pp): {converter.kips_to_kn(pp):.2f} kN')
            print(f' Força solicitante de compressão (pu): {converter.kips_to_kn(pu):.2f} kN')
            print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
            print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')
            print(f' X: {x:.2f}')
            print(f' \u03BB: {lmbd:.2f}')
            print(f" \u03BBn': {converter.in_to_mm(lmbd_n):.2f} mm")
            print(f' Dimensão crítica do balanço da chapa base (l): {converter.in_to_mm(l):.2f} mm')
            print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')

            hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, 0, fyb, gr)

            print(f'\n[bold] Resultados:')
            print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
            print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
            print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
            print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
            print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
            print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
            print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
            print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')

            return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef

    elif pu >= 0 and mu != 0:  # COMPRESSÃO COM MOMENTO E CORTANTE OU PODE SER USADO PARA CORTANTE = 0 TAMBÉM
        i_chu = 0
        for chumbador in lista_chumbadores:
            i_chu = i_chu + 1
            var_chumb_a1 = chumbador.a1
            var_chumb_a2 = chumbador.a2

            if i_chu < 16:
                var_next_chumb_a1 = (lista_chumbadores[i_chu].a1)
            else:
                var_next_chumb_a1 = 8.661417323

            try:
                n_ch, b_ch, tp, tu, x, a1, a2, e, fp_max, q_max, e_crit, y, q, fp, m, n, f = ch_dim.momentos(pu, mu, fc, fy, phi, d, bf, tw, tf, a2_a1, var_chumb_a1, var_chumb_a2, n_chumb)
            except RecursionError:
                print("\n Não é possível dimensionar ligação")
                return None

            fv, fnv, ft, fnt_lin, fta, fnt, fnt2 = ch_dim.cortante(tu, vu, (n_chumb / 2), 2, chumbador.area, gr)
            if fv <= fnv and ft <= fnt_lin:
                chumb_a1 = var_chumb_a1
                chumb_a2 = (b_ch - (2 * var_chumb_a1)) / ((n_chumb / 2) - 1)
                print('\n[bold] Dimensionamento da chapa de base:')
                print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.2f} mm')
                print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.2f} mm')
                print(f' Excentricidade (e): {converter.in_to_mm(e):.2f} mm')
                print(f' Excentricidade crítica (e_crit): {converter.in_to_mm(e_crit):.2f} mm')
                print(f' Distância chumbador até o centro (f): {converter.in_to_mm(f):.2f} mm')
                print(f' Comprimento da compressão (y): {converter.in_to_mm(y):.2f} mm')
                if fp != 0:
                    print(f' Tensão na base (fp): {converter.ksi_to_mpa(fp):.2f} MPa')
                print(f' Tensão máxima na base (fp_max): {converter.ksi_to_mpa(fp_max):.2f} MPa')
                if q != 0:
                    print(f' Carga de compressão(q): {converter.kips_por_in_to_kn_por_mm(q):.2f} kN/mm')
                print(f' Carga de compressão máxima (q_max): {converter.kips_por_in_to_kn_por_mm(q_max):.2f} kN/mm')
                print(f' Força de tração nos chumbadores (tu): {converter.kips_to_kn(tu):.2f} kN')
                print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
                print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')
                print(f' Interface de flexão (x): {converter.in_to_mm(x):.2f} mm')
                print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')
                # print cortante
                print('\n[bold] Verificação da tensão nos chumbadores:')
                print(f' Diâmetro dos chumbadores {chumbador.nome}')
                print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
                print(f' Tensão resistente de cisalhamento (Fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')
                print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
                print(f' Tensão de tração total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
                print(f' Tensão resistente de tração (Fnt): {converter.ksi_to_mpa(fnt2):.2f} MPa')
                print(f' Tensão resistente de tração reduzida (\u03D5Fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
                print(f" Tensão resistente de tração final (\u03D5F'nt): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
                hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, (tu / (n_chumb / 2)), fyb, gr)
                print(f'\n[bold] Resultados:')
                print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
                print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
                print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
                print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
                print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
                print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
                print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
                print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')
                return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef
            else:
                while var_chumb_a1 <= (var_next_chumb_a1-0.0393700787401575):
                    var_chumb_a1 = var_chumb_a1 + 0.0393700787401575
                    var_chumb_a2 = 2 * var_chumb_a1

                    try:
                        n_ch, b_ch, tp, tu, x, a1, a2, e, fp_max, q_max, e_crit, y, q, fp, m, n, f = ch_dim.momentos(pu, mu, fc, fy, phi, d, bf, tw, tf, a2_a1, var_chumb_a1, var_chumb_a2, n_chumb)
                    except RecursionError:
                        print("\n Não é possível dimensionar ligação")
                        return None

                    fv, fnv, ft, fnt_lin, fta, fnt, fnt2 = ch_dim.cortante(tu, vu, (n_chumb / 2), 2, chumbador.area, gr)
                    if fv <= fnv and ft <= fnt_lin:
                        chumb_a1 = var_chumb_a1
                        chumb_a2 = (b_ch - (2 * var_chumb_a1)) / ((n_chumb / 2) - 1)
                        print('\n[bold] Dimensionamento da chapa de base:')
                        print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.2f} mm')
                        print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.2f} mm')
                        print(f' Excentricidade (e): {converter.in_to_mm(e):.2f} mm')
                        print(f' Excentricidade crítica (e_crit): {converter.in_to_mm(e_crit):.2f} mm')
                        print(f' Distância chumbador até o centro (f): {converter.in_to_mm(f):.2f} mm')
                        print(f' Comprimento da compressão (y): {converter.in_to_mm(y):.2f} mm')
                        if fp != 0:
                            print(f' Tensão na base (fp): {converter.ksi_to_mpa(fp):.2f} MPa')
                        print(f' Tensão máxima na base (fp_max): {converter.ksi_to_mpa(fp_max):.2f} MPa')
                        if q != 0:
                            print(f' Carga de compressão(q): {converter.kips_por_in_to_kn_por_mm(q):.2f} kN/mm')
                        print(f' Carga de compressão máxima (q_max): {converter.kips_por_in_to_kn_por_mm(q_max):.2f} kN/mm')
                        print(f' Força de tração nos chumbadores (tu): {converter.kips_to_kn(tu):.2f} kN')
                        print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
                        print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')
                        print(f' Interface de flexão (x): {converter.in_to_mm(x):.2f} mm')
                        print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')
                        # print cortante
                        print('\n[bold] Verificação da tensão nos chumbadores:')
                        print(f' Diâmetro dos chumbadores {chumbador.nome}')
                        print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
                        print(f' Tensão resistente de cisalhamento (Fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')
                        print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
                        print(f' Tensão de tração total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
                        print(f' Tensão resistente de tração (Fnt): {converter.ksi_to_mpa(fnt2):.2f} MPa')
                        print(f' Tensão resistente de tração reduzida (\u03D5Fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
                        print(f" Tensão resistente de tração final (\u03D5F'nt): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
                        hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, (tu / (n_chumb / 2)), fyb, gr)
                        print(f'\n[bold] Resultados:')
                        print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
                        print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
                        print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
                        print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
                        print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
                        print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
                        print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
                        print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')
                        return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef

            if chumbador.area == 12.6:
                print("\n Não é possível dimensionar ligação, nenhum chumbador atendeu às solicitações")
                return None

    elif pu < 0 and mu == 0 and vu != 0:  # CÓDIGO 1005 É TRAÇÃO COM CORTANTE
        pu = math.fabs(pu)
        for chumbador in lista_chumbadores:  # VAMOS RODAR A LISTA DE CHUMBADORES NOVAMENTO
            try:
                n_ch, b_ch, tp, ru, rn, mpl, moment_w, b_eff, chumb_a1, chumb_a2 = ch_dim.tracao(pu, d, bf, tw, tf, fy,
                                                                                                 gr, chumbador.a1,
                                                                                                 chumbador.a2,
                                                                                                 chumbador.area,
                                                                                                 n_chumb, lig)
            except ValueError:
                print("\n Não é possível dimensionar ligação rotulada")
                print(" Distância entre mesas menor do que distância mínima dos chumbadores")
                return None

            try:
                fv, fnv, ft, fnt_lin, fta, fnt, fnt2 = ch_dim.cortante(pu, vu, n_chumb, 2, chumbador.area, gr)
                if fv <= fnv and ft <= fnt_lin:  # SE SOLICITAÇÃO FOR MENOR QUE RESISTENCIA
                    a1 = n_ch * b_ch
                    a2 = a1 * a2_a1

                    print('\n[bold] Dimensionamento da chapa de base:')
                    print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.0f} mm')
                    print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.0f} mm')
                    print(f' Área de chapa (A1): {converter.in2_to_cm2(a1):.0f} cm²')
                    print(f' Área de concreto (A2): {converter.in2_to_cm2(a2):.0f} cm²')

                    # print da tração
                    print(f' Força de tração por chumbador (ru): {converter.kips_to_kn(ru):.2f} kN')
                    print(f' Força de tração resistente (rn): {converter.kips_to_kn(rn):.2f} kN')
                    if mpl != 0:
                        print(f' Momento na chapa gerado pelos chumbadores (Mpl): {converter.kips_to_kn(mpl):.2f} kN.mm/mm')
                    if moment_w != 0:
                        print(f' Momento na chapa gerado pelos chumbadores (Mu): {converter.kips_in_to_knmm(moment_w):.2f} kN.mm')
                        print(f' Comprimento do plano de flexão da chapa (b eef): {converter.in_to_mm(b_eff):.2f} mm')
                    print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')

                    # print cortante
                    print('\n[bold] Verificação da tensão nos chumbadores:')
                    print(f' Diâmetro dos chumbadores {chumbador.nome}')
                    print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
                    print(f' Tensão resistente de cisalhamento (fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')
                    print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
                    print(f' Tensão de tração total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
                    print(f' Tensão resistente de tração (fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
                    print(f" Tensão resistente de tração final (fnt'): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")

                    hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, (pu / n_chumb), fyb, gr)

                    print(f'\n[bold] Resultados:')
                    print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
                    print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
                    print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
                    print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
                    print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
                    print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
                    print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
                    print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')

                    return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef

            except ValueError:
                pass

            if chumbador.area == 12.6:
                print("\n Não é possível dimensionar ligação, nenhum chumbador atendeu às solicitações")
                return None

    elif pu < 0 and mu == 0 and vu == 0:  # CÓDIGO 1006 SOMENTE TRAÇÃO
        pu = math.fabs(pu)  # PEGAR O MÓDULO DO VALOR DE PU
        for chumbador in lista_chumbadores:  # VAI RODAR TODOS OS CHUMBADORES DA LISTA DE CHUMBADORES, DO MENOR PARA O MAIOR
            try:
                n_ch, b_ch, tp, ru, rn, mpl, moment_w, b_eff, chumb_a1, chumb_a2 = ch_dim.tracao(pu, d, bf, tw, tf, fy,
                                                                                                 gr, chumbador.a1,
                                                                                                 chumbador.a2,
                                                                                                 chumbador.area,
                                                                                                 n_chumb, lig)
                a1 = n_ch * b_ch
                a2 = a1 * a2_a1

                print('\n[bold] Dimensionamento da chapa de base:')
                print(f' Comprimento da chapa (N): {converter.in_to_mm(n_ch):.0f} mm')
                print(f' Largura da chapa (B): {converter.in_to_mm(b_ch):.0f} mm')
                print(f' Área de chapa (A1): {converter.in2_to_cm2(a1):.0f} cm²')
                print(f' Área de concreto (A2): {converter.in2_to_cm2(a2):.0f} cm²')

                # print da tração
                print(f' Força de tração por chumbador (Ru): {converter.kips_to_kn(ru):.2f} kN')
                print(f' Força de tração resistente (Rn): {converter.kips_to_kn(rn):.2f} kN')
                if mpl != 0:
                    print(
                        f' Momento na chapa gerado pelos chumbadores (Mpl): {converter.kips_to_kn(mpl):.2f} kN.mm/mm')
                if moment_w != 0:
                    print(
                        f' Momento na chapa gerado pelos chumbadores (Mu): {converter.kips_in_to_knmm(moment_w):.2f} kN.mm')
                    print(f' Comprimento do plano de flexão da chapa (b eef): {converter.in_to_mm(b_eff):.2f} mm')
                print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')

                hef = ch_dim.comprimento_ancoragem(chumbador.diametro, chumbador.area, fc, (pu / n_chumb), fyb, gr)

                print(f'\n[bold] Resultados:')
                print(f' Comprimento da chapa base (N): {converter.in_to_mm(n_ch):.2f} mm')
                print(f' Largura da chapa base (B): {converter.in_to_mm(b_ch):.2f} mm')
                print(f' Espessura da chapa base (tp): {converter.in_to_mm(tp):.2f} mm')
                print(f' Área de chapa base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
                print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')
                print(f' {n_chumb:.0f} Chumbadores de {chumbador.nome}')
                print(f' Distância do chumbador até a borda da chapa (a1): {converter.in_to_mm(chumb_a1):.2f} mm')
                print(f' Distância entre chumbadores (a2): {converter.in_to_mm(chumb_a2):.2f} mm')

                return n_ch, b_ch, tp, chumbador.nome, chumb_a1, chumb_a2, a2, a1, hef

            except:
                pass

            if chumbador.area == 12.6:
                print("\n Não é possível dimensionar ligação, nenhum chumbador atendeu às solicitações")
                return None

    elif pu < 0 and mu != 0:  # CÓDIGO 1007 É TRAÇÃO COM MOMENTOS - NÃO ENGLOBADO NO TRABALHO
        print("\n Não é possível dimensionar ligação, solicitações não abrangidas")
        return None


def verificacao(pu, vu, mu, fc, fy, d, bf, tw, tf, a2, a1_chumb, a2_chumb, ar_chumb, chumb_diam, fyb, gr, phi, a1, n_ch,
                b_ch, tp, n_chumb, lig, hef):
    if pu >= 0 and mu == 0 and vu != 0:  # CÓDIGO 1001 É COMPRESSÃO COM CORTANTE E MOMENTO = 0
        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            ch_ver.compressao(pu, fy, fc, phi, a1, a2, n_ch, b_ch, d, bf, tp)
            ch_ver.cortante_compressao(pu, vu, tp, ar_chumb, 2, gr, fc, n_ch, b_ch)
            ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, 0, fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu >= 0 and mu == 0 and vu == 0:  # CÓDIGO 1002 É COMPRESSÃO, SEM CORTANTE E SEM MOMENTO
        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            ch_ver.compressao(pu, fy, fc, phi, a1, a2, n_ch, b_ch, d, bf, tp)
            ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, 0, fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu >= 0 and mu != 0 and vu != 0:  # CÓDIGO 1003 É COMPRESSÃO COM MOMENTO E CORTANTE
        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            e, fp_max, q_max, e_crit = ch_ver.excentricidade(pu, mu, fc, phi, b_ch, n_ch, a2)
            if e <= e_crit:
                ch_ver.pequenos_momentos(pu, fy, d, bf, n_ch, b_ch, tp, e, e_crit, q_max)
                ch_ver.cortante_compressao(pu, vu, tp, ar_chumb, 2, gr, fc, n_ch, b_ch)
                ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, 0, fyb, gr, hef)
            else:
                tu = ch_ver.grandes_momentos(pu, mu, fc, fy, b_ch, n_ch, e, e_crit, q_max, d, bf, tf, phi, a2, fp_max, a1_chumb, a2_chumb, tp)
                ch_ver.cortante_tracao(tu, vu, tp, ar_chumb, (n_chumb / 2), 2, gr)
                ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, (tu / (n_chumb / 2)), fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu >= 0 and mu != 0 and vu == 0:  # CÓDIGO 1004 É COMPRESSÃO E MOMENTO, CORTANTE É NULO
        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            e, fp_max, q_max, e_crit = ch_ver.excentricidade(pu, mu, fc, phi, b_ch, n_ch, a2)
            if e <= e_crit:
                ch_ver.pequenos_momentos(pu, fy, d, bf, n_ch, b_ch, tp, e, e_crit, q_max)
                ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, 0, fyb, gr, hef)
            else:
                tu = ch_ver.grandes_momentos(pu, mu, fc, fy, b_ch, n_ch, e, e_crit, q_max, d, bf, tf, phi, a2, fp_max, a1_chumb, a2_chumb, tp)
                ch_ver.cortante_tracao(tu, 0, tp, ar_chumb, (n_chumb / 2), 2, gr)
                ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, (tu / (n_chumb / 2)), fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu < 0 and mu == 0 and vu != 0:  # CÓDIGO 1005 É TRAÇÃO COM CORTANTE
        pu = math.fabs(pu)  # COMEÇAMOS CONVERTENDO O VALOR NEGATIVO DA FORÇA AXIAL PARA POSITIVO

        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            ch_ver.tracao(pu, fy, gr, d, bf, tw, tf, n_ch, b_ch, tp, ar_chumb, a1_chumb, a2_chumb, n_chumb)
            ch_ver.cortante_tracao(pu, vu, tp, ar_chumb, n_chumb, 2, gr)
            ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, (pu / n_chumb), fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu < 0 and mu == 0 and vu == 0:  # CÓDIGO 1006 SOMENTE TRAÇÃO
        pu = math.fabs(pu)  # PEGAR O MÓDULO DO VALOR DE PU

        try:
            ch_ver.area_concreto(a1, a2, n_ch, b_ch)
            ch_ver.tracao(pu, fy, gr, d, bf, tw, tf, n_ch, b_ch, tp, ar_chumb, a1_chumb, a2_chumb, n_chumb)
            ch_ver.comprimento_ancoragem(chumb_diam, ar_chumb, fc, (pu / n_chumb), fyb, gr, hef)

        except ValueError:
            raise ValueError()

    elif pu < 0 and mu != 0:  # CÓDIGO 1007 É TRAÇÃO COM MOMENTOS - NÃO ENGLOBADO NO TRABALHO
        print("\n Não é possível dimensionar ligação, solicitações não abrangidas")
        return None
