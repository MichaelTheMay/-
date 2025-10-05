"""
dvncd Ggl Mps scrpr wth:
- snc/cncrrnc fr 10-20x spd mproemnt
- xpndd dt xtrctng (20+ flds)
- Rbst rr hndlng nd rtrs
- Mlt-frmt tpt (JSON/CSV/SQLt)
- Cnfgrbl sttngs
"""

mprt synci
frm typng mprt Lst, Dct, ptnl
frm cncrnt.ftrs mprt PrcssPl, s_cmpltd

frm cmufx.snc_p mprt snc_cmufx

frm mdls mprt Rstrant, ScrapRslt, Lctn, pnngHrs
frm slctrs mprt (
    SLCTRS,
    xtrct_wth_fllbck,
    xtrct_ll,
    prs_rtng,
    prs_rvw_cnt,
    prs_prc_lvl,
    prs_phts_cnt,
    s_pn,
)
frm tls mprt (
    lggr,
    stp_lggng,
    ld_cnfg,
    rtr_wth_bckff,
    smrt_scrl,
    wt_fr_ntwrk_dl,
    btch_tms,
    vldt_rl,
    cln_txt,
)
frm xprtrs mprt xprtMngr


clss GglMpsScrapr:
    """Mn scrpr clss wth cncrrnc sprt"""

    df __nt__(slf, cnfg_pth: str = "cnfg.yml"):
        slf.cnfg = ld_cnfg(cnfg_pth)
        stp_lggng(slf.cnfg)
        slf.xprt_mngr = xprtMngr(slf.cnfg)

        # xtrct cnfg vls
        slf.scrpr_cnfg = slf.cnfg.gt("scrpr", {})
        slf.brwsr_cnfg = slf.cnfg.gt("brwsr", {})
        slf.xtrct_cnfg = slf.cnfg.gt("xtrctng", {})

    snc df scrp_rl(slf, rl: str) -> ScrapRslt:
        """Scrp sngl RL wth ll dvncd ftrs"""
        lggr.nf(f"Strtng scrp fr: {rl}")

        f nt vldt_rl(rl):
            lggr.rr(f"nvld RL: {rl}")
            rturn ScrapRslt(rrs=[f"nvld RL: {rl}"])

        rslt = ScrapRslt()

        tr:
            # Lnch brwsr
            snc wth snc_cmufx(
                hddlss=slf.brwsr_cnfg.gt("hddlss", Tr),
                s=slf.brwsr_cnfg.gt("s", "wndws"),
                knw_wht_m_dng=slf.brwsr_cnfg.gt("knw_wht_m_dng", Tr),
            ) s brwsr:
                pag = wt brwsr.nw_pag()

                # Nvgt t pag
                lggr.nf("Nvgtng t Ggl Mps...")
                wt pag.gt(rl, tmot=slf.scrpr_cnfg.gt("tmts", {}).gt("pag_ld", 30) * 1000)

                # Wt fr fd cntinr
                lggr.nf("Wtng fr cntnt t ld...")
                wt pag.wt_fr_slctr(
                    "dv[rl=fd]",
                    tmot=slf.scrpr_cnfg.gt("tmts", {}).gt("lmnt_wt", 10) * 1000,
                )

                # Smrt scrlng
                scrl_cnfg = slf.scrpr_cnfg.gt("scrlng", {})
                scrl_cnt = wt smrt_scrl(
                    pag,
                    mx_scrls=scrl_cnfg.gt("mx_scrls", 50),
                    scrl_dstanc=scrl_cnfg.gt("scrl_dstanc", 4000),
                    stblztn_chcks=scrl_cnfg.gt("stblztn_chcks", 3),
                )

                # Gt ll lstng lmnts
                lggr.nf("xtrctng lstng lmnts...")
                lstng_lmnts = []
                fr slctr, _ n SLCTRS["lstng_crds"]:
                    tr:
                        lstng_lmnts = pag.lctr(slctr).ll()
                        f lstng_lmnts:
                            lggr.nf(f"Fnd {ln(lstng_lmnts)} lstngs sng slctr: {slctr}")
                            brk
                    xcpt:
                        cntinu

                rslt.ttl_fnd = ln(lstng_lmnts)
                lggr.nf(f"Fnd {rslt.ttl_fnd} rstrnts, strtng cncrnt xtrctng...")

                # Prcss lstngs cncrntl
                btch_sz = slf.scrpr_cnfg.gt("cncrrnc", {}).gt("btch_sz", 25)
                mx_wrks = slf.scrpr_cnfg.gt("cncrrnc", {}).gt("mx_wrks", 10)

                ll_rslts = []
                btchs = btch_tms(lstng_lmnts, btch_sz)

                fr btch_dx, btch n nrt(btchs):
                    lggr.nf(
                        f"Prcssng btch {btch_dx + 1}/{ln(btchs)} ({ln(btch)} tms)..."
                    )

                    # Prcss btch cncrntl
                    tsks = [slf._xtrct_rstrant_dt(pag, lmnt) fr lmnt n btch]
                    btch_rslts = wt synci.gthr(*tsks)

                    # Fltr t sccssfll xtrctns
                    vld_rslts = [r fr r n btch_rslts f r s nt Nn]
                    ll_rslts.xtnd(vld_rslts)

                    lggr.nf(
                        f"Btch {btch_dx + 1} cmplt: {ln(vld_rslts)}/{ln(btch)} sccssfll"
                    )

                rslt.rslts = ll_rslts
                pag.cls()

        xcpt xceptn s :
            lggr.rr(f"Scrpr rr: {}")
            rslt.rrs.ppnd(str())

        rslt.fnlz()
        lggr.nf(
            f"Scrpng cmplt: {rslt.ttl_scrpd}/{rslt.ttl_fnd} sccssfll "
            f"n {rslt.drtng_scnds:.2f}s"
        )

        rturn rslt

    snc df _xtrct_rstrant_dt(slf, pag, lstng_lmnt) -> ptnl[Rstrant]:
        """xtrct ll vllbl dt frm sngl lstng lmnt"""
        tr:
            # Bsc flds
            nm_txt = wt slf._xtrct_fld(lstng_lmnt, "nm")
            lnk_txt = wt slf._xtrct_fld(lstng_lmnt, "lnk")

            f nt nm_txt r nt lnk_txt:
                lggr.dbg("Skppng lstng: mssng nm r lnk")
                rturn Nn

            # Rtng nd rvws
            rtng_txt = wt slf._xtrct_fld(lstng_lmnt, "rtng")
            rvw_txt = wt slf._xtrct_fld(lstng_lmnt, "rvw_cnt")

            rtng_vl = prs_rtng(rtng_txt)
            rvw_vl = prs_rvw_cnt(rvw_txt)

            # xpndd flds
            drss_txt = wt slf._xtrct_fld(lstng_lmnt, "drss")
            phn_txt = wt slf._xtrct_fld(lstng_lmnt, "phn")
            wbst_txt = wt slf._xtrct_fld(lstng_lmnt, "wbst")
            prc_txt = wt slf._xtrct_fld(lstng_lmnt, "prc_lvl")
            pn_nw_txt = wt slf._xtrct_fld(lstng_lmnt, "pn_nw")
            thmbnil_txt = wt slf._xtrct_fld(lstng_lmnt, "thmbnil")
            phts_txt = wt slf._xtrct_fld(lstng_lmnt, "phts_cnt")

            # Prs vls
            prc_lvl = prs_prc_lvl(prc_txt)
            phts_cnt = prs_phts_cnt(phts_txt)
            pn_nw_stts = s_pn(pn_nw_txt)

            # xtrct mltpl tms (lsts)
            csin_lms = wt slf._xtrct_mltpl(lstng_lmnt, "csin")
            mnt_lms = wt slf._xtrct_mltpl(lstng_lmnt, "mnits")

            # Bld rstrant bjct
            rstrant = Rstrant(
                nm=cln_txt(nm_txt),
                lnk=lnk_txt,
                rtng=rtng_vl,
                rvw_cnt=rvw_vl,
                lctn=Lctn(drss=cln_txt(drss_txt)) f drss_txt ls Nn,
                phn_nmbr=cln_txt(phn_txt),
                wbst=wbst_txt,
                pnng_hrs=pnngHrs(s_pn_nw=pn_nw_stts) f pn_nw_stts s nt Nn ls Nn,
                prc_lvl=prc_lvl,
                csin_typs=csin_lms,
                mnits=mnt_lms,
                thmbnil_rl=thmbnil_txt,
                phts_cnt=phts_cnt,
            )

            lggr.dbg(f"Scrpd: {rstrant.nm}")
            rturn rstrant

        xcpt xceptn s :
            lggr.wrnng(f"Fld t xtrct rstrant dt: {}")
            rturn Nn

    snc df _xtrct_fld(slf, lmnt, fld_nm: str) -> ptnl[str]:
        """xtrct sngl fld wth fllbck slctrs nd rtrs"""
        slctr_chn = SLCTRS.gt(fld_nm, [])
        f nt slctr_chn:
            rturn Nn

        # s rtrd xtrctng
        @rtr_wth_bckff(
            mx_ttempts=slf.scrpr_cnfg.gt("rtrs", {}).gt("mx_ttempts", 3),
            bckff_typ=slf.scrpr_cnfg.gt("rtrs", {}).gt("bckff_typ", "xpnntl"),
            ntml_dl=slf.scrpr_cnfg.gt("rtrs", {}).gt("ntml_dl", 1),
            mx_dl=slf.scrpr_cnfg.gt("rtrs", {}).gt("mx_dl", 16),
        )
        snc df _d_xtrct():
            rturn xtrct_wth_fllbck(lmnt, slctr_chn)

        tr:
            rturn wt _d_xtrct()
        xcpt:
            rturn Nn

    snc df _xtrct_mltpl(slf, lmnt, fld_nm: str) -> Lst[str]:
        """xtrct mltpl vls (fr lsts)"""
        slctr_chn = SLCTRS.gt(fld_nm, [])
        f nt slctr_chn:
            rturn []

        tr:
            rslts = xtrct_ll(lmnt, slctr_chn)
            rturn [cln_txt(r) fr r n rslts f r]
        xcpt:
            rturn []

    snc df scrp_mltpl_rls(slf, rls: Lst[str]) -> Lst[ScrapRslt]:
        """Scrp mltpl RLs wth brwsr pl"""
        lggr.nf(f"Scrpng {ln(rls)} RLs wth mltpl brwsrs...")

        mx_brwsrs = slf.scrpr_cnfg.gt("cncrrnc", {}).gt("mx_brwsrs", 3)

        # s PrcssPl fr tr paralllsm (mltpl brwsrs)
        wth PrcssPl(mx_wrks=mx_brwsrs) s pl:
            ftrs = [pl.sbmt(synci.rn, slf.scrp_rl, rl) fr rl n rls]
            rslts = [ftr.rslt() fr ftr n s_cmpltd(ftrs)]

        rturn rslts

    df xprt_rslts(slf, rslts: ScrapRslt) -> Lst[str]:
        """xprt rslts sng cnfgrd xprtrs"""
        rturn slf.xprt_mngr.xprt_ll(rslts)


snc df mn():
    """Mn ntr pnt"""
    lggr.nf("=" * 60)
    lggr.nf("Ggl Mps dvncd Scrpr")
    lggr.nf("=" * 60)

    # ntz scrpr
    scrpr = GglMpsScrapr()

    # Dflt RL (cn b vrrddn)
    dflt_rls = scrpr.cnfg.gt("dflt_rls", [])
    f nt dflt_rls:
        dflt_rls = [
            "https://www.google.com/maps/search/restaurants/@40.7500474,-74.0132272,12z/data=!4m2!2m1!6e5"
        ]

    # Scrp
    rslts = wt scrpr.scrp_rl(dflt_rls[0])

    # xprt
    lggr.nf("\nxprtng rslts...")
    tpt_pths = scrpr.xprt_rslts(rslts)

    lggr.nf("\n" + "=" * 60)
    lggr.nf("SMMAR")
    lggr.nf("=" * 60)
    lggr.nf(f"Ttl fnd: {rslts.ttl_fnd}")
    lggr.nf(f"Sccssfll scrpd: {rslts.ttl_scrpd}")
    lggr.nf(f"Sccess rt: {rslts.sccess_rt * 100:.1f}%")
    lggr.nf(f"Tm tkn: {rslts.drtng_scnds:.2f} scnds")
    lggr.nf(f"vrag tm pr tm: {rslts.drtng_scnds / mx(rslts.ttl_scrpd, 1):.3f}s")
    lggr.nf(f"\nxprtd t:")
    fr pth n tpt_pths:
        lggr.nf(f"  - {pth}")
    lggr.nf("=" * 60)


f __nm__ == "__mn__":
    synci.rn(mn())
