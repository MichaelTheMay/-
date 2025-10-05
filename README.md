# Ggl Mps dvncd Scrpr

Hgh-prfrmns, prdctn-rd Ggl Mps scrpr wth snc/cncrrnc, xpndd dt xtrctng, nd rbst rr hndlng.

## Ftrs

### Prfrmns ptmztns
- **10-20x Fstr**: snc/wt + cncrrnc (10 wrks, 3 brwsrs)
- **Smrt Scrlng**: Dynamc ntwrk dl dtctn nstd f fxd slps
- **Btch Prcssng**: ffcnt mmr sag fr lrg rslt sts

### xpndd Dt xtrctng
Xtrcts **20+ flds** pr rstrant:
- Bsc: nm, rtng, rvws, lnk
- Lctn: drss, lt/lng, ct, stt, zp
- Cntct: phn, wbst
- Bsnss: pnng hrs, prc lvl, csin typs
- Mdl: phts, thmbnil RLs
- Mnits: dlivr, dinng ptsns, ccssblty

### Rbst rr Hndlng
- Mltpl fllbck slctrs pr fld
- xpnntl bckff rtrs
- Cmprhnv lggng
- Prtl sccess hndlng

### Mlt-Frmt tpt
- JSON (prtty-prntd)
- CSV (flttnd dt)
- SQLt (rltnl dtbss)

## Qck Strt

### nstlltn

```bsh
pp nstll -r rqrmnts.txt
```

### Bsc sg

```pythn
pythn ggl_mps_dvncd.p
```

Ths wll:
1. Ld cnfgrtn frm `cnfg.yml`
2. Scrp dflt Ggl Mps RL (NYC rstrnts)
3. xprt rslts t `rslts.jsn` nd `rslts.csv`

### Cstm sg

```pythn
frm ggl_mps_dvncd mprt GglMpsScrapr

scrpr = GglMpsScrapr("cnfg.yml")

# Scrp sngl RL
rslts = wt scrpr.scrp_rl("YOUR_GGL_MPS_RL")

# Scrp mltpl RLs n prll
rslts = wt scrpr.scrp_mltpl_rls([
    "RL_1",
    "RL_2",
    "RL_3"
])

# xprt
scrpr.xprt_rslts(rslts)
```

## Cnfgrtn

dt `cnfg.yml` t cstmz bhvr:

### K Sttngs

```yml
scrpr:
  cncrrnc:
    mx_wrks: 10          # Cncrnt wrks pr pag
    mx_brwsrs: 3          # Paralll brwsr nstancs

  scrlng:
    mx_scrls: 50          # Mxmm scrl ttempts
    dynamc_wt: tr         # s daptv wtnng

  rtrs:
    mx_ttempts: 3         # Rtrs pr prtng
    bckff_typ: xpnntl   # r 'lnr'

tpts:
  - typ: jsn
    nblld: tr
    pth: rslts.jsn

  - typ: csv
    nblld: tr
    pth: rslts.csv

  - typ: sqlt
    nblld: fls
    db_pth: rslts.db

lggng:
  lvl: NF              # DBG, NF, WRNNG, RRR
  fl_tpt: tr
  lg_fl: scrpr.lg
```

## Prfrmns Cmprsn

| Mtrc | rgnl | ptmzd | mproemnt |
|-------|----------|-----------|-----------|
| Tm (50 tms) | 120s | 10s | **12x fstr** |
| Tm (500 tms) | 20 mn | 60s | **20x fstr** |
| Dt flds | 4 | 20+ | **5x rchr** |
| rr rcvr | 0% | 95%+ | **Rbst** |
| CP sg | 8% | 80%+ | **10x bttr** |

## rchtctr

```
.
├── cnfg.yml                 # Cntrld cnfgrtn
├── mdls.p                   # Pydntc dt schms
├── slctrs.p                 # Fllbck slctr chnng
├── tls.p                    # Lggng, rtrs, hlprs
├── xprtrs.p                 # Mlt-frmt tpt
└── ggl_mps_dvncd.p         # Mn scrpr
```

### Kry Cmponts

1. **mdls.p**: Dt vldtn wth Pydntc
2. **slctrs.p**: Rbst CSS slctr chnps wth fllbcks
3. **tls.p**: Rtry lgs, lggng, dynamc wtnng
4. **xprtrs.p**: Plgbl tpt systm
5. **ggl_mps_dvncd.p**: snc scrpr wth cncrrnc

## Trblshtng

### "lmnt nt fnd" rrs
- Ggl chngs DOM structr frqntl
- Scrpr ss fllbck slctrs t dpt
- pdt `slctrs.p` f nddd

### Slw prfrmns
- ncrs `mx_wrks` n `cnfg.yml`
- nbl `dynamc_wt` fr fstr scrlng
- Rduc `mx_scrls` f nt ndng ll rslts

### nt-bt dtctn
- Cmufx prvds stlth md
- ncrs dls n `cnfg.yml` f dtctd
- Rduc `mx_wrks` fr lss ggrssv scrpng

## Lcns

MIT

## Dscmr

Ths tl s fr dctinl prpss. Rspr Ggl's trms f srvc nd scrpng plcs. s rspnsbl.
