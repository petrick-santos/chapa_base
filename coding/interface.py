import tkinter as tk
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk
import sys
import os
import converter
import gerdau_w
import chumbadores
import inf_inicial
import processo
import limite_ultimo
from tkinter import messagebox

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.configure(state="normal")

        if "[bold]" in text:
            text = text.replace("[bold]", "")
            self.widget.insert("end", text, "bold")
        elif "[italic]" in text:
            text = text.replace("[italic]", "")
            self.widget.insert("end", text, "italic")
        else:
            self.widget.insert("end", text)

        self.widget.configure(state="disabled")

    def flush(self):
        pass


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def click_limpar(widget_text):
    widget_text.configure(state='normal')
    widget_text.delete("1.0", tk.END)
    widget_text.configure(state='disabled')

    var_chapa_n2.set("")
    var_chapa_b2.set("")
    var_chapa_tp2.set("")
    var_concreto_a2_2.set("")
    var_area_chapa.set("")
    var_chumb_a1_2.set("")
    var_chumb_a2_2.set("")
    var_chumb_diametro.set("")
    var_status.set("")


def click_salvar(widget_text):
    conteudo = widget_text.get('1.0', tk.END)
    with open('chapa_base.txt', 'w', encoding="utf-8") as f:
        f.write(conteudo)


def selecionar_familia(*args):
    valores_perfis = gerdau_w.dic_familias[variavel_familia.get()]
    nomes_perfis = [perfil.nome for perfil in valores_perfis]
    cmb_perfil_nome.configure(values=nomes_perfis)
    variavel_perfil.set("")


def informacoes_perfil(*args):
    global nome, d, bf, tw, tf, ag, zx
    nome_perfil_selecionado = variavel_perfil.get()
    grupo_perfil_selecionado = variavel_familia.get()
    lista_de_perfis_da_familia = gerdau_w.dic_familias[grupo_perfil_selecionado]
    perfil = next((p for p in lista_de_perfis_da_familia if p.nome == nome_perfil_selecionado))
    nome = perfil.nome
    d = perfil.d
    bf = perfil.bf
    tw = perfil.tw
    tf = perfil.tf
    ag = perfil.ag
    zx = perfil.zx
    var_perfil_d.set(d)
    var_perfil_bf.set(bf)
    var_perfil_tw.set(tw)
    var_perfil_tf.set(tf)
    var_perfil_ag.set(ag)
    var_perfil_zx.set(zx)


def cancelar():
    window.destroy()


def cancelar_inicial():
    janela_inicializacao.grab_release()
    janela_inicializacao.destroy()


def recusar_sair():
    janela_inicializacao.destroy()
    window.destroy()


def botao_sobre():
    janela_sobre = tk.Toplevel()
    janela_sobre.title("Sobre")
    janela_sobre.grab_set()

    largura_tela = janela_sobre.winfo_screenwidth()
    altura_tela = janela_sobre.winfo_screenheight()

    largura_janela = 560
    altura_janela = 560

    pos_x = int((largura_tela / 2) - (largura_janela / 2))
    pos_y = int((altura_tela / 2) - (altura_janela / 2))

    # Tamanho da janela
    janela_sobre.geometry("{}x{}+{}+{}".format(largura_janela, altura_janela, pos_x, pos_y))
    janela_sobre.resizable(False, False)

    caminho_icone = resource_path('icone.ico')
    janela_sobre.iconbitmap(caminho_icone)

    frame_geral = ttk.Frame(janela_sobre)
    frame_geral.grid(row=0, column=0, sticky="news")

    frame_imagens_sobre = ttk.Frame(frame_geral)
    frame_imagens_sobre.grid(row=0, column=0, pady=(25, 15), sticky="news")

    ########
    lbl_imagem_ee_sobre = ttk.Label(frame_imagens_sobre, image=img_ee)
    lbl_imagem_ee_sobre.grid(row=0, column=0, padx=(120, 50), pady=5)

    lbl_imagem_ufrgs_sobre = ttk.Label(frame_imagens_sobre, image=img_ufrgs)
    lbl_imagem_ufrgs_sobre.grid(row=0, column=1, padx=5, pady=5)
    ########

    frame_texto_sobre = ttk.Frame(frame_geral)
    frame_texto_sobre.grid(row=1, column=0, pady=5, sticky="news")

    texto006 = tk.Text(frame_texto_sobre, wrap="word", height=20, width=77, borderwidth=0, bg=bg_ini_color)
    texto006.grid(row=0, column=0, padx=5, pady=5, sticky="news")

    mensagem_inicial = """\
    Esse software é uma ferramenta desenvolvida como parte do Trabalho de Conclusão
    do Curso de Engenharia Civil da Universidade Federal do Rio Grande do Sul, do
    aluno Petrick Eichwald Rosa dos Santos. O projeto foi realizado sob a orientação
    do professor Enio Carlos Mesacasa Júnior, que atuou como orientador durante todo
    o desenvolvimento do software.
    
    O objetivo deste programa é auxiliar no cálculo das principais dimensões de ligações
    de chapas de base de pilares metálicos, proporcionando uma solução prática para
    estudantes, engenheiros e profissionais da área.
    
    Os resultados fornecidos pelo software são baseados nas informações inseridas pelo
    usuário, e os desenvolvedores não se responsabilizam por quaisquer consequências 
    resultantes do uso das informações ou resultados gerados por este programa. O
    usuário é inteiramente responsável por verificar e validar os cálculos realizados
    pelo software, bem como por considerar todas as normas e regulamentos vigentes.
    
    Versão 1.0 - Agosto, 2023
    
    Versões mais recentes podem estar disponíveis na plataforma GitHub
    Link: https://github.com/petrick-santos/chapa_base"""

    texto006.insert("1.0", mensagem_inicial)
    texto006.config(font=('Segoe UI', 10), state="disabled")


def dimensionar():
    btn_principal.config(text="Dimensionar", command=click_dimensionar)

    lbl_chapa_n.configure(state="disabled")
    ety_chapa_n.configure(state="disabled")
    lbl_chapa_n_unid.configure(state="disabled")

    lbl_chapa_b.configure(state="disabled")
    ety_chapa_b.configure(state="disabled")
    lbl_chapa_b_unid.configure(state="disabled")

    lbl_chapa_tp.configure(state="disabled")
    ety_chapa_tp.configure(state="disabled")
    lbl_chapa_tp_unid.configure(state="disabled")

    lbl_chumbadores_diametro.configure(state="disabled")
    cmb_chumbadores_diametro.configure(state="disabled")

    lbl_chumbadores_embutimento.configure(state="disabled")
    ety_chumbadores_embutimento.configure(state="disabled")
    lbl_chumbadores_embutimento_unid.configure(state="disabled")

    lbl_chumbadores_a1.configure(state="disabled")
    ety_chumbadores_a1.configure(state="disabled")
    lbl_chumbadores_a1_unid.configure(state="disabled")

    lbl_chumbadores_a2.configure(state="disabled")
    ety_chumbadores_a2.configure(state="disabled")
    lbl_chumbadores_a2_unid.configure(state="disabled")

    lbl_proporcao.configure(state="normal")
    scl_proporcao.configure(state="normal")
    lbl_variavel_proporcao.configure(state="normal")

    lbl_area_concreto.config(state="disabled")
    ety_area_concreto.config(state="disabled")
    lbl_area_concreto_unid.config(state="disabled")

    var_chapa_n.set("")
    var_chapa_b.set("")
    var_chapa_tp.set("")
    var_concreto_a2.set("")
    var_chumb_a1.set("")
    var_chumb_a2.set("")
    cmb_chumbadores_diametro.set("")
    var_hef_chumb.set("")


def verificar():
    btn_principal.config(text="Verificar", command=click_verificar)

    lbl_proporcao.config(state="disabled")
    scl_proporcao.config(state="disabled")
    lbl_variavel_proporcao.config(state="disabled")

    lbl_area_concreto.config(state="normal")
    ety_area_concreto.config(state="normal")
    lbl_area_concreto_unid.config(state="normal")

    lbl_chapa_n.configure(state="normal")
    ety_chapa_n.configure(state="normal")
    lbl_chapa_n_unid.configure(state="normal")

    lbl_chapa_b.configure(state="normal")
    ety_chapa_b.configure(state="normal")
    lbl_chapa_b_unid.configure(state="normal")

    lbl_chapa_tp.configure(state="normal")
    ety_chapa_tp.configure(state="normal")
    lbl_chapa_tp_unid.configure(state="normal")

    lbl_chumbadores_diametro.configure(state="normal")
    cmb_chumbadores_diametro.configure(state="readonly")

    lbl_chumbadores_embutimento.configure(state="normal")
    ety_chumbadores_embutimento.configure(state="normal")
    lbl_chumbadores_embutimento_unid.configure(state="normal")

    lbl_chumbadores_a1.configure(state="normal")
    ety_chumbadores_a1.configure(state="normal")
    lbl_chumbadores_a1_unid.configure(state="normal")

    lbl_chumbadores_a2.configure(state="normal")
    ety_chumbadores_a2.configure(state="normal")
    lbl_chumbadores_a2_unid.configure(state="normal")

    var_chapa_n.set("")
    var_chapa_b.set("")
    var_chapa_tp.set("")
    var_concreto_a2.set("")
    var_chumb_a1.set("")
    var_chumb_a2.set("")
    cmb_chumbadores_diametro.set("")
    var_hef_chumb.set("")


def tabelado():
    lbl_perfil_d.configure(state="disabled")
    lbl_perfil_bf.configure(state="disabled")
    lbl_perfil_tw.configure(state="disabled")
    lbl_perfil_tf.configure(state="disabled")

    ety_perfil_d.configure(state="disabled")
    ety_perfil_bf.configure(state="disabled")
    ety_perfil_tw.configure(state="disabled")
    ety_perfil_tf.configure(state="disabled")

    lbl_perfil_d_unid.configure(state="disabled")
    lbl_perfil_bf_unid.configure(state="disabled")
    lbl_perfil_tw_unid.configure(state="disabled")
    lbl_perfil_tf_unid.configure(state="disabled")


    lbl_perfil_familia.configure(state="normal")
    lbl_perfil_nome.configure(state="normal")
    cmb_perfil_familia.configure(state="readonly")
    cmb_perfil_nome.configure(state="readonly")

    var_perfil_d.set("")
    var_perfil_bf.set("")
    var_perfil_tw.set("")
    var_perfil_tf.set("")
    var_perfil_ag.set("")
    var_perfil_zx.set("")


def usuario():
    global nome
    nome = "Perfil do usuário"
    lbl_perfil_familia.configure(state="disabled")
    lbl_perfil_nome.configure(state="disabled")
    cmb_perfil_familia.configure(state="disabled")
    cmb_perfil_nome.configure(state="disabled")

    lbl_perfil_d.configure(state="normal")
    lbl_perfil_bf.configure(state="normal")
    lbl_perfil_tw.configure(state="normal")
    lbl_perfil_tf.configure(state="normal")

    ety_perfil_d.configure(state="normal")
    ety_perfil_bf.configure(state="normal")
    ety_perfil_tw.configure(state="normal")
    ety_perfil_tf.configure(state="normal")

    lbl_perfil_d_unid.configure(state="normal")
    lbl_perfil_bf_unid.configure(state="normal")
    lbl_perfil_tw_unid.configure(state="normal")
    lbl_perfil_tf_unid.configure(state="normal")

    cmb_perfil_nome.configure(values=[])

    variavel_familia.set("")
    variavel_perfil.set("")

    var_perfil_d.set("")
    var_perfil_bf.set("")
    var_perfil_tw.set("")
    var_perfil_tf.set("")
    var_perfil_ag.set("")
    var_perfil_zx.set("")


def engastado():
    cmb_quantidade_chumbador.configure(values=["4", "6", "8", "10"])
    cmb_quantidade_chumbador.set("4")
    cmb_quantidade_chumbador.configure(state="readonly")
    lbl_imagem_principal.configure(image=img_1)
    var_mu.set("")
    lbl_mu.configure(state="normal")
    ety_mu.configure(state="normal")
    lbl_mu_unidades.configure(state="normal")


def rotulado():
    cmb_quantidade_chumbador.configure(values=["4"])
    cmb_quantidade_chumbador.set("4")
    lbl_quantidade_chumbador.configure(state="disabled")
    cmb_quantidade_chumbador.configure(state="disabled")
    lbl_imagem_principal.configure(image=img_2)
    var_mu.set("0")
    lbl_mu.configure(state="disabled")
    ety_mu.configure(state="disabled")
    lbl_mu_unidades.configure(state="disabled")


def numero_chumbadores(*args):
    n_chumb = float(var_numero_chumbadores.get())

    if n_chumb == 4:
        lbl_imagem_principal.configure(image=img_1)
    elif n_chumb == 6:
        lbl_imagem_principal.configure(image=img_3)
    elif n_chumb == 8:
        lbl_imagem_principal.configure(image=img_4)
    else:
        lbl_imagem_principal.configure(image=img_5)


def material_help():
    janela_material = tk.Toplevel()
    janela_material.title("Resistência dos chumbadores")

    largura_tela = janela_material.winfo_screenwidth()
    altura_tela = janela_material.winfo_screenheight()

    largura_janela = 480
    altura_janela = 180

    pos_x = int((largura_tela / 2) - (largura_janela / 2))
    pos_y = int((altura_tela / 2) - (altura_janela / 2))

    # Tamanho da janela
    janela_material.geometry("{}x{}+{}+{}".format(largura_janela, altura_janela, pos_x, pos_y))
    janela_material.resizable(False, False)

    caminho_icone = resource_path('icone.ico')
    janela_material.iconbitmap(caminho_icone)

    frame_material = ttk.Frame(janela_material)
    frame_material.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="news")

    imagem_material = ttk.Label(frame_material, image=img_6)
    imagem_material.grid(row=0, column=0, padx=12, pady=5, sticky="news")


def click_dimensionar():
    global pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, zx, fyb, gr, a2_a1, n_chumb, lig, hef

    click_limpar(txt_saida)
    var_chapa_n.set("")
    var_chapa_b.set("")
    var_chapa_tp.set("")
    var_concreto_a2.set("")
    var_chumb_a1.set("")
    var_chumb_a2.set("")
    cmb_chumbadores_diametro.set("")
    var_hef_chumb.set("")

    try:
        pu = float(ety_pu.get())
        vu = abs(float(ety_vu.get()))
        mu = abs(float(ety_mu.get()))
        fc = float(ety_fck.get())
        fy = float(ety_fy.get())
        a2_a1 = variavel_proporcao.get()
        fyk = float(ety_perfil_fyk.get())

    except ValueError:
        var_status.set("Não dimensionado: preencher todos os campos corretamente")
        return None

    if pu < 0 and mu != 0:
        var_status.set("Não dimensionado: solicitações não abrangidas")
        return None

    try:
        d = float(ety_perfil_d.get())
        bf = float(ety_perfil_bf.get())
        tw = float(ety_perfil_tw.get())
        tf = float(ety_perfil_tf.get())
    except ValueError:
        var_status.set("Não dimensionado: perfil não identificado")
        return None

    if nome == "Perfil do usuário":
        try:
            ag = ((2 * bf * tf) + ((d - (2 * tf)) * tw)) / 100
            var_perfil_ag.set(f"{ag:.1f}")

            zx = ((bf * d * d / 4) - ((bf - tw) * (d - (2 * tf)) * (d - (2 * tf)) / 4)) / 1000
            var_perfil_zx.set(zx)

        except ValueError:
            var_status.set("Não dimensionado: verificar dimensões do perfil")
            return None
    else:
        try:
            ag = float(var_perfil_ag.get())
            zx = float(var_perfil_zx.get())
        except ValueError:
            var_status.set("Não dimensionado: verificar dimensões do perfil")
            return None

    if pu == 0 and mu != 0:
        var_status.set("Não dimensionado: verificar solicitações")
        return None

    if d <= 0 or bf <= 0 or tw <= 0 or tf <= 0:
        var_status.set("Não dimensionado: verificar dimensões do perfil")
        return None

    if tf > (d / 2):
        var_status.set("Não dimensionado: verificar dimensões do perfil")
        return None

    if tw > bf:
        var_status.set("Não dimensionado: verificar dimensões do perfil")
        return None

    if fyk <= 0:
        var_status.set("Não dimensionado: verificar tensão de escoamento do perfil")
        return None

    if fc <= 0:
        var_status.set("Não dimensionado: verificar a resistência da base de concreto")
        return None

    if fy <= 0:
        var_status.set("Não dimensionado: verificar a resistência da chapa de base")
        return None

    try:
        grade_nome = cmb_material_chumbador.get()
        gr = float(chumbadores.dic_materiais[cmb_material_chumbador.get()][1])
        fyb = float(chumbadores.dic_materiais[cmb_material_chumbador.get()][0])

    except KeyError:
        var_status.set("Não dimensionado: verificar material do chumbador")
        return None

    n_chumb = float(var_numero_chumbadores.get())
    lig = var_ch_ligacao.get()

    # Início dos cálculos
    #inf_inicial.entrada_dim(pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, a2_a1, grade_nome, n_chumb, lig)
    lim_rd = limite_ultimo.resistencia_calculo(pu, mu, ag, fyk, zx)
    pu, vu, mu, fc, fy, d, bf, tw, tf = converter.dimensionamento_entrada(pu, vu, mu, fc, fy, d, bf, tw, tf)

    try:
        n_ch, b_ch, tp, chumb_nome, dist_a1, dist_a2, a2, a1, hef = processo.dimensionamento(pu, vu, mu, fc, fy, d, bf,
                                                                                             tw, tf, a2_a1, fyb, gr,
                                                                                             0.65, n_chumb, lig)
    except TypeError:
        var_status.set("Não dimensionado")
        return None

    n_ch, b_ch, tp, dist_a1, dist_a2, a2, a1 = converter.dimensionamento_saida(n_ch, b_ch, tp, dist_a1, dist_a2, a2, a1)

    n_ch = round(float(n_ch), 2)
    b_ch = round(float(b_ch), 2)
    tp = round(float(tp), 2)
    dist_a1 = round(float(dist_a1), 2)
    dist_a2 = round(float(dist_a2), 2)
    a2 = round(float(a2), 0)
    a1 = round(float(a1), 0)
    hef = round(float(hef), 2)

    var_chapa_n.set(str(n_ch))
    var_chapa_n2.set(str(n_ch))

    var_chapa_b.set(str(b_ch))
    var_chapa_b2.set(str(b_ch))

    var_chapa_tp.set(str(tp))
    var_chapa_tp2.set(str(tp))

    var_concreto_a2.set(str(a2))
    var_concreto_a2_2.set(str(a2))

    var_area_chapa.set(str(a1))

    var_chumb_diametro.set(chumb_nome)

    var_chumb_a1.set(str(dist_a1))
    var_chumb_a1_2.set(str(dist_a1))

    var_chumb_a2.set(str(dist_a2))
    var_chumb_a2_2.set(str(dist_a2))

    var_hef_chumb.set(str(hef))

    if chumb_nome in list(chumbadores.lista_chumbadores.keys()):
        cmb_chumbadores_diametro.set(chumb_nome)

    if lim_rd > 1:
        var_status.set("Dimensionado com aviso")
    else:
        var_status.set("Dimensionado com sucesso")


def click_verificar():
    global pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, zx, fyb, gr, a2_a1, a2, n_ch, b_ch, tp, d_a1, d_a2,\
        chumb, n_chumb, lig, hef

    click_limpar(txt_saida)

    try:
        pu = float(ety_pu.get())
        vu = abs(float(ety_vu.get()))
        mu = abs(float(ety_mu.get()))
        fc = float(ety_fck.get())
        fy = float(ety_fy.get())
        # a2_a1 = variavel_proporcao.get()

        a2 = float(ety_area_concreto.get())
        n_ch = float(ety_chapa_n.get())
        b_ch = float(ety_chapa_b.get())
        tp = float(ety_chapa_tp.get())
        d_a1 = float(ety_chumbadores_a1.get())
        d_a2 = float(ety_chumbadores_a2.get())
        hef = float(ety_chumbadores_embutimento.get())

    except ValueError:
        var_status.set("Não verificado: preencher todos os campos corretamente")
        return None

    if pu < 0 and mu != 0:
        var_status.set("Não verificado: solicitações não abrangidas")
        return None

    try:
        chumb = chumbadores.lista_chumbadores[cmb_chumbadores_diametro.get()]
        chumb_nome = chumb.nome
        chumb_area = chumb.area
        chumb_diam = chumb.diametro

    except:
        var_status.set("Não verificado: preencher todos os campos corretamente")
        return None

    n_chumb = float(var_numero_chumbadores.get())
    lig = var_ch_ligacao.get()

    try:
        d = float(ety_perfil_d.get())
        bf = float(ety_perfil_bf.get())
        tw = float(ety_perfil_tw.get())
        tf = float(ety_perfil_tf.get())
    except ValueError:
        var_status.set("Não verificado: conferir dimensões do perfil")
        return None

    if nome == "Perfil do usuário":
        try:
            ag = ((2 * bf * tf) + ((d - (2 * tf)) * tw)) / 100
            var_perfil_ag.set(f"{ag:.1f}")

            zx = ((bf * d * d / 4) - ((bf - tw) * (d - (2 * tf)) * (d - (2 * tf)) / 4)) / 1000
            var_perfil_zx.set(zx)

        except ValueError:
            var_status.set("Não verificado: conferir dimensões do perfil")
            return None
    else:
        try:
            ag = float(var_perfil_ag.get())
            zx = float(var_perfil_zx.get())
        except ValueError:
            var_status.set("Não verificado: conferir dimensões do perfil")
            return None

    try:
        fyk = float(ety_perfil_fyk.get())
    except ValueError:
        var_status.set("Não verificado: conferir resistência do perfil")
        return None

    try:
        grade_nome = cmb_material_chumbador.get()
        gr = float(chumbadores.dic_materiais[cmb_material_chumbador.get()][1])
        fyb = float(chumbadores.dic_materiais[cmb_material_chumbador.get()][0])

    except KeyError:
        var_status.set("Não verificado: material do chumbador não identificado")
        return None

    if pu == 0 and mu != 0:
        var_status.set("Não verificado: solicitações não abrangidas")
        return None

    if n_ch < d:
        var_status.set("Não verificado: comprimento de chapa (N) menor que perfil (d)")
        return None

    if b_ch < bf:
        var_status.set("Não verificado: largura de chapa (B) menor que perfil (bf)")
        return None

    # dimensoes do perfil
    if d <= 0 or bf <= 0 or tw <= 0 or tf <= 0:
        var_status.set("Não verificado: dimensões do perfil inválidas")
        return None

    if tf > (d / 2):
        var_status.set("Não verificado: dimensões do perfil inválidas")
        return None

    if tw > bf:
        var_status.set("Não verificado: dimensões do perfil inválidas")
        return None

    # dimensoes do concreto
    if fc <= 0:
        var_status.set("Não verificado: propriedades da base de concreto inválidas")
        return None

    if a2 <= 0:
        var_status.set("Não verificado: dimensões da base de concreto inválidas")
        return None

    if n_ch <= 0 or b_ch <= 0 or tp <= 0:
        var_status.set("Não verificado: dimensões da chapa base inválidas")
        return None

    if fy <= 0:
        var_status.set("Não verificado: propriedades da chapa base inválidas")
        return None

    if d_a1 < 0 or d_a2 < 0:
        var_status.set("Não verificado: distâncias dos chumbadores inválidas")
        return None

    if d_a1 > (n_ch / 2):
        var_status.set("Não verificado: distâncias dos chumbadores inválidas")
        return None

    if mu != 0 and d_a1 > ((n_ch - d) / 2):
        var_status.set("Não verificado: posição dos chumbadores inválida")
        return None

    if d_a2 > b_ch:
        var_status.set("Não verificado: distâncias dos chumbadores inválidas")
        return None

    if (((n_chumb / 2) - 1) * d_a2) > b_ch:
        var_status.set("Não verificado: distâncias dos chumbadores inválidas")
        return None

    if fyk <= 0:
        var_status.set("Não verificado: tensão de escoamento do perfil inválida")
        return None

    if hef <= 0:
        var_status.set("Não verificado: Embutimento \u2264 0")
        return None

    a1 = (n_ch * b_ch) / 100  # cm²

    try:
        #inf_inicial.entrada_verif(pu, vu, mu, fc, fy, nome, d, bf, tw, tf, ag, fyk, a2, n_ch, b_ch, tp, grade_nome,
                                  #chumb_nome, d_a1, d_a2, a1, n_chumb, lig, hef)

        # FAZER AQUI A VERIFICAÇÃO DO PERFIL, POR QUE PRECISO DOS VALROES EM UNIDADES INTERNACIONAIS
        lim_rd = limite_ultimo.resistencia_calculo(pu, mu, ag, fyk, zx)

        pu, vu, mu, d, bf, tw, tf, fc, fy, a2, n_ch, b_ch, tp, a1, dist_a1, dist_a2, hef = converter.verificacao_entrada(pu, vu, mu, d, bf, tw, tf, fc, fy, a2, n_ch, b_ch, tp, a1, d_a1, d_a2, hef)


        processo.verificacao(pu, vu, mu, fc, fy, d, bf, tw, tf, a2, dist_a1, dist_a2, chumb_area, chumb_diam, fyb, gr,
                             0.65, a1, n_ch, b_ch, tp, n_chumb, lig, hef)

        n_ch = round(float(converter.in_to_mm(n_ch)), 2)
        b_ch = round(float(converter.in_to_mm(b_ch)), 2)
        tp = round(float(converter.in_to_mm(tp)), 2)
        dist_a1 = round(float(converter.in_to_mm(dist_a1)), 2)
        dist_a2 = round(float(converter.in_to_mm(dist_a2)), 2)
        a2 = round(float(converter.in2_to_cm2(a2)), 0)
        a1 = round(float(converter.in2_to_cm2(a1)), 0)

        var_chapa_n2.set(str(n_ch))
        var_chapa_b2.set(str(b_ch))
        var_chapa_tp2.set(str(tp))
        var_concreto_a2_2.set(str(a2))
        var_area_chapa.set(str(a1))
        var_chumb_diametro.set(chumb_nome)
        var_chumb_a1_2.set(str(dist_a1))
        var_chumb_a2_2.set(str(dist_a2))

    except ValueError:
        var_status.set("Não passou na verificação")
        return None

    if lim_rd > 1:
        var_status.set("Verificado com aviso")
    else:
        var_status.set("Verificado com sucesso")


# Configurações da janela principal
window = ThemedTk(theme="vista")
window.title("Chapa Base")

# Posição da janela
largura_tela = window.winfo_screenwidth()
altura_tela = window.winfo_screenheight()

largura_janela = 835
altura_janela = 895

pos_x = int((largura_tela / 2) - (largura_janela / 2))
pos_y = int((altura_tela / 2) - (altura_janela / 2))

# Tamanho da janela
window.geometry("{}x{}+{}+{}".format(largura_janela, altura_janela, pos_x, pos_y))
window.resizable(False, False)

caminho_icone = resource_path('icone.ico')
window.iconbitmap(caminho_icone)

######################janela para aceitar termos######################
janela_inicializacao = tk.Toplevel()
janela_inicializacao.title("Chapa Base - Responsabilidade")
janela_inicializacao.grab_set()

width_janela = 560
height_janela = 630 #arrumar dps-------------------------------------------------------------------------------------------------

new_pos_x = int((largura_tela / 2) - (width_janela / 2))
new_pos_y = int((altura_tela / 2) - (height_janela / 2))

janela_inicializacao.geometry("{}x{}+{}+{}".format(width_janela, height_janela, new_pos_x, new_pos_y))
janela_inicializacao.resizable(False, False)

janela_inicializacao.iconbitmap(caminho_icone)

frame_imagens_inic = ttk.Frame(janela_inicializacao)
frame_imagens_inic.grid(row=0, column=0, padx=4, pady=(25, 15), sticky="news")

frame_de_inicializacao = ttk.Frame(janela_inicializacao)
frame_de_inicializacao.grid(row=1, column=0, padx=4, pady=5, sticky="news")

frame_btn_inicial = ttk.Frame(janela_inicializacao)
frame_btn_inicial.grid(row=2, column=0, padx=1, pady=3, sticky="news")

img_ee = tk.PhotoImage(file=resource_path("ee.png"))
img_ufrgs = tk.PhotoImage(file=resource_path("ufrgs-logo-6.png"))

############
lbl_imagem_ee = ttk.Label(frame_imagens_inic, image=img_ee)
lbl_imagem_ee.grid(row=0, column=0, padx=(120, 50), pady=5)

lbl_imagem_ufrgs = ttk.Label(frame_imagens_inic, image=img_ufrgs)
lbl_imagem_ufrgs.grid(row=0, column=1, padx=5, pady=5)
#################
bg_ini_color = "#f0f0f0"

txt_inicializacao = tk.Text(frame_de_inicializacao, wrap="word", height=22, width=77, borderwidth=0, bg=bg_ini_color)
txt_inicializacao.grid(row=0, column=0, padx=5, pady=5, sticky="news")

mensagem_inicial = """\
    Esse software é uma ferramenta desenvolvida como parte do Trabalho de Conclusão
    do Curso de Engenharia Civil da Universidade Federal do Rio Grande do Sul, do
    aluno Petrick Eichwald Rosa dos Santos. O projeto foi realizado sob a orientação
    do professor Enio Carlos Mesacasa Júnior, que atuou como orientador durante todo
    o desenvolvimento do software.
    
    O objetivo deste programa é auxiliar no cálculo das principais dimensões de ligações
    de chapas de base de pilares metálicos, proporcionando uma solução prática para
    estudantes, engenheiros e profissionais da área.
    
    Os resultados fornecidos pelo software são baseados nas informações inseridas pelo
    usuário, e os desenvolvedores não se responsabilizam por quaisquer consequências 
    resultantes do uso das informações ou resultados gerados por este programa. O
    usuário é inteiramente responsável por verificar e validar os cálculos realizados
    pelo software, bem como por considerar todas as normas e regulamentos vigentes.
    
    Ao prosseguir e utilizar o software, você está concordando em assumir a
    responsabilidade pelas decisões e resultados obtidos através deste programa.
    
    Versão 1.0 - Agosto, 2023"""

txt_inicializacao.insert("1.0", mensagem_inicial)
txt_inicializacao.config(font=('Segoe UI', 10), state="disabled")

btn_ok = ttk.Button(frame_btn_inicial, text="Prosseguir", command=cancelar_inicial, width=15)
btn_ok.grid(row=0, column=0, padx=(160, 15))

btn_inic_sair = ttk.Button(frame_btn_inicial, text="Sair", command=recusar_sair, width=10)
btn_inic_sair.grid(row=0, column=1, padx=10)

#######################Volta para programa original##########################
# Variaveis, não sei muito bem como funciona, mas tem que ficar dentro da window
procedimento = tk.StringVar()
propriedade = tk.StringVar()

# Variaveis das imagens
img_1 = tk.PhotoImage(file=resource_path("imagem_principal.png"))
img_2 = tk.PhotoImage(file=resource_path("interno.png"))
img_3 = tk.PhotoImage(file=resource_path("6ch.png"))
img_4 = tk.PhotoImage(file=resource_path("8ch.png"))
img_5 = tk.PhotoImage(file=resource_path("10ch.png"))
img_6 = tk.PhotoImage(file=resource_path("resist_chumb.png"))

# Frame esquerdo
frame_esquerdo = ttk.Frame(window)
frame_esquerdo.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="news")
frame_esquerdo.rowconfigure(2, minsize=146)
frame_esquerdo.rowconfigure(3, minsize=96)

# Frame para botoões, abaixo do esquerdo
frame_esquerdo_baixo = ttk.Frame(window, style="TFrame")
frame_esquerdo_baixo.grid(row=1, column=0, padx=(10, 5), pady=1, sticky="news")

# Frame centro
frame_centro = ttk.Frame(window)
frame_centro.grid(row=0, column=1, pady=10, sticky="n")
frame_centro.rowconfigure(1, minsize=30)
frame_centro.rowconfigure(2, minsize=151)
frame_centro.columnconfigure(0, minsize=10)

# Frame para botões, abaixo do centro
frame_centro_baixo = ttk.Frame(window)
frame_centro_baixo.grid(row=1, column=1, sticky="n")

# Frame de procedimento
frame_procedimento = ttk.LabelFrame(frame_esquerdo, text="Procedimento")
frame_procedimento.grid(row=0, column=0, padx=10, pady=5, sticky="news")
frame_procedimento.columnconfigure(1, minsize=155)

var_procedimento = tk.StringVar(value="d")

rb_dimensionar = ttk.Radiobutton(frame_procedimento, text="Dimensionamento", value="d", variable=var_procedimento, command=dimensionar)
rb_dimensionar.grid(row=0, column=0, padx=(5, 1), pady=5, sticky="w")

rb_verificar = ttk.Radiobutton(frame_procedimento, text="Verificação", value="v", variable=var_procedimento, command=verificar)
rb_verificar.grid(row=0, column=1, padx=(12, 5), pady=5, sticky="w")

# Frame das solicitações
var_mu = tk.StringVar()
frame_solicitacoes = ttk.LabelFrame(frame_esquerdo, text="Solicitações")
frame_solicitacoes.grid(row=1, column=0, padx=10, pady=5, sticky="news")

lbl_pu = ttk.Label(frame_solicitacoes, text="Força axial (Pu)", width=20)
lbl_pu.grid(row=0, column=0, sticky="w", padx=5)

lbl_vu = ttk.Label(frame_solicitacoes, text="Força horizontal (Vu)")
lbl_vu.grid(row=1, column=0, sticky="w", padx=5)

lbl_mu = ttk.Label(frame_solicitacoes, text="Momento fletor (Mu)")
lbl_mu.grid(row=2, column=0, sticky="w", padx=5, pady=(1, 5))

ety_pu = ttk.Entry(frame_solicitacoes, width=13)
ety_pu.grid(row=0, column=1, padx=5, pady=1)

ety_vu = ttk.Entry(frame_solicitacoes, width=13)
ety_vu.grid(row=1, column=1, padx=5, pady=1)

ety_mu = ttk.Entry(frame_solicitacoes, width=13, textvariable=var_mu)
ety_mu.grid(row=2, column=1, padx=5, pady=(1, 5))

lbl_pu_unidades = ttk.Label(frame_solicitacoes, text="kN")
lbl_pu_unidades.grid(row=0, column=2, padx=5, sticky="w")

lbl_vu_unidades = ttk.Label(frame_solicitacoes, text="kN")
lbl_vu_unidades.grid(row=1, column=2, padx=5, sticky="w")

lbl_mu_unidades = ttk.Label(frame_solicitacoes, text="kNm")
lbl_mu_unidades.grid(row=2, column=2, padx=5, pady=(1, 5), sticky="w")

# Frame das propriedades do perfil
var_perfil_zx = tk.StringVar()

frame_perfil = ttk.LabelFrame(frame_esquerdo, text="Perfil")
frame_perfil.grid(row=2, column=0, padx=10, pady=5, sticky="news")

var_propriedade = tk.StringVar(value="t")
rb_tabelado = ttk.Radiobutton(frame_perfil, text="Tabelado", value="t", variable=var_propriedade, command=tabelado, width=16)
rb_tabelado.grid(row=0, column=0, padx=5, sticky="nw")

rb_usuario = ttk.Radiobutton(frame_perfil, text="Usuário", value="u", variable=var_propriedade, command=usuario)
rb_usuario.grid(row=0, column=1, padx=10, sticky="nw")

lbl_perfil_familia = ttk.Label(frame_perfil, text="Família")
lbl_perfil_familia.grid(row=1, column=0, padx=5, sticky="nw")

variavel_familia = tk.StringVar()
cmb_perfil_familia = ttk.Combobox(frame_perfil, state="readonly", values=list(gerdau_w.dic_familias.keys()), width=10, textvariable=variavel_familia)
cmb_perfil_familia.bind("<<ComboboxSelected>>", selecionar_familia)
cmb_perfil_familia.grid(row=1, column=1, padx=10, pady=1, sticky="w")

lbl_perfil_nome = ttk.Label(frame_perfil, text="Perfil W")
lbl_perfil_nome.grid(row=2, column=0, padx=5, sticky="nw")

variavel_perfil = tk.StringVar()
cmb_perfil_nome = ttk.Combobox(frame_perfil, width=10, state="readonly", textvariable=variavel_perfil)
cmb_perfil_nome.bind("<<ComboboxSelected>>", informacoes_perfil)
cmb_perfil_nome.grid(row=2, column=1, padx=10, pady=1, sticky="w")

var_perfil_d = tk.StringVar()
lbl_perfil_d = ttk.Label(frame_perfil, text="Altura (d)", state="disabled")
lbl_perfil_d.grid(row=3, column=0, padx=5, sticky="nw")
ety_perfil_d = ttk.Entry(frame_perfil, width=13, state="disabled", textvariable=var_perfil_d)
ety_perfil_d.grid(row=3, column=1, padx=10, pady=1, sticky="w")
lbl_perfil_d_unid = ttk.Label(frame_perfil, text="mm", state="disabled")
lbl_perfil_d_unid.grid(row=3, column=2, sticky="w")

var_perfil_bf = tk.StringVar()
lbl_perfil_bf = ttk.Label(frame_perfil, text="Largura (bf)", state="disabled")
lbl_perfil_bf.grid(row=4, column=0, padx=5, sticky="nw")
ety_perfil_bf = ttk.Entry(frame_perfil, width=13, state="disabled", textvariable=var_perfil_bf)
ety_perfil_bf.grid(row=4, column=1, padx=10, pady=1, sticky="w")
lbl_perfil_bf_unid = ttk.Label(frame_perfil, text="mm", state="disabled")
lbl_perfil_bf_unid.grid(row=4, column=2, sticky="w")

var_perfil_tw = tk.StringVar()
lbl_perfil_tw = ttk.Label(frame_perfil, text="Esp. alma (tw)", state="disabled")
lbl_perfil_tw.grid(row=5, column=0, padx=5, pady=1, sticky="w")
ety_perfil_tw = ttk.Entry(frame_perfil, width=13, state="disabled", textvariable=var_perfil_tw)
ety_perfil_tw.grid(row=5, column=1, padx=10, pady=1, sticky="w")
lbl_perfil_tw_unid = ttk.Label(frame_perfil, text="mm", state="disabled")
lbl_perfil_tw_unid.grid(row=5, column=2, sticky="w")

var_perfil_tf = tk.StringVar()
lbl_perfil_tf = ttk.Label(frame_perfil, text="Esp. mesa (tf)", state="disabled")
lbl_perfil_tf.grid(row=6, column=0, padx=5, pady=1, sticky="w")
ety_perfil_tf = ttk.Entry(frame_perfil, width=13, state="disabled", textvariable=var_perfil_tf)
ety_perfil_tf.grid(row=6, column=1, padx=10, pady=1, sticky="w")
lbl_perfil_tf_unid = ttk.Label(frame_perfil, text="mm", state="disabled")
lbl_perfil_tf_unid.grid(row=6, column=2, pady=1, sticky="w")

var_perfil_ag = tk.StringVar()
lbl_perfil_ag = ttk.Label(frame_perfil, text="Área do perfil (Ag)")
lbl_perfil_ag.grid(row=7, column=0, padx=5, pady=3, sticky="w")
value_perfil_ag = ttk.Label(frame_perfil, textvariable=var_perfil_ag)
value_perfil_ag.grid(row=7, column=1, padx=10, pady=3, sticky="w")
lbl_perfil_ag_unid = ttk.Label(frame_perfil, text="cm²")
lbl_perfil_ag_unid.grid(row=7, column=2, pady=3, sticky="w")

var_perfil_fyk = tk.StringVar()
lbl_perfil_fyk = ttk.Label(frame_perfil, text="Resist. do aço (fyk)")
lbl_perfil_fyk.grid(row=8, column=0, padx=5, pady=(0, 5), sticky="w")
ety_perfil_fyk = ttk.Entry(frame_perfil, width=13, textvariable=var_perfil_fyk)
ety_perfil_fyk.grid(row=8, column=1, padx=10, pady=(1, 5), sticky="w")
lbl_perfil_fyk = ttk.Label(frame_perfil, text="MPa")
lbl_perfil_fyk.grid(row=8, column=2, pady=(0, 5), sticky="w")

# Fazer o frame do concreto
frame_concreto = ttk.LabelFrame(frame_esquerdo, text="Base de concreto")
frame_concreto.grid(row=3, column=0, padx=10, pady=5, sticky="news")

lbl_concreto = ttk.Label(frame_concreto, text="Resist. do concreto")
lbl_concreto.grid(row=0, column=0, padx=5, pady=1, sticky="news")
ety_fck = ttk.Entry(frame_concreto, width=13)
ety_fck.grid(row=0, column=1, padx=(23, 5), pady=1, sticky="w")
lbl_fck = ttk.Label(frame_concreto, text="MPa")
lbl_fck.grid(row=0, column=2, padx=5, pady=1, sticky="news")

lbl_proporcao = ttk.Label(frame_concreto, text="Proporção da base")
lbl_proporcao.grid(row=1, column=0, padx=5, pady=1, sticky="news")
variavel_proporcao = tk.DoubleVar()
scl_proporcao = tk.Scale(frame_concreto, from_=1, to=4, orient=tk.HORIZONTAL, resolution=0.01, length=84,
                         showvalue=False, variable=variavel_proporcao)
scl_proporcao.grid(row=1, column=1, padx=(20, 1), pady=(1, 1), sticky="nw")
lbl_variavel_proporcao = ttk.Label(frame_concreto, textvariable=variavel_proporcao)
lbl_variavel_proporcao.grid(row=1, column=2)

#var_nb = tk.StringVar()
#lbl_nb_concreto = ttk.Label(frame_concreto, text="Comprimento (Nb)", state="disabled")
#lbl_nb_concreto.grid(row=2, column=0, padx=5, pady=1, sticky="w")
#ety_nb_concreto = ttk.Entry(frame_concreto, width=13, state="disabled", textvariable=var_nb)
#ety_nb_concreto.grid(row=2, column=1, padx=(23, 5), pady=1, sticky="w")
#lbl_nb_unid = ttk.Label(frame_concreto, text="cm", state="disabled")
#lbl_nb_unid.grid(row=2, column=2, padx=5, pady=1, sticky="w")
#var_nb.set("--ETY NB--")

#var_bb = tk.StringVar()
#lbl_bb_concreto = ttk.Label(frame_concreto, text="Largura (Bb)", state="disabled")
#lbl_bb_concreto.grid(row=3, column=0, padx=5, pady=1, sticky="w")
#ety_bb_concreto = ttk.Entry(frame_concreto, width=13, state="disabled", textvariable=var_bb)
#ety_bb_concreto.grid(row=3, column=1, padx=(23, 5), pady=1, stick="w")
#lbl_bb_unid = ttk.Label(frame_concreto, text="cm", state="disabled")
#lbl_bb_unid.grid(row=3, column=2, padx=5, pady=1, sticky="w")
#var_bb.set("--ETY BB--")

var_concreto_a2 = tk.StringVar()
lbl_area_concreto = ttk.Label(frame_concreto, text="Área de concreto", state="disabled")
lbl_area_concreto.grid(row=2, column=0, padx=5, pady=(1, 5), sticky="w")
ety_area_concreto = ttk.Entry(frame_concreto, width=13, state="disabled", textvariable=var_concreto_a2)
ety_area_concreto.grid(row=2, column=1, padx=(23, 5), pady=(1, 5), sticky="w")
lbl_area_concreto_unid = ttk.Label(frame_concreto, text="cm²", state="disabled")
lbl_area_concreto_unid.grid(row=2, column=2, padx=5, pady=(1, 5), sticky="w")

# Frame da chapa de base
frame_chapa_base = ttk.LabelFrame(frame_esquerdo, text="Chapa base")
frame_chapa_base.grid(row=4, column=0, padx=10, pady=5, sticky="news")

lbl_chapa_base = ttk.Label(frame_chapa_base, text="Resist. do aço ")
lbl_chapa_base.grid(row=0, column=0, padx=5, pady=1, sticky="w")
ety_fy = ttk.Entry(frame_chapa_base, width=13)
ety_fy.grid(row=0, column=1, padx=(30, 5), pady=1, sticky="w")
lbl_fy = ttk.Label(frame_chapa_base, text="MPa")
lbl_fy.grid(row=0, column=2, padx=5, pady=1, sticky="w")

lbl_chapa_n = ttk.Label(frame_chapa_base, text="Comprimento (N)", state="disabled")
lbl_chapa_n.grid(row=1, column=0, padx=5, pady=1, sticky="w")
var_chapa_n = tk.StringVar()
ety_chapa_n = ttk.Entry(frame_chapa_base, width=13, state="disabled", textvariable=var_chapa_n)
ety_chapa_n.grid(row=1, column=1, padx=(30, 5), pady=1, sticky="w")
lbl_chapa_n_unid = ttk.Label(frame_chapa_base, text="mm", state="disabled")
lbl_chapa_n_unid.grid(row=1, column=2, padx=5, pady=1, sticky="w")

lbl_chapa_b = ttk.Label(frame_chapa_base, text="Largura (B)", state="disabled")
lbl_chapa_b.grid(row=2, column=0, padx=5, sticky="w")
var_chapa_b = tk.StringVar()
ety_chapa_b = ttk.Entry(frame_chapa_base, width=13, state="disabled", textvariable=var_chapa_b)
ety_chapa_b.grid(row=2, column=1, padx=(30, 5), pady=1, sticky="w")
lbl_chapa_b_unid = ttk.Label(frame_chapa_base, text="mm", state="disabled")
lbl_chapa_b_unid.grid(row=2, column=2, padx=5, pady=1, sticky="w")

lbl_chapa_tp = ttk.Label(frame_chapa_base, text="Espessura (tp)", state="disabled")
lbl_chapa_tp.grid(row=3, column=0, padx=5, pady=(1, 5), sticky="w")
var_chapa_tp = tk.StringVar()
ety_chapa_tp = ttk.Entry(frame_chapa_base, width=13, state="disabled", textvariable=var_chapa_tp)
ety_chapa_tp.grid(row=3, column=1, padx=(30, 5), pady=(1, 5), sticky="w")
lbl_chapa_tp_unid = ttk.Label(frame_chapa_base, text="mm", state="disabled")
lbl_chapa_tp_unid.grid(row=3, column=2, padx=5, pady=(1, 5), sticky="w")

# Frame dos chumbadores
frm_chumbadores = ttk.LabelFrame(frame_esquerdo, text="Chumbadores")
frm_chumbadores.grid(row=5, column=0, padx=10, pady=5, sticky="news")

var_ch_ligacao = tk.StringVar(value="e")
rb_engaste = ttk.Radiobutton(frm_chumbadores, text="Engaste", value="e", variable=var_ch_ligacao, command=engastado)
rb_engaste.grid(row=0, column=0, padx=5, pady=1, sticky="w")
rb_rotula = ttk.Radiobutton(frm_chumbadores, text="Articulação", value="r", variable=var_ch_ligacao, command=rotulado)
rb_rotula.grid(row=0, column=1, padx=(24, 5), pady=1, sticky="w")

var_numero_chumbadores = tk.StringVar()
lbl_quantidade_chumbador = ttk.Label(frm_chumbadores, text="Quantidade")
lbl_quantidade_chumbador.grid(row=1, column=0, padx=5, pady=1, sticky="w")
cmb_quantidade_chumbador = ttk.Combobox(frm_chumbadores, state="readonly", values=["4", "6", "8", "10"],
                                        textvariable=var_numero_chumbadores, width=10)
cmb_quantidade_chumbador.bind("<<ComboboxSelected>>", numero_chumbadores)
cmb_quantidade_chumbador.grid(row=1, column=1, padx=(24, 5), pady=1, sticky="w")
cmb_quantidade_chumbador.set("4")

lbl_material_chumbador = ttk.Label(frm_chumbadores, text="Material: F1554")
lbl_material_chumbador.grid(row=2, column=0, padx=5, pady=1, sticky="w")
cmb_material_chumbador = ttk.Combobox(frm_chumbadores, state="readonly", values=list(chumbadores.dic_materiais.keys()),
                                      width=10)
cmb_material_chumbador.grid(row=2, column=1, padx=(24, 5), pady=1, sticky="w")
btn_material_help = ttk.Button(frm_chumbadores, text="...", command=material_help, width=2)
btn_material_help.grid(row=2, column=2, padx=5, pady=0)

lbl_chumbadores_diametro = ttk.Label(frm_chumbadores, text="Diâmetro", state="disabled")
lbl_chumbadores_diametro.grid(row=3, column=0, padx=5, pady=1, sticky="w")
cmb_chumbadores_diametro = ttk.Combobox(frm_chumbadores, values=list(chumbadores.lista_chumbadores.keys()), width=10,
                                        state="disabled")
cmb_chumbadores_diametro.grid(row=3, column=1, padx=(24, 5), pady=1, sticky="w")

lbl_chumbadores_embutimento = ttk.Label(frm_chumbadores, text="Embutimento (hef)", state="disabled")
lbl_chumbadores_embutimento.grid(row=4, column=0, padx=5, pady=1, sticky="w")
var_hef_chumb = tk.StringVar()
ety_chumbadores_embutimento = ttk.Entry(frm_chumbadores, width=13, state="disabled", textvariable=var_hef_chumb)
ety_chumbadores_embutimento.grid(row=4, column=1, padx=(24, 5), pady=1, sticky="w")
lbl_chumbadores_embutimento_unid = ttk.Label(frm_chumbadores, text="mm", state="disabled")
lbl_chumbadores_embutimento_unid.grid(row=4, column=2, padx=5, pady=1, sticky="w")

lbl_chumbadores_a1 = ttk.Label(frm_chumbadores, text="Distância (a1)", state="disabled")
lbl_chumbadores_a1.grid(row=5, column=0, padx=5, pady=1, sticky="w")
var_chumb_a1 = tk.StringVar()
ety_chumbadores_a1 = ttk.Entry(frm_chumbadores, width=13, state="disabled", textvariable=var_chumb_a1)
ety_chumbadores_a1.grid(row=5, column=1, padx=(24, 5), pady=1, sticky="w")
lbl_chumbadores_a1_unid = ttk.Label(frm_chumbadores, text="mm", state="disabled")
lbl_chumbadores_a1_unid.grid(row=5, column=2, padx=5, pady=1, sticky="w")

lbl_chumbadores_a2 = ttk.Label(frm_chumbadores, text="Distância (a2)", state="disabled")
lbl_chumbadores_a2.grid(row=6, column=0, padx=5, pady=(1, 5), sticky="w")
var_chumb_a2 = tk.StringVar()
ety_chumbadores_a2 = ttk.Entry(frm_chumbadores, width=13, state="disabled", textvariable=var_chumb_a2)
ety_chumbadores_a2.grid(row=6, column=1, padx=(24, 5), pady=(1, 5), sticky="w")
lbl_chumbadores_a2_unid = ttk.Label(frm_chumbadores, text="mm", state="disabled")
lbl_chumbadores_a2_unid.grid(row=6, column=2, padx=5, pady=(1, 5), sticky="w")

# Frame dos botões
frm_botoes = ttk.Frame(frame_esquerdo_baixo)
frm_botoes.grid(row=0, column=0, padx=10, pady=5, sticky="s")

btn_principal = ttk.Button(frm_botoes, text="Dimensionar", command=click_dimensionar, width=15)
btn_principal.grid(row=0, column=0, padx=5, pady=5)

btn_cancelar = ttk.Button(frm_botoes, text="Cancelar", command=cancelar)
btn_cancelar.grid(row=0, column=1, padx=5, pady=5)

btn_ajuda = ttk.Button(frm_botoes, text="Sobre", command=botao_sobre)
btn_ajuda.grid(row=0, column=2, padx=5, pady=5)

# ------------------------------------------------------DIREITA---------------------------------------------------------

# Frame da imagem
lbl_imagem_principal = ttk.Label(frame_centro, image=img_1)
lbl_imagem_principal.grid(row=0, column=0, padx=5, pady=5)

# Frame status
frm_status = ttk.LabelFrame(frame_centro, text="Status")
frm_status.grid(row=1, column=0, padx=5, pady=(1, 5), sticky="new")

# label do status do programa
var_status = tk.StringVar()
lbl_status = ttk.Label(frm_status, textvariable=var_status)
lbl_status.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")
lbl_status.config(font=('Segoe UI', 10, 'italic'))
var_status.set("")


# Frame dos resultados
frm_resumo = ttk.LabelFrame(frame_centro, text="Resumo") #tenho que ver como não precisar indicar o tamanho do frame
frm_resumo.grid(row=2, column=0, padx=5, pady=(1, 10), sticky="news")
frm_resumo.columnconfigure(1, minsize=50, weight=0)
frm_resumo.columnconfigure(2, minsize=50, weight=0)
frm_resumo.columnconfigure(4, minsize=50, weight=0)

# Resultado da altura da chapa base (acho que terei que definir tamnhos para as colunas, para não ficar se mexendo com os valores
lbl_resumo_altura_chapa = ttk.Label(frm_resumo, text="Comprimento da chapa (N)")
lbl_resumo_altura_chapa.grid(row=0, column=0, padx=5, sticky="w")
var_chapa_n2 = tk.StringVar()
lbl_resumo_altura_chapa_valor = ttk.Label(frm_resumo, textvariable=var_chapa_n2, width=8)
lbl_resumo_altura_chapa_valor.grid(row=0, column=1, padx=5, sticky="w")
lbl_resumo_altura_chapa_unid = ttk.Label(frm_resumo, text="mm")
lbl_resumo_altura_chapa_unid.grid(row=0, column=2, padx=5, sticky="w")

# Resultado da largura da chapa base
lbl_resumo_largura_chapa = ttk.Label(frm_resumo, text="Largura da chapa (B)")
lbl_resumo_largura_chapa.grid(row=1, column=0, padx=5, sticky="w")
var_chapa_b2 = tk.StringVar()
lbl_resumo_largura_chapa_valor = ttk.Label(frm_resumo, textvariable=var_chapa_b2) # Bem provavel que seja um text variable
lbl_resumo_largura_chapa_valor.grid(row=1, column=1, padx=5, sticky="w")
lbl_resumo_largura_chapa_unid = ttk.Label(frm_resumo, text="mm")
lbl_resumo_largura_chapa_unid.grid(row=1, column=2, padx=5, sticky="w")

# Resultado da espessura de chapa base
lbl_resumo_espessura_chapa = ttk.Label(frm_resumo, text="Espessura da chapa (tp)")
lbl_resumo_espessura_chapa.grid(row=2, column=0, padx=5, sticky="w")
var_chapa_tp2 = tk.StringVar()
lbl_resumo_espessura_chapa_valor = ttk.Label(frm_resumo, textvariable=var_chapa_tp2) # bem provavel que seja um textvariable
lbl_resumo_espessura_chapa_valor.grid(row=2, column=1, padx=5, sticky="w")
lbl_resumo_espessura_chapa_unid = ttk.Label(frm_resumo, text="mm")
lbl_resumo_espessura_chapa_unid.grid(row=2, column=2, padx=5, sticky="w")

# Áreas
lbl_resumo_area_chapa = ttk.Label(frm_resumo, text="Área de chapa")
lbl_resumo_area_chapa.grid(row=0, column=3, padx=5, sticky="w")
var_area_chapa = tk.StringVar()
lbl_resumo_area_chapa_valor = ttk.Label(frm_resumo, textvariable=var_area_chapa)
lbl_resumo_area_chapa_valor.grid(row=0, column=4, padx=5, sticky="w")
lbl_resumo_area_chapa_unid = ttk.Label(frm_resumo, text="cm²")
lbl_resumo_area_chapa_unid.grid(row=0, column=5, padx=5, sticky="w")

lbl_resumo_area_concreto = ttk.Label(frm_resumo, text="Área de concreto")
lbl_resumo_area_concreto.grid(row=1, column=3, padx=5, sticky="w")
var_concreto_a2_2 = tk.StringVar()
lbl_resumo_area_concreto_valor = ttk.Label(frm_resumo, textvariable=var_concreto_a2_2, width=8)
lbl_resumo_area_concreto_valor.grid(row=1, column=4, padx=5, sticky="w")
lbl_resumo_area_concreto_unid = ttk.Label(frm_resumo, text="cm²")
lbl_resumo_area_concreto_unid.grid(row=1, column=5, padx=5, sticky="w")

# Resultados dos chumbadores
lbl_resumo_chumbadores = ttk.Label(frm_resumo, text="Diâmetro dos chumbadores")
lbl_resumo_chumbadores.grid(row=4, column=0, padx=5, pady=(8, 2), sticky="w")

var_chumb_diametro = tk.StringVar()
lbl_resumo_chumbadores_diametro = ttk.Label(frm_resumo, textvariable=var_chumb_diametro)
lbl_resumo_chumbadores_diametro.grid(row=4, column=1, padx=5, pady=(8, 2), sticky="w")

lbl_resumo_dist_a1 = ttk.Label(frm_resumo, text="Distância (a1)")
lbl_resumo_dist_a1.grid(row=5, column=0, padx=5, sticky="w")

var_chumb_a1_2 = tk.StringVar()
lbl_resumo_dist_a1_valor = ttk.Label(frm_resumo, textvariable=var_chumb_a1_2)
lbl_resumo_dist_a1_valor.grid(row=5, column=1, padx=5, sticky="w")

lbl_resumo_dist_a1_unid = ttk.Label(frm_resumo, text="mm")
lbl_resumo_dist_a1_unid.grid(row=5, column=2, padx=5, sticky="w")

lbl_resumo_dist_a2 = ttk.Label(frm_resumo, text="Distância (a2)")
lbl_resumo_dist_a2.grid(row=5, column=3, padx=5, sticky="w")

var_chumb_a2_2 = tk.StringVar()
lbl_resumo_dist_a2_valor = ttk.Label(frm_resumo, textvariable=var_chumb_a2_2)
lbl_resumo_dist_a2_valor.grid(row=5, column=4, padx=5, sticky="w")

lbl_resumo_dist_a2_unid = ttk.Label(frm_resumo, text="mm")
lbl_resumo_dist_a2_unid.grid(row=5, column=5, padx=5, sticky="w")

# Frame do memorial de cálculo
frm_calculos = ttk.LabelFrame(frame_centro, text="Memorial")
frm_calculos.grid(row=3, column=0, padx=5, pady=(1, 0), sticky="news")  # pady era 5

txt_saida = tk.Text(frm_calculos, width=65, height=22, background="white")
txt_saida.grid(row=0, column=0, padx=(10, 0), pady=(9, 9))
txt_saida.configure(font=('Segoe UI', 10))
txt_saida.tag_configure("bold", font=('Segoe UI', 10, "bold"))
txt_saida.tag_configure("italic", font=('Segoe UI', 10, "italic"))
sys.stdout = TextRedirector(txt_saida)

scrollbar = tk.Scrollbar(frm_calculos, orient='vertical', command=txt_saida.yview)
scrollbar.grid(row=0, column=1, padx=(0, 5), pady=(8, 9), sticky='ns')
txt_saida['yscrollcommand'] = scrollbar.set

# Frame dos botões salvar
frm_btn_txt = ttk.Frame(frame_centro_baixo)
frm_btn_txt.grid(row=1, column=0, padx=10, pady=5, sticky="w")

btn_save = ttk.Button(frm_btn_txt, text="Salvar", command=lambda: click_salvar(txt_saida))
btn_save.grid(row=0, column=0, padx=5, pady=5)

btn_clear = ttk.Button(frm_btn_txt, text="Limpar", command=lambda: click_limpar(txt_saida))
btn_clear.grid(row=0, column=1, padx=5, pady=6)


window.mainloop()

# usar o auto-py-to-exe para gerar executavel
# adicionar todas as imagens usadas no programa
