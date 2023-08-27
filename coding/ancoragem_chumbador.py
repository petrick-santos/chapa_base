def comprimento_ancoragem(diam, area, fck, nt_sd, fyb, fub):
    # Diametro (mm)
    # Área (cm²)
    # Fck, Fyb, Fub (MPa)
    # Nt_sd (kN)
    nt_rd = (0.75 * area) * fub / (1.35 * 10)
    print(f"Nt,rd é {nt_rd:.2f} kN")
    n1 = 1  # Barras lisas
    print("n1 = 1")
    n2 = 1  # Boa aderência
    print("n2 = 1")
    if diam < 32:  # mm
        n3 = 1
        print("\u2300 < 32 mm")
        print("n3 = 1")

    else:
        print("\u2300 \u2265 32 mm")
        n3 = (132 - diam) / 100
        print(f"n3 = {n3}")

    fctk_inf = 0.7 * 0.3 * (fck ** (2/3))
    print(f"fctk_inf = {fctk_inf:.2f} MPa")

    fctd = fctk_inf / 1.4
    print(f"fctd = {fctd:.2f} MPa")

    fbd = n1 * n2 * n3 * fctd
    print(f"fbd = {fbd:.2f} MPa")

    fyd = fyb / 1.1
    print(f"fyd = {fyd:.2f} MPa")

    lb = max((diam / 4) * (fyd / fbd), 25 * diam)
    print(f"lb = {lb:.2f} mm")

    lb_min = max(0.3 * lb, 10 * diam, 100)
    print(f"lb_min = {lb_min:.2f} mm")

    lb_nec = max(0.7 * lb * (nt_sd / nt_rd), lb_min)
    print(f"lb_nec = {lb_nec:.2f} mm")

    return lb_nec
