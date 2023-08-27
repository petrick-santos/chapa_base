# Para imperial


def kn_to_kips(kn):
    kips = kn / 4.4482216152604995
    return kips


def knm_to_kips_in(knm):
    kips_in = knm * 8.850745791327184
    return kips_in


def mpa_to_ksi(mpa):
    ksi = mpa / 6.8947572931683595
    return ksi


def mm_to_in(mm):
    inch = mm / 25.4
    return inch


def cm2_to_in2(cm2):
    in2 = cm2 / 6.4516
    return in2


def kn_por_m_to_kips_por_in(kn_por_m):
    kips_por_in = kn_por_m / 175.12683524647633
    return kips_por_in

# Para internacional


def kips_to_kn(kips):
    kn = kips * 4.4482216152604995
    return kn


def kips_in_to_knm(kips_in):
    knm = kips_in / 8.850745791327184
    return knm

def kips_in_to_knmm(kips_in):
    knmm = 1000 * kips_in / 8.850745791327184
    return knmm


def ksi_to_mpa(ksi):
    mpa = ksi * 6.8947572931683595
    return mpa


def in_to_mm(inch):
    mm = inch * 25.4
    return mm


def in2_to_cm2(in2):
    cm2 = in2 * 6.4516
    return cm2


def kips_por_in_to_kn_por_m(kips_por_in):
    kn_por_m = kips_por_in * 175.12683524647633
    return kn_por_m


def kips_por_in_to_kn_por_mm(kips_por_in):
    kn_por_mm = kips_por_in * 175.12683524647633 / 1000
    return kn_por_mm


def dimensionamento_entrada(pu, vu, mu, fc, fy, d, bf, tw, tf):
    pu = kn_to_kips(pu)
    vu = kn_to_kips(vu)
    mu = knm_to_kips_in(mu)
    fc = mpa_to_ksi(fc)
    fy = mpa_to_ksi(fy)
    d = mm_to_in(d)
    bf = mm_to_in(bf)
    tw = mm_to_in(tw)
    tf = mm_to_in(tf)
    return pu, vu, mu, fc, fy, d, bf, tw, tf


def dimensionamento_saida(n_ch, b_ch, tp, dist_a1, dist_a2, a2, a1):
    n_ch = in_to_mm(n_ch)
    b_ch = in_to_mm(b_ch)
    tp = in_to_mm(tp)
    dist_a1 = in_to_mm(dist_a1)
    dist_a2 = in_to_mm(dist_a2)
    a2 = in2_to_cm2(a2)
    a1 = in2_to_cm2(a1)
    return n_ch, b_ch, tp, dist_a1, dist_a2, a2, a1


def verificacao_entrada(pu, vu, mu, d, bf, tw, tf, fc, fy, a2, n_ch, b_ch, tp, a1, dist_a1, dist_a2, hef):
    pu = kn_to_kips(pu)
    vu = kn_to_kips(vu)
    mu = knm_to_kips_in(mu)
    fc = mpa_to_ksi(fc)
    fy = mpa_to_ksi(fy)
    a2 = cm2_to_in2(a2)
    a1 = cm2_to_in2(a1)
    d = mm_to_in(d)
    bf = mm_to_in(bf)
    tw = mm_to_in(tw)
    tf = mm_to_in(tf)
    n_ch = mm_to_in(n_ch)
    b_ch = mm_to_in(b_ch)
    tp = mm_to_in(tp)
    dist_a1 = mm_to_in(dist_a1)
    dist_a2 = mm_to_in(dist_a2)
    hef = mm_to_in(hef)
    return pu, vu, mu, d, bf, tw, tf, fc, fy, a2, n_ch, b_ch, tp, a1, dist_a1, dist_a2, hef