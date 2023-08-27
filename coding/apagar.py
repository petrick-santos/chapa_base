import converter
import ch_dim

pu = 0
vu = 0
mu = 0
fc = 20
fy = 250


# w
d = 529
bf = 166
tw = 9.7
tf = 13.6

a2_a1 = 1
fyb = 36.2594344325524
gr = 58.0150950920838
n_chumb = 4
lig = "a"
x = 1
phi = 0.65
chumbador_a1 = 1.5748031496063
chumbador_a2 = 3.1496062992126

pu, vu, mu, fc, fy, d, bf, tw, tf = converter.dimensionamento_entrada(pu, vu, mu, fc, fy, d, bf, tw, tf)

for i in range(501):

    n_ch, b_ch, a1, a2, pp, tp, m, n, x, lmbd, lmbd_n, l, chumb_a1, chumb_a2 = ch_dim.compressao(pu, fc, fy, d, bf, tw, tf, phi, a2_a1, chumbador_a1, chumbador_a2, n_chumb, lig)
    pu_kn = converter.kips_to_kn(pu)
    tp_mm = converter.in_to_mm(tp)
    n_ch_mm = converter.in_to_mm(n_ch)
    b_ch_mm = converter.in_to_mm(b_ch)
    #print(f'{pu_kn:.2f} {tp_mm:.2f} {n_ch_mm:.2f} {b_ch_mm:.2f}')
    print(f'{pu_kn:.2f} {tp_mm:.2f}')
    pu = pu + (1 / 4.4482216152604995)
