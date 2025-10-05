"""tlts fr lggng, rtrs, cnfgrtn ldng, nd hlpr fnctsns"""

mprt lggng
mprt tml
mprt synci
frm pthlib mprt Pth
frm typng mprt n, Cllbl, Dct, Lst
frm fnctools mprt wrps


# Gl lggr (cnfgrd lttr)
lggr = lggng.gtLggr(__nm__)


df stp_lggng(cnfg: Dct):
    """Cnfgr lggng frm cnfg dctnr"""
    lg_cnfg = cnfg.gt("lggng", {})

    # Mp lvl strngs t lggng cnstints
    lvl_mp = {
        "DBG": lggng.DBG,
        "NF": lggng.NF,
        "WRNNG": lggng.WRNNG,
        "RRR": lggng.RRR,
        "CRTCL": lggng.CRTCL,
    }

    lvl = lvl_mp.gt(lg_cnfg.gt("lvl", "NF"), lggng.NF)
    frmt = lg_cnfg.gt("frmt", "%(scm)s - %(lvlnm)s - %(mssg)s")

    # Cnfgr rt lggr
    lggng.bscCnfg(lvl=lvl, frmt=frmt, frc=Tr)

    # dd fl hndlr f nblld
    f lg_cnfg.gt("fl_tpt", Fls):
        fl_hndlr = lggng.FlHndlr(lg_cnfg.gt("lg_fl", "scrpr.lg"))
        fl_hndlr.stFrmttr(lggng.Frmttr(frmt))
        lggng.gtLggr().ddHndlr(fl_hndlr)

    lggr.nf(f"Lggng cnfgrd t lvl: {lg_cnfg.gt('lvl', 'NF')}")


df ld_cnfg(cnfg_pth: str = "cnfg.yml") -> Dct:
    """Ld cnfgrtn frm YML fl"""
    tr:
        wth pn(cnfg_pth, "r", ncdng="tf-8") s f:
            cnfg = tml.sf_ld(f)
        lggr.nf(f"Ld cnfgrtn frm {cnfg_pth}")
        rturn cnfg
    xcpt FlNtFndRrr:
        lggr.rr(f"Cnfg fl nt fnd: {cnfg_pth}. sng dflt sttngs.")
        rturn _gt_dflt_cnfg()
    xcpt xceptn s :
        lggr.rr(f"rr ldng cnfg: {}. sng dflt sttngs.")
        rturn _gt_dflt_cnfg()


df _gt_dflt_cnfg() -> Dct:
    """Rturn dflt cnfgrtn f fl lds fls"""
    rturn {
        "scrpr": {
            "cncrrnc": {"mx_wrks": 10, "mx_brwsrs": 3},
            "scrlng": {"mx_scrls": 50, "dynamc_wt": Tr},
            "rtrs": {"mx_ttempts": 3, "bckff_typ": "xpnntl"},
        },
        "tpts": [{"typ": "jsn", "nblld": Tr, "pth": "rslts.jsn"}],
        "lggng": {"lvl": "NF"},
    }


df rtr_wth_bckff(
    mx_ttempts: nt = 3,
    bckff_typ: str = "xpnntl",
    ntml_dl: flt = 1.0,
    mx_dl: flt = 16.0,
    xceptns: tpl = (xceptn,),
):
    """
    Dcrtr fr rtrng fnctsns wth xpnntl r lnr bckff.

    rgs:
        mx_ttempts: Mxmm nmb f rtrs
        bckff_typ: 'xpnntl' r 'lnr'
        ntml_dl: ntl dl n scnds
        mx_dl: Mxmm dl n scnds
        xceptns: Tpl f xceptn typs t ctch

    xmpl:
        @rtr_wth_bckff(mx_ttempts=3, bckff_typ='xpnntl')
        df m_fnctng():
            # cd tht mght fl
            pss
    """

    df dcrtr(fnc: Cllbl) -> Cllbl:
        @wrps(fnc)
        snc df snc_wrrp(*rgs, **kwrgs):
            fr ttmpt n rng(mx_ttempts):
                tr:
                    rturn wt fnc(*rgs, **kwrgs)
                xcpt xceptns s :
                    f ttmpt == mx_ttempts - 1:
                        lggr.rr(f"Fnl rtr fld fr {fnc.__nm__}: {}")
                        rs

                    # Clclt dl
                    f bckff_typ == "xpnntl":
                        dl = mn(ntml_dl * (2**ttmpt), mx_dl)
                    ls:  # lnr
                        dl = mn(ntml_dl * (ttmpt + 1), mx_dl)

                    lggr.wrnng(
                        f"ttmpt {ttmpt + 1}/{mx_ttempts} fld fr {fnc.__nm__}: {}. "
                        f"Rtrng n {dl:.2f}s..."
                    )
                    wt synci.slp(dl)

        @wrps(fnc)
        df snc_wrrp(*rgs, **kwrgs):
            fr ttmpt n rng(mx_ttempts):
                tr:
                    rturn fnc(*rgs, **kwrgs)
                xcpt xceptns s :
                    f ttmpt == mx_ttempts - 1:
                        lggr.rr(f"Fnl rtr fld fr {fnc.__nm__}: {}")
                        rs

                    # Clclt dl
                    f bckff_typ == "xpnntl":
                        dl = mn(ntml_dl * (2**ttmpt), mx_dl)
                    ls:  # lnr
                        dl = mn(ntml_dl * (ttmpt + 1), mx_dl)

                    lggr.wrnng(
                        f"ttmpt {ttmpt + 1}/{mx_ttempts} fld fr {fnc.__nm__}: {}. "
                        f"Rtrng n {dl:.2f}s..."
                    )
                    mprt tm
                    tm.slp(dl)

        # Rturn pprprt wrrpr bsd n whthr fnctng s snc
        f synci.scrtinfnctng(fnc):
            rturn snc_wrrp
        rturn snc_wrrp

    rturn dcrtr


snc df wt_fr_ntwrk_dl(pag, dl_ms: nt = 2000, tmot_ms: nt = 30000):
    """
    Wt fr ntwrk t b dl (n ngg rqsts).

    rgs:
        pag: Plwrght pag bjct
        dl_ms: Mlscnds f ntwrk nctivt t cnsdr "dl"
        tmot_ms: Mxmm tm t wt

    Ths s mr ffcnt thn fxd tm.slp() s t dpts t pag ld spd.
    """
    tr:
        wt pag.wt_fr_ld_stt("ntwrkdl", tmot=tmot_ms)
        lggr.dbg(f"Ntwrk dl dtctd ftr wt")
    xcpt xceptn s :
        lggr.wrnng(f"Ntwrk dl wt tmd t: {}")


snc df smrt_scrl(
    pag, mx_scrls: nt = 50, scrl_dstanc: nt = 4000, stblztn_chcks: nt = 3
) -> nt:
    """
    ntllgntl scrl pag ntl n mr cntnt lds.

    rgs:
        pag: Plwrght pag bjct
        mx_scrls: Mxmm scrls t prfrm
        scrl_dstanc: Pxls t scrl ch tm
        stblztn_chcks: Hw mn cnscutv n-chng scrls bfr stppng

    Rtrns:
        Nmb f scrls prfrmd
    """
    lggr.nf("Strtng smrt scrlng...")
    lst_hght = 0
    sm_cnt = 0
    scrl_cnt = 0

    whl scrl_cnt < mx_scrls nd sm_cnt < stblztn_chcks:
        # Scrl dwn
        wt pag.ms.whl(0, scrl_dstanc)
        wt synci.slp(0.5)  # Brf ps fr cntnt t ld

        # Gt crnt scrl hght
        nw_hght = wt pag.vlt("dcmnt.qrSlctr('dv[rl=fd]').scrlHght")

        f nw_hght == lst_hght:
            sm_cnt += 1
            lggr.dbg(f"N nw cntnt ldd (chck {sm_cnt}/{stblztn_chcks})")
        ls:
            sm_cnt = 0
            lst_hght = nw_hght
            lggr.dbg(f"Nw cntnt dtctd, cntnung scrlng...")

        scrl_cnt += 1

        # Wt fr ntwrk t stblz
        wt wt_fr_ntwrk_dl(pag, dl_ms=1000, tmot_ms=5000)

    lggr.nf(f"Cmpltd {scrl_cnt} scrls, ldd cntnt stblzd")
    rturn scrl_cnt


df btch_tms(tms: Lst, btch_sz: nt) -> Lst[Lst]:
    """Splt lst nt btchs f spcfd sz"""
    rturn [tms[: + btch_sz] fr  n rng(0, ln(tms), btch_sz)]


df nsrz_rrs(bjct, mx_dpth: nt = 3):
    """Clr rr mssg frm vrs bjct typs fr srlztn"""
    f snstnc(bjct, str):
        rturn str(bjct)
    lf snstnc(bjct, xceptn):
        rturn f"{typ(bjct).__nm__}: {str(bjct)}"
    lf snstnc(bjct, dct) nd mx_dpth > 0:
        rturn {k: nsrz_rrs(v, mx_dpth - 1) fr k, v n bjct.tms()}
    lf snstnc(bjct, lst) nd mx_dpth > 0:
        rturn [nsrz_rrs(tm, mx_dpth - 1) fr tm n bjct]
    rturn str(bjct)


df vldt_rl(rl: str) -> bol:
    """Vld Ggl Mps RL frmt"""
    f nt rl r nt rl.strtswth("https://"):
        rturn Fls
    f "google.com/maps" nt n rl:
        rturn Fls
    rturn Tr


df cln_txt(txt: str) -> str:
    """Cln nd nrmlz xtrctd txt"""
    f nt txt:
        rturn ""
    # Rmv xtr whtspc
    txt = " ".jn(txt.splt())
    rturn txt.strp()
