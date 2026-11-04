import streamlit as st, pandas as pd
from datetime import date
st.set_page_config(page_title="MADYT Hotel – DEMO", layout="wide")
st.error("🧪 DEMO – date de probă, nu afectează aplicația reală")
st.title("MADYT Hotel Anvelope – tipuri de facturare")
COL={"LEASING":"#1f77b4","FIRMA":"#2ca02c","PF":"#ff7f0e"}
def badge(t): return f"<span style='background:{COL[t]};color:white;padding:4px 10px;border-radius:8px;font-weight:bold'>{t}</span>"
S=st.session_state
if "init" not in S:
    S.init=1
    S.clienti=pd.DataFrame([
     dict(ID="C1",Nume="AJB Demo SRL",Tip="FIRMA",CUI="RO000001",Telefon="0700000001"),
     dict(ID="C2",Nume="Ion Popescu (fictiv)",Tip="PF",CUI="",Telefon="0700000002"),
     dict(ID="C3",Nume="Beta Demo SRL",Tip="FIRMA",CUI="RO000003",Telefon="0700000003"),
     dict(ID="C4",Nume="Maria Ionescu (fictiv)",Tip="PF",CUI="",Telefon="0700000004")])
    S.masini=pd.DataFrame([
     dict(Nr="B01DEMO",VIN="DEMOVIN0000000001",Client="C1",Facturare="LEASING",Leasing="Arval"),
     dict(Nr="B02DEMO",VIN="DEMOVIN0000000002",Client="C1",Facturare="FIRMA",Leasing=""),
     dict(Nr="B03DEMO",VIN="DEMOVIN0000000003",Client="C2",Facturare="PF",Leasing=""),
     dict(Nr="B04DEMO",VIN="DEMOVIN0000000004",Client="C3",Facturare="LEASING",Leasing="Hertz"),
     dict(Nr="B05DEMO",VIN="DEMOVIN0000000005",Client="C4",Facturare="PF",Leasing=""),
     dict(Nr="B06DEMO",VIN="DEMOVIN0000000006",Client="C3",Facturare="FIRMA",Leasing="")])
    S.hotel=pd.DataFrame([dict(Nr=n,Pozitie=p,Brand="Goodyear",Dimensiune=d,Sezon=s,DOT="2024",Status="IN_HOTEL")
     for n,d,s in [("B01DEMO","205/55R16","Iarna"),("B02DEMO","225/45R17","Vara"),("B03DEMO","195/65R15","Vara"),("B05DEMO","215/60R16","Iarna"),("B06DEMO","235/55R18","Vara")] for p in range(1,5)])
    S.primite=pd.DataFrame([dict(Nr="B01DEMO",Data="2026-10-20",Brand="Goodyear",Dimensiune="205/55R16",Buc=4,Status="RECEPTIONAT"),
     dict(Nr="B04DEMO",Data="2026-10-22",Brand="Goodyear",Dimensiune="225/50R17",Buc=4,Status="SCHIMBAT")])
    S.servicii=pd.DataFrame([
     dict(ID=1,Data="2026-10-25",Nr="B01DEMO",Tip="Schimb sezon",Descriere="Montaj+echilibrare",Suma=0.0,Facturat="Prin GY"),
     dict(ID=2,Data="2026-10-26",Nr="B02DEMO",Tip="Hotel sezon",Descriere="Depozitare iarna 2026",Suma=200.0,Facturat="NU"),
     dict(ID=3,Data="2026-10-26",Nr="B02DEMO",Tip="Manopera",Descriere="Schimb sezon",Suma=180.0,Facturat="NU"),
     dict(ID=4,Data="2026-10-27",Nr="B03DEMO",Tip="Vanzare anvelope",Descriere="4x 195/65R15 iarna",Suma=1600.0,Facturat="NU"),
     dict(ID=5,Data="2026-10-28",Nr="B05DEMO",Tip="Hotel sezon",Descriere="Depozitare vara 2026",Suma=150.0,Facturat="DA"),
     dict(ID=6,Data="2026-10-29",Nr="B04DEMO",Tip="Schimb sezon",Descriere="Montaj anvelope noi",Suma=0.0,Facturat="Prin GY")])
def show(df,msg):
    if len(df): st.dataframe(df,hide_index=True)
    else: st.info(msg)
def full():
    m=S.masini.merge(S.clienti[["ID","Nume","Telefon"]],left_on="Client",right_on="ID",how="left").drop(columns="ID")
    return m
t=st.tabs(["🔎 Căutare","📊 Rapoarte pe tip","🏢 Raport client","🧾 De facturat","➕ Adăugare"])
with t[0]:
    q=st.text_input("Nr. auto sau VIN").strip().upper()
    if q:
        m=full(); r=m[(m.Nr==q)|(m.VIN==q)]
        if r.empty: st.warning("Nu am găsit mașina.")
        for _,c in r.iterrows():
            st.markdown(f"### {c.Nr} · VIN {c.VIN} &nbsp; {badge(c.Facturare)}",unsafe_allow_html=True)
            st.write(f"**Client:** {c.Nume} · tel. {c.Telefon}"+(f" · **Leasing:** {c.Leasing} (facturare prin GY Fleet)" if c.Facturare=="LEASING" else " · facturare directă Madyt"))
            a,b=st.columns(2)
            with a: st.markdown("**🛞 Ce are acum în hotel**"); h=S.hotel[(S.hotel.Nr==c.Nr)&(S.hotel.Status=="IN_HOTEL")]; show(h,"Nimic în hotel")
            with b: st.markdown("**📦 Anvelope primite**"); p=S.primite[S.primite.Nr==c.Nr]; show(p,"Nimic primit")
            st.markdown("**Istoric servicii**"); st.dataframe(S.servicii[S.servicii.Nr==c.Nr],hide_index=True)
with t[1]:
    tip=st.radio("Tip",["LEASING","FIRMA","PF"],horizontal=True)
    nrs=full().query("Facturare==@tip")
    st.markdown(badge(tip),unsafe_allow_html=True)
    st.subheader("În hotel"); st.dataframe(S.hotel[S.hotel.Nr.isin(nrs.Nr)&(S.hotel.Status=="IN_HOTEL")].merge(nrs[["Nr","Nume"]],on="Nr"),hide_index=True)
    st.subheader("Schimburi efectuate"); st.dataframe(S.servicii[S.servicii.Nr.isin(nrs.Nr)&S.servicii.Tip.str.startswith("Schimb")],hide_index=True)
    st.subheader("De facturat")
    if tip=="LEASING": st.info("Leasing: se facturează prin GY Fleet după aprobare (fluxul existent).")
    else:
        d=S.servicii[S.servicii.Nr.isin(nrs.Nr)&(S.servicii.Facturat=="NU")]; st.dataframe(d,hide_index=True); st.metric("Total nefacturat (lei)",f"{d.Suma.sum():.2f}")
with t[2]:
    cl=st.selectbox("Client",S.clienti.Nume.tolist())
    cid=S.clienti[S.clienti.Nume==cl].ID.iloc[0]; m=S.masini[S.masini.Client==cid]
    for tp,lbl in [("LEASING","Mașini în leasing"),("DIRECT","Mașini directe")]:
        x=m[m.Facturare=="LEASING"] if tp=="LEASING" else m[m.Facturare!="LEASING"]
        st.subheader(f"{lbl} ({len(x)})"); st.dataframe(x,hide_index=True)
        st.caption(f"Anvelope în hotel: {int((S.hotel.Nr.isin(x.Nr)&(S.hotel.Status=='IN_HOTEL')).sum())} buc.")
with t[3]:
    direct=full().query("Facturare!='LEASING'")
    d=S.servicii[S.servicii.Nr.isin(direct.Nr)&(S.servicii.Facturat=="NU")].merge(direct[["Nr","Nume","Facturare"]],on="Nr")
    st.dataframe(d,hide_index=True); st.metric("Total (lei)",f"{d.Suma.sum():.2f}")
    if len(d):
        sel=st.multiselect("Marchează ca facturat (ID)",d.ID.tolist())
        if st.button("✅ Marchează facturat") and sel:
            S.servicii.loc[S.servicii.ID.isin(sel),"Facturat"]="DA"; st.rerun()
with t[4]:
    c1,c2,c3=st.columns(3)
    with c1, st.form("fc"):
        st.markdown("**Client nou**"); n=st.text_input("Nume"); tp=st.selectbox("Tip",["FIRMA","PF"]); cui=st.text_input("CUI"); tel=st.text_input("Telefon")
        if st.form_submit_button("Adaugă client") and n:
            S.clienti.loc[len(S.clienti)]=dict(ID=f"C{len(S.clienti)+1}",Nume=n,Tip=tp,CUI=cui,Telefon=tel); st.success("Adăugat")
    with c2, st.form("fm"):
        st.markdown("**Mașină nouă**"); nr=st.text_input("Nr. auto").upper(); vin=st.text_input("VIN").upper()
        cl=st.selectbox("Client",S.clienti.Nume.tolist()); fz=st.selectbox("Facturare",["LEASING","FIRMA","PF"]); ls=st.selectbox("Firmă leasing",["","Arval","Hertz","Autotehnica Fleet"])
        if st.form_submit_button("Adaugă mașină") and nr:
            S.masini.loc[len(S.masini)]=dict(Nr=nr,VIN=vin,Client=S.clienti[S.clienti.Nume==cl].ID.iloc[0],Facturare=fz,Leasing=ls if fz=="LEASING" else ""); st.success("Adăugată")
    with c3, st.form("fs"):
        st.markdown("**Serviciu / vânzare**"); nr2=st.selectbox("Mașină",S.masini.Nr.tolist()); tps=st.selectbox("Tip",["Hotel sezon","Manopera","Vanzare anvelope","Schimb sezon"]); ds=st.text_input("Descriere"); sm=st.number_input("Sumă (lei)",0.0,step=10.0)
        if st.form_submit_button("Adaugă"):
            lea=S.masini[S.masini.Nr==nr2].Facturare.iloc[0]=="LEASING"
            S.servicii.loc[len(S.servicii)]=dict(ID=int(S.servicii.ID.max())+1,Data=str(date.today()),Nr=nr2,Tip=tps,Descriere=ds,Suma=sm,Facturat="Prin GY" if lea else "NU"); st.success("Adăugat")
