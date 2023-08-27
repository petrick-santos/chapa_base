import math
import sys

sys.setrecursionlimit(100000)


def compressao(pu, fc, fy, d, bf, tw, tf, phi, a2_a1, a1_chumb, a2_chumb, n_chumb, lig):  # corrigir, agora a ligação é rotulada se o check na interface esticar clicado
    if lig == "r":
        n_ch = (d + (2 * a1_chumb))
        if (d - (2 * tf)) < max(((2 * a1_chumb) + a2_chumb), ((4 * a1_chumb) + tw)):
            raise ValueError()
        else:
            a2_chumb = max(a2_chumb, tw + (2 * a1_chumb))
            b_ch = max((bf + (2 * a1_chumb)), ((2 * a1_chumb) + a2_chumb))
            a1_chumb = (n_ch - a2_chumb) / 2
            a1 = b_ch * n_ch
            a2 = a1 * a2_a1
    else:
        n_ch = d + (4 * a1_chumb)
        b_ch = max((bf + (2 * a1_chumb)), ((((n_chumb / 2) - 1) * a2_chumb) + (2 * a1_chumb)))

        a1 = b_ch * n_ch
        a2 = a1 * a2_a1

    pp = phi * 0.85 * fc * a1 * math.sqrt(a2_a1)  # SE A ÁREA DE CHAPA CALCULADA FOR MENOR QUE NECESSARIA, PP VAI RESULTAR EM UM VALOR MENOR QUE PU /// OU SEJA RESISTENCIA MENOR QUE SOLICITAÇÃO
    ratio = (0.95 * d) - (0.8 * bf)  # RELAÇÃO ALTURA E LARGURA DAS LINHAS DE FLEXÃO DO PERFIL

    while pp < pu:
        if (n_ch - b_ch) > ratio:
            b_ch = b_ch + 0.0393700787401575
        elif (n_ch - b_ch) < ratio:
            n_ch = n_ch + 0.0393700787401575
        else:
            n_ch = n_ch + 0.0393700787401575
            b_ch = n_ch - ratio
        a1 = n_ch * b_ch
        a2 = a1 * a2_a1
        pp = phi * 0.85 * fc * a1 * math.sqrt(a2_a1)  # PP COM A ÁREA NOVA, ATÉ SAIR DO WHILE
    m = (n_ch - (0.95 * d)) / 2  # COMPRIMENTO M DO BALANÇO DA CHAPA
    n = (b_ch - (0.8 * bf)) / 2  # COMPRIMENTO N DO BALANÇO DA CHAPA
    x = ((4 * d * bf) / ((d + bf) ** 2)) * (pu / pp)  # PARAMETRO X
    lmbd = min((2 * math.sqrt(x) / (1 + math.sqrt(1 - x))), 1)  # PARAMETRO LAMBDA
    lmbd_n = lmbd * (math.sqrt(d * bf) / 4)  # PARAMETRO LAMBDA N
    l = max(m, n, lmbd_n)  # BALANÇO CRITICO DA CHAPA
    tp = l * math.sqrt((2 * pu) / (0.90 * fy * b_ch * n_ch))

    if lig == "r":
        a1_chumb = (n_ch - a2_chumb) / 2  # a1 vai mudar conforme chapa aumenta

    else:
        a2_chumb = (b_ch - (2 * a1_chumb)) / ((n_chumb / 2) - 1)  # a2 vai mudar conforme chapa aumenta

    return n_ch, b_ch, a1, a2, pp, tp, m, n, x, lmbd, lmbd_n, l, a1_chumb, a2_chumb


def cortante(tu, vu, tra_rod, v_chumb, ar_chumb, gr):
    fv = 1.25 * vu / (v_chumb * ar_chumb)  # CONSIDERANDO APENAS 2 CHUMBADORES PEGANDO O CISALHAMENTO
    fta = tu / (tra_rod * ar_chumb)
    ft = fta
    fnt = 0.75 * 0.75 * gr
    fnt2 = 0.75 * gr
    fnv = 0.45 * gr
    fnt_lin = min(0.75 * (1.3 * fnt2 - (fnt2 * fv / (0.75 * fnv))), fnt)

    if fnt_lin <= 0:
        fnt_lin = 0

    return fv, fnv, ft, fnt_lin, fta, fnt, fnt2


def excentricidade(pu, mu, fc, fy, phi, d, bf, tw, tf, a2_a1, a1_chumb, a2_chumb, n_ch, b_ch, ratio, e, e_crit):
    if e < e_crit:
        y = n_ch - (2 * e)
        pp = phi * 0.85 * fc * b_ch * y * math.sqrt(a2_a1)

        if pp < pu:
            if (n_ch - b_ch) > ratio:
                b_ch = b_ch + 0.0393700787401575
            elif (n_ch - b_ch) < ratio:
                n_ch = n_ch + 0.0393700787401575
            else:
                n_ch = n_ch + 0.0393700787401575
                b_ch = n_ch - ratio

            e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
            y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf, tw,
                                                                                       tf, a2_a1, a1_chumb, a2_chumb,
                                                                                       n_ch, b_ch, ratio, e, e_crit)
            return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f
        else:
            fp_max = phi * 0.85 * fc * math.sqrt(a2_a1)
            q_max = fp_max * b_ch
            fp = pu / (b_ch * y)
            q = pu / y

            if q > q_max:
                if (n_ch - b_ch) > ratio:
                    b_ch = b_ch + 0.0393700787401575
                elif (n_ch - b_ch) < ratio:
                    n_ch = n_ch + 0.0393700787401575
                else:
                    n_ch = n_ch + 0.0393700787401575
                    b_ch = n_ch - ratio

                e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
                y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf,
                                                                                           tw, tf, a2_a1, a1_chumb,
                                                                                           a2_chumb, n_ch, b_ch,
                                                                                           ratio, e, e_crit)
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f
            else:
                tu = 0
                x = (n_ch / 2) - (d / 2) - a1_chumb + (tf / 2)
                f = (n_ch / 2) - a1_chumb
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f

    elif e == e_crit:
        y = pu / (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch)
        pp = phi * 0.85 * fc * b_ch * y * math.sqrt(a2_a1)

        if pp < pu:
            if (n_ch - b_ch) > ratio:
                b_ch = b_ch + 0.0393700787401575
            elif (n_ch - b_ch) < ratio:
                n_ch = n_ch + 0.0393700787401575
            else:
                n_ch = n_ch + 0.0393700787401575
                b_ch = n_ch - ratio

            e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
            y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf, tw,
                                                                                       tf, a2_a1, a1_chumb, a2_chumb,
                                                                                       n_ch, b_ch, ratio, e, e_crit)
            return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f

        else:
            fp_max = phi * 0.85 * fc * math.sqrt(a2_a1)
            q_max = fp_max * b_ch
            fp = pu / (b_ch * y)
            q = pu / y

            if q > q_max:
                if (n_ch - b_ch) > ratio:
                    b_ch = b_ch + 0.0393700787401575
                elif (n_ch - b_ch) < ratio:
                    n_ch = n_ch + 0.0393700787401575
                else:
                    n_ch = n_ch + 0.0393700787401575
                    b_ch = n_ch - ratio

                e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
                y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf,
                                                                                           tw, tf, a2_a1, a1_chumb,
                                                                                           a2_chumb, n_ch, b_ch, ratio,
                                                                                           e, e_crit)
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f
            else:
                tu = 0
                x = (n_ch / 2) - (d / 2) - a1_chumb + (tf / 2)
                f = (n_ch / 2) - a1_chumb
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f

    else:
        f = (n_ch / 2) - a1_chumb
        q_max = phi * 0.85 * fc * b_ch * math.sqrt(a2_a1)
        ver_1 = (f + (n_ch / 2)) ** 2
        ver_2 = (2 * pu * (e + f)) / q_max

        if ver_1 < ver_2:
            if (n_ch - b_ch) > ratio:
                b_ch = b_ch + 0.0393700787401575
            elif (n_ch - b_ch) < ratio:
                n_ch = n_ch + 0.0393700787401575
            else:
                n_ch = n_ch + 0.0393700787401575
                b_ch = n_ch - ratio

            e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
            y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf, tw,
                                                                                       tf, a2_a1, a1_chumb, a2_chumb,
                                                                                       n_ch, b_ch, ratio, e, e_crit)
            return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f
        else:
            y1 = (f + (n_ch / 2)) + math.sqrt(((f + (n_ch / 2)) ** 2) - ((2 * pu * (e + f)) / q_max))
            y2 = (f + (n_ch / 2)) - math.sqrt(((f + (n_ch / 2)) ** 2) - ((2 * pu * (e + f)) / q_max))
            if y2 < 0:
                y = y1
            else:
                y = y2
            pp = phi * 0.85 * fc * b_ch * y * math.sqrt(a2_a1)

            if pp < pu:
                if (n_ch - b_ch) > ratio:
                    b_ch = b_ch + 0.0393700787401575
                elif (n_ch - b_ch) < ratio:
                    n_ch = n_ch + 0.0393700787401575
                else:
                    n_ch = n_ch + 0.0393700787401575
                    b_ch = n_ch - ratio

                e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)
                y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf,
                                                                                           tw, tf, a2_a1, a1_chumb,
                                                                                           a2_chumb, n_ch, b_ch, ratio,
                                                                                           e, e_crit)
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f
            else:
                fp_max = phi * 0.85 * fc * math.sqrt(a2_a1)
                q_max = fp_max * b_ch
                fp = fp_max
                q = q_max
                tu = (q_max * y) - pu
                x = (n_ch / 2) - (d / 2) - a1_chumb + (tf / 2)
                return y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f


def momentos(pu, mu, fc, fy, phi, d, bf, tw, tf, a2_a1, a1_chumb, a2_chumb, n_chumb):
    n_ch = d + (4 * a1_chumb)
    b_ch = max((bf + (2 * a1_chumb)), (a1_chumb + (((n_chumb / 2) - 1) * a2_chumb) + a1_chumb))
    ratio = (0.95 * d) - (0.8 * bf)

    e = round(mu / pu, 4)
    e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)

    while e_crit < 0:
        if (n_ch - b_ch) > ratio:
            b_ch = b_ch + 0.0393700787401575
        elif (n_ch - b_ch) < ratio:
            n_ch = n_ch + 0.0393700787401575
        else:
            n_ch = n_ch + 0.0393700787401575
            b_ch = n_ch - ratio
        e_crit = round((n_ch / 2) - (pu / (2 * (phi * 0.85 * fc * math.sqrt(a2_a1) * b_ch))), 4)

    y, pp, n_ch, b_ch, e_crit, fp_max, q_max, fp, q, tu, x, f = excentricidade(pu, mu, fc, fy, phi, d, bf, tw, tf,
                                                                               a2_a1, a1_chumb, a2_chumb, n_ch, b_ch,
                                                                               ratio, e, e_crit)

    m = (n_ch - (0.95 * d)) / 2
    n = (b_ch - (0.80 * bf)) / 2

    if y >= m:
        tp_m = 1.5 * m * math.sqrt(fp / fy)
    else:
        tp_m = 2.11 * math.sqrt((fp * y * (m - (y / 2))) / fy)

    tp_x = 2.11 * math.sqrt(tu * x / (b_ch * fy))
    tp_n = 1.5 * n * math.sqrt(fp / fy)
    tp = max(tp_m, tp_n, tp_x)

    a1 = n_ch * b_ch
    a2 = a1 * a2_a1

    return n_ch, b_ch, tp, tu, x, a1, a2, e, fp_max, q_max, e_crit, y, q, fp, m, n, f


def tracao(pu, d, bf, tw, tf, fy, gr, a1_chumb, a2_chumb, chumb_area, n_chumb, lig):  # CHAPAS SUBMETIDAS A TRAÇÃO
    rn = 0.75 * 0.75 * gr * chumb_area
    ru = pu / n_chumb  # VALOR DA TRAÇÃO EM CADA CHUMBADOR

    if rn >= ru:
        if lig == "r":
            n_ch = (d + (2 * a1_chumb))
            if (d - (2 * tf)) < max(((2 * a1_chumb) + a2_chumb), ((4 * a1_chumb) + tw)):
                raise ValueError()

            else:
                a2_chumb = max(a2_chumb, tw + (2 * a1_chumb))
                b_ch = max((bf + (2 * a1_chumb)), ((2 * a1_chumb) + a2_chumb))

            moment_w = ru * (a2_chumb - tw)  # MOMENTO GERADO NA CHAPA PELA FORÇA DE TRAÇÃO
            b_eff = (2 * (a2_chumb - tw))

            tp = math.sqrt((moment_w * 4) / (b_eff * 0.90 * fy))  # ESPESSURA DA CHAPA

            chumb_a1 = (n_ch - a2_chumb) / 2
            chumb_a2 = a2_chumb

            return n_ch, b_ch, tp, ru, rn, 0, moment_w, b_eff, chumb_a1, chumb_a2

        else:
            n_ch = d + (4 * a1_chumb)
            b_ch = max((bf + (2 * a1_chumb)), ((((n_chumb / 2) - 1) * a2_chumb) + (2 * a1_chumb)))
            tu = pu / (n_chumb / 2)
            x = (n_ch / 2) - (d / 2) - a1_chumb + (tf / 2)
            mpl = (tu * x) / b_ch
            tp = 2.11 * math.sqrt((tu * x) / (b_ch * fy))

            chumb_a1 = a1_chumb
            chumb_a2 = (b_ch - (2 * chumb_a1)) / ((n_chumb / 2) - 1)

            return n_ch, b_ch, tp, ru, rn, mpl, 0, 0, chumb_a1, chumb_a2

    else:
        return None


def comprimento_ancoragem(diam, area, fck, nt_sd, fyb, fub):
    diam = diam * 25.4  # Diâmetro para mm
    area = area * 6.4516  # Área para cm²
    nt_sd = nt_sd * 4.4482216152604995  # kips para kN
    fck = fck * 6.8947572931683595  # ksi para MPa
    fyb = fyb * 6.8947572931683595  # ksi para MPa
    fub = fub * 6.8947572931683595  # ksi para MPa

    print("\n[bold] Comprimento de ancoragem dos chumbadores: "
          "")
    print(f" Força axial solicitante (Nt,sd): {nt_sd:.2F} kN")
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

    fctk_inf = 0.7 * 0.3 * (fck ** (2 / 3))
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

    return lb_nec
