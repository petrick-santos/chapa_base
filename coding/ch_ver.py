import math
import converter


def area_concreto(a1, a2, n_ch, b_ch):
    print('\n[bold] Verificação da área da chapa de base:')
    print(f' Área de chapa de base (A1): {converter.in2_to_cm2(a1):.2f} cm²')
    print(f' Área da base de concreto (A2): {converter.in2_to_cm2(a2):.2f} cm²')

    if a1 > a2:
        print(f' (A1) {converter.in2_to_cm2(a1):.2f} cm² > (A2) {converter.in2_to_cm2(a2):.2f} cm²')
        print('[italic] Não passou na verificação')
        raise ValueError()

    else:
        print('[italic] A1 \u2264 A2 - Verificação das áreas ok')


def compressao(pu, fy, fc, phi, a1, a2, n_ch, b_ch, d, bf, tp):
    print('\n[bold] Verificação da chapa de base para compressão:')
    pp = min(phi * 0.85 * fc * a1 * math.sqrt(a2 / a1), 2 * phi * 0.85 * fc * a1)
    print(f' Força axial solicitante (Pu): {converter.kips_to_kn(pu):.2f} kN')
    print(f' Força axial resistente (Pp): {converter.kips_to_kn(pp):.2f} kN')

    if pp < pu:
        print(f' (Pu) {converter.kips_to_kn(pu):.2f} kN > (Pp) {converter.kips_to_kn(pp):.2f} kN')
        print(f'[italic] Não passou na verificação')
        raise ValueError()

    else:
        print(f' (Pu) {converter.kips_to_kn(pu):.2f} kN < (Pp) {converter.kips_to_kn(pp):.2f} kN')

    m = (n_ch - (0.95 * d)) / 2
    n = (b_ch - (0.8 * bf)) / 2
    x = ((4 * d * bf) / ((d + bf) ** 2)) * (pu / pp)
    lmbd = min((2 * math.sqrt(x) / (1 + math.sqrt(1 - x))), 1)
    lmbd_n = lmbd * (math.sqrt(d * bf) / 4)
    l = max(m, n, lmbd_n)
    tp_min = l * math.sqrt((2 * pu) / (0.90 * fy * b_ch * n_ch))

    print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
    print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')
    print(f' X: {x:.2f}')
    print(f' \u03BB: {lmbd:.2f}')
    print(f" \u03BBn': {converter.in_to_mm(lmbd_n):.2f} mm")
    print(f' Dimensão crítica do balanço da chapa base (l): {converter.in_to_mm(l):.2f} mm')
    print(f' Espessura mínima (tp min): {converter.in_to_mm(tp_min):.2f} mm')
    print(f' Espessura da chapa (tp): {converter.in_to_mm(tp):.2f} mm')

    if tp < tp_min:
        print(f' tp {converter.in_to_mm(tp):.2f} mm < tp min {converter.in_to_mm(tp_min):.2f} mm')
        print(f'[italic] Não passou na verificação')
        raise ValueError()

    else:
        print(f' tp {converter.in_to_mm(tp):.2f} mm \u2265 tp min {converter.in_to_mm(tp_min):.2f} mm')
        print('[italic] Verificação da espessura ok')
        return None


def tracao(pu, fy, gr, d, bf, tw, tf, n_ch, b_ch, tp, ar_chumb, a1_chumb, a2_chumb, n_chumb):
    ru = pu / n_chumb
    rn = 0.75 * 0.75 * gr * ar_chumb

    print(f' Força de tração por chumbador (Ru): {converter.kips_to_kn(ru):.2f} kN')
    print(f' Força de tração resistente (Rn): {converter.kips_to_kn(rn):.2f} kN')

    if rn < ru:
        print(f' (Rn) {converter.kips_to_kn(rn):.2f} kN < (Ru) {converter.kips_to_kn(ru):.2f} kN')
        print('[italic] Não passou na verificação')
        raise ValueError()

    else:
        print(f' (Rn) {converter.kips_to_kn(rn):.2f} kN \u2265 (Ru) {converter.kips_to_kn(ru):.2f} kN')

    a3_chumb = n_ch - (2 * a1_chumb)  # distancia entre chumbadores em relação a altura da chapa
    dist_chum_mesa = ((d - a3_chumb) / 2) - tf  # distancia quando chumbadores internos
    dist_chum_mesa = round(dist_chum_mesa, 5)
    dist_chum_alma = (a2_chumb - tw) / 2
    dist_chum_alma = round(dist_chum_alma, 5)

    if d > a3_chumb:  # se chumbadores alinhados com as mesas ou internos / calculamos momento em relação a alma
        if dist_chum_mesa < dist_chum_alma:  # Chumbadores mais proximos da mesa
            if dist_chum_mesa <= 0:
                moment_w = ru * tf
                b_eff = 2 * tf
                print(' Chumbadores localizados sob a mesa do perfil')
            else:
                moment_w = 2 * ru * dist_chum_mesa
                b_eff = min(4 * dist_chum_mesa, (2 * dist_chum_mesa) + (b_ch - a2_chumb))
                print(' Chumbadores localizados entre as mesas do perfil')

            tp_min = math.sqrt((moment_w * 4) / (b_eff * 0.90 * fy))

            print(' Flexão em relação a mesa do perfil')
            print(f' Momento na chapa gerado pelos chumbadores (Mu): {converter.kips_in_to_knmm(moment_w):.2f} kN.mm')
            print(f' Comprimento do plano de flexão da chapa (b eef): {converter.in_to_mm(b_eff):.2f} mm')
            print(f' Espessura mínima da chapa (tp_min): {converter.in_to_mm(tp_min):.2f} mm')

        else:
            if dist_chum_alma <= 0:
                moment_w = ru * tw
                b_eff = 2 * tw
                print(' Chumbadores localizados sob a alma do perfil')

            else:
                moment_w = 2 * ru * dist_chum_alma  # momento para 2 chumbadores
                b_eff = min(4 * dist_chum_alma, (2 * dist_chum_alma) + a3_chumb)
                print(' Chumbadores localizados entre as mesas do perfil')

            tp_min = math.sqrt((moment_w * 4) / (b_eff * 0.90 * fy))

            print(' Flexão em relação a alma do perfil')
            print(f' Momento na chapa gerado pelos chumbadores (Mu): {converter.kips_in_to_knmm(moment_w):.2f} kN.mm')
            print(f' Comprimento do plano de flexão da chapa (b eef): {converter.in_to_mm(b_eff):.2f} mm')
            print(f' Espessura mínima da chapa (tp_min): {converter.in_to_mm(tp_min):.2f} mm')

        if tp < tp_min:
            print(f' tp {converter.in_to_mm(tp):.2f} mm < tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Não passou na verificação')
            raise ValueError()

        else:
            print(f' tp {converter.in_to_mm(tp):.2f} mm \u2265 tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Verificação da espessura - ok')
            return None

    else:
        tu = pu / 2
        x = (n_ch / 2) - a1_chumb - (d / 2) + (tf / 2)
        mpl = (tu * x) / b_ch
        tp_min = 2.11 * math.sqrt((tu * x) / (b_ch * fy))

        print(' Chumbadores localizados no lado externo do perfil')
        print(f' Força de flexão na chapa (tu): {converter.kips_to_kn(tu):.2f} kN')
        print(f' Distância do eixo dos chumbadores até plano de flexão da chapa (x): {converter.in_to_mm(x):.2f} mm')
        print(f' Momento na chapa gerado pelos chumbadores (Mpl): {converter.kips_to_kn(mpl):.2f} kN.mm/mm')
        print(f' Espessura mínima da chapa (tp_min): {converter.in_to_mm(tp_min):.2f} mm')

        if tp < tp_min:
            print(f' tp {converter.in_to_mm(tp):.2f} mm < tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Não passou na verificação')
            raise ValueError()

        else:
            print(f' tp {converter.in_to_mm(tp):.2f} mm \u2265 tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Verificação da espessura - ok')
            return None


def cortante_tracao(pu, vu, tp, ar_chumb, tra_rod, num_rod, gr):
    print('\n[bold] Verificação da tensão nos chumbadores:')
    fv = 1.25 * vu / (num_rod * ar_chumb)  # CORTANTE NOS CHUMBADORES
    fta = pu / (tra_rod * ar_chumb)  # TENSÃO CAUSADA PELA TRAÇÃO
    ft = fta  # SOMA DAS TENSÕES

    fnt = 0.75 * 0.75 * gr  # TENSÃO RESISTENTE
    fnt2 = 0.75 * gr
    fnv = 0.45 * gr  # CORTANTE RESISTENTE
    fnt_lin = min(0.75 * (1.3 * fnt2 - (fnt2 * fv / (0.75 * fnv))), fnt)  # VERIFICAÇÃO

    print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
    print(f' Tensão resistente de cisalhamento (Fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')
    print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
    print(f' Tensão de tração total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
    print(f' Tensão resistente de tração (Fnt): {converter.ksi_to_mpa(fnt2):.2f} MPa')
    print(f' Tensão resistente de tração reduzida (\u03D5Fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
    print(f" Tensão resistente de tração final (\u03D5F'nt): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")

    if fnt_lin <= 0:
        print(f" \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa \u2264 0 MPa")
        print('[italic] Não passou na verificação')
        raise ValueError()

    if ft <= fnt_lin:
        print(f" ft {converter.ksi_to_mpa(ft):.2f} MPa \u2264 \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
        print('[italic] Verificação dos chumbadores - ok')
        return None

    else:
        print(f" ft {converter.ksi_to_mpa(ft):.2f} MPa > \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
        print('[italic] Não passou na verificação')
        raise ValueError()


def cortante_compressao(pu, vu, tp, ar_chumb, num_rod, gr, fc, n_ch, b_ch):
    print('\n[bold] Verificação da tensão nos chumbadores:')
    fv = 1.25 * vu / (num_rod * ar_chumb)  # CORTANTE NOS CHUMBADORES
    fta = 0  # TENSÃO CAUSADA PELA TRAÇÃO É ZERO, POIS ESTÁ EM COMPRESSÃO
    ft = fta  # TENSÃO TOTAL

    fnt = 0.75 * 0.75 * gr  # TENSÃO RESISTENTE
    fnt2 = 0.75 * gr
    fnv = 0.45 * gr  # CORTANTE RESISTENTE
    fnt_lin = min(0.75 * (1.3 * fnt2 - (fnt2 * fv / (0.75 * fnv))), fnt)  # VERIFICAÇÃO

    print(f' Tensão de cisalhamento (fv): {converter.ksi_to_mpa(fv):.2f} MPa')
    print(f' Tensão resistente de cisalhamento (Fnv): {converter.ksi_to_mpa(fnv):.2f} MPa')

    print(f' Tensão causada pela força de tração (fta): {converter.ksi_to_mpa(fta):.2f} MPa')
    print(f' Tensão total (ft): {converter.ksi_to_mpa(ft):.2f} MPa')
    print(f' Tensão resistente de tração (Fnt): {converter.ksi_to_mpa(fnt2):.2f} MPa')
    print(f' Tensão resistente de tração reduzida (\u03D5Fnt): {converter.ksi_to_mpa(fnt):.2f} MPa')
    print(f" Tensão resistente de tração final (\u03D5F'nt): {converter.ksi_to_mpa(fnt_lin):.2f} MPa")

    if fnt_lin <= 0:
        print(f" \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa \u2264 0 MPa")
        print('[italic] Não passou na verificação')
        raise ValueError()

    if ft <= fnt_lin:
        print(f" ft {converter.ksi_to_mpa(ft):.2f} MPa \u2264 \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
        print('[italic] Verificação dos chumbadores - ok')
        return None

    else:
        print(f" ft {converter.ksi_to_mpa(ft):.2f} MPa > \u03D5F'nt {converter.ksi_to_mpa(fnt_lin):.2f} MPa")
        print('[italic] Não passou na verificação')
        raise ValueError()


def excentricidade(pu, mu, fc, phi, b_ch, n_ch, a2):
    a1 = b_ch * n_ch  # AREA DA CHAPA BASE
    e = mu / pu  # EXCENTRICIDADE DA CARGA

    fp = pu / a1
    print(f' Tensão da força axial pela área de chapa (fp): {converter.ksi_to_mpa(fp):.2f} MPa')

    fp_max = min(phi * 0.85 * fc * math.sqrt(a2 / a1), phi * 0.85 * fc * 2)  # fp_max CONFORME MATERIAL

    print(f' Tensão de compressão máxima entre chapa e concreto (fp_max): {converter.ksi_to_mpa(fp_max):.2f} MPa')

    if fp > fp_max:
        print('[italic] Não passou na verificação, tensão acima do limite')
        raise ValueError()

    else:
        q_max = fp_max * b_ch  # q_max CONFORME MATERIAL
        e_crit = (n_ch / 2) - (pu / (2 * q_max))  # e_critico

        print(f' Carga linear de compressão máxima (q_max): {converter.kips_por_in_to_kn_por_mm(q_max):.2f} kN/mm')
        print(f' Excentricidade (e): {converter.in_to_mm(e):.2f} mm')
        print(f' Excentricidade crítica (e_crítico): {converter.in_to_mm(e_crit):.2f} mm')

        return e, fp_max, q_max, e_crit  # RETORNA VALORES PARA SEREM USADOS NAS OUTRAS FUNÇÕES


def pequenos_momentos(pu, fy, d, bf, n_ch, b_ch, tp, e, e_crit, q_max):
    if e == e_crit:
        y = pu / q_max
        q = q_max

    else:
        y = n_ch - (2 * e)
        q = pu / y

    if q <= q_max:
        fp = pu / (b_ch * y)
        m = (n_ch - (0.95 * d)) / 2
        n = (b_ch - (0.80 * bf)) / 2

        if y >= m:
            tp_m = 1.5 * m * math.sqrt(fp / fy)
        else:
            tp_m = 2.11 * math.sqrt((fp * y * (m - (y / 2))) / fy)

        tp_n = 1.5 * n * math.sqrt(fp / fy)

        tp_min = max(tp_m, tp_n)

        print(f' Excentricidade (e): {converter.in_to_mm(e):.2f} mm < Excentricidade crítica (e_crítico): {converter.in_to_mm(e_crit):.2f} mm')
        print(f' Comprimento da carga de compressão (Y): {converter.in_to_mm(y):.2f} mm')
        print(f' Carga linear de compressão (q): {converter.kips_por_in_to_kn_por_mm(q):.2f} kN/mm')
        print(f' Tensão de compressão (fp): {converter.ksi_to_mpa(fp):.2f} MPa')

        print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')
        print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')

        print(f' Espessura mínima (tp_min): {converter.in_to_mm(tp_min):.2f} mm')

        if tp < tp_min:
            print(f' tp {converter.in_to_mm(tp):.2f} mm < tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Não passou na verificação')
            raise ValueError()

        else:
            print(f' tp {converter.in_to_mm(tp):.2f} mm \u2265 tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Verificação da espessura - ok')
            return None

    else:
        print(f' Carga linear (q) {converter.kips_por_in_to_kn_por_mm(q):.2f} kN/mm > Carga linear máxima (q_max) {converter.kips_por_in_to_kn_por_mm(q_max):.2f} kN/mm')
        print('[italic] Não passou na verificação')
        raise ValueError()


def grandes_momentos(pu, mu, fc, fy, b_ch, n_ch, e, e_crit, q_max, d, bf, tf, phi, a2, fp_max, a1_chumb, a2_chumb, tp):  # CALCULO PARA LARGE MOMENTS (e > e_critico)
    print(f' Excentricidade (e): {converter.in_to_mm(e):.2f} mm > Excentricidade crítica (e_crítica): {converter.in_to_mm(e_crit):.2f} mm')
    print(f' Carga linear (q) = Carga linear máxima (q_max): {converter.kips_por_in_to_kn_por_mm(q_max):.2f} kN/mm ')
    f = (n_ch / 2) - a1_chumb  # DISTANCIA CHUMBADOR ATÉ CENTRO DA CHAPA
    print(f' Distância dos chumbadores ao eixo (f): {converter.in_to_mm(f):.2f} mm')

    x = (n_ch / 2) - (d / 2) - a1_chumb + (tf / 2)
    x = round(x, 10)  # X DA PROBLEMA SE TEM MUITAS CASAS DECIMAIS

    if x < 0:
        print(f' Distância dos chumbadores à interface de tensão (x): {converter.in_to_mm(x):.2f} mm')
        print('[italic] Não passou na verificação, chumbadores incorretamente posicionados')
        raise ValueError()

    elif x == 0:
        x = abs(x)  # X RETORNOU -0.00 ALGUMAS VEZES

    print(f' Distância dos chumbadores à interface de tensão (x): {converter.in_to_mm(x):.2f} mm')

    verif_1 = (f + (n_ch / 2))**2
    verif_2 = (2 * pu * (e + f))/q_max

    if verif_1 < verif_2:  # ENQUANTO VERIF_1 MENOR QUE VERIF_2 AUMENTAMOS DIMENSÕES DA CHAPA
        print(' (f+0.5N)^2 < 2Pu(e+f)/q_max')
        print('[italic] Não passou na verificação')
        print('[italic] Aumentar medidas da chapa ou resistência do concreto')
        raise ValueError()

    else:
        y1 = (f + (n_ch / 2)) + math.sqrt(((f + (n_ch / 2)) ** 2) - ((2 * pu * (e + f)) / q_max))
        y2 = (f + (n_ch / 2)) - math.sqrt(((f + (n_ch / 2)) ** 2) - ((2 * pu * (e + f)) / q_max))

        if y2 < 0:
            y = y1
            print(f' Comprimento da carga de compressão (Y): {converter.in_to_mm(y):.2f} mm')

        else:
            y = y2
            print(f' Comprimento da carga de compressão (Y): {converter.in_to_mm(y):.2f} mm')

        tu = q_max * y - pu
        print(f' Força de tração nos chumbadores (tu): {converter.kips_to_kn(tu):.2f} kN')

        m = (n_ch - (0.95 * d)) / 2
        print(f' Linha de flexão paralela à mesa do perfil (m): {converter.in_to_mm(m):.2f} mm')

        n = (b_ch - (0.8 * bf)) / 2
        print(f' Linha de flexão paralela à alma do perfil (n): {converter.in_to_mm(n):.2f} mm')

        if y >= m:
            tp_1 = 1.5 * m * math.sqrt(fp_max/fy)  # ESPESSURA PARA BALANÇO M - CONFORME EQUAÇÕES

        else:
            tp_1 = 2.11 * math.sqrt((fp_max * y * (m - (y / 2))) / fy)  # ESPESSURA PARA BALANÇO M - CONFORME EQUAÇÕES

        tp_3 = 1.5 * n * math.sqrt(fp_max / fy)

        if x >= 0 and tu >= 0:
            tp_2 = 2.11 * math.sqrt(tu * x / (b_ch * fy))  # ESPESSURA PARA BALANÇO A PARTIR DOS CHUMBADORES
        else:
            print('[italic] Não passou na verificação, chumbadores incorretamente posicionados')
            raise ValueError()

        tp_min = max(tp_1, tp_2, tp_3)  # ESPESSURA VAI SER A MAIOR ESPESSURA

        if tp < tp_min:
            print(f' tp {converter.in_to_mm(tp):.2f} mm < tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Não passou na verificação')
            raise ValueError()

        else:
            print(f' tp {converter.in_to_mm(tp):.2f} mm \u2265 tp min {converter.in_to_mm(tp_min):.2f} mm')
            print('[italic] Verificação da espessura - ok')
            return tu


def comprimento_ancoragem(diam, area, fck, nt_sd, fyb, fub, hef):
    diam = diam * 25.4  # Diâmetro para mm
    area = area * 6.4516  # Área para cm²
    nt_sd = nt_sd * 4.4482216152604995  # kips para kN
    fck = fck * 6.8947572931683595  # ksi para MPa
    fyb = fyb * 6.8947572931683595  # ksi para MPa
    fub = fub * 6.8947572931683595  # ksi para MPa
    hef = hef * 25.4  # in para mm

    print("\n[bold] Verificação da ancoragem dos chumbadores")
    print(f" Força axial solicitante (Nt,sd): {nt_sd:.2f} kN")
    nt_rd = (0.75 * area) * fub / (1.35 * 10)
    print(f" Força axial resistente (Nt,rd): {nt_rd:.2f} kN")
    n1 = 1  # Barras lisas
    print(" Parâmetro de rugosidade (\u03B71): 1")
    n2 = 1  # Boa aderência
    print(" Parâmetro de posição (\u03B72): 1")
    if diam < 32:  # mm
        n3 = 1
        print(" \u2300 < 32 mm")
        print(" Parâmetro de diâmetro (\u03B73): 1")

    else:
        print("\u2300 \u2265 32 mm")
        n3 = (132 - diam) / 100
        print(f" Parâmetro de diâmetro (\u03B73): {n3}")

    fctk_inf = 0.7 * 0.3 * (fck ** (2/3))
    print(f" Resistência à tração característica (fctk_inf): {fctk_inf:.2f} MPa")

    fctd = fctk_inf / 1.4
    print(f" Resistência à tração direta (fctd): {fctd:.2f} MPa")

    fbd = n1 * n2 * n3 * fctd
    print(f" Resistência de aderência do concreto (fbd): {fbd:.2f} MPa")

    fyd = fyb / 1.1
    print(f" Tensão de escoamento (fyd): {fyd:.2f} MPa")

    lb = max((diam / 4) * (fyd / fbd), 25 * diam)
    lb = math.ceil(lb)
    print(f" Comprimento de ancoragem básico (lb): {lb:.2f} mm")

    lb_min = max(0.3 * lb, 10 * diam, 100)
    lb_min = math.ceil(lb_min)
    print(f" Comprimento de ancoragem mínimo (lb_min): {lb_min:.2f} mm")

    lb_nec = max(0.7 * lb * (nt_sd / nt_rd), lb_min)
    lb_nec = math.ceil(lb_nec)
    print(f" Comprimento de ancoragem necessário (lb_nec): {lb_nec:.2f} mm")

    if hef >= lb_nec:
        print(f"[italic] Verificação do comprimento de ancoragem ok")
        return None

    else:
        print("[italic] Ancoragem menor do que a necessária")
        raise ValueError()
