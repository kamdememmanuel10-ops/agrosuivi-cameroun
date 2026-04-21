import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.db import get_all_fiches, get_climat_region
from utils.const import ( COORDS_REGIONS, COULEURS_REGIONS, CULTURES_PAR_REGION, ZONES_AGROECO, MOIS_NOMS, REGIONS)
CAMEROON_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {"type":"Feature","id":"Adamaoua","properties":{"region":"Adamaoua"},
         "geometry":{"type":"Polygon","coordinates":[[[11.5,6.5],[15.0,6.5],[15.0,8.5],[13.5,8.5],[12.5,8.0],[11.5,7.5],[11.5,6.5]]]}},
        {"type":"Feature","id":"Centre","properties":{"region":"Centre"},
         "geometry":{"type":"Polygon","coordinates":[[[10.0,3.0],[12.5,3.0],[12.5,5.5],[11.5,6.5],[11.0,6.0],[10.5,5.0],[10.0,4.0],[10.0,3.0]]]}},
        {"type":"Feature","id":"Est","properties":{"region":"Est"},
         "geometry":{"type":"Polygon","coordinates":[[[12.5,3.0],[16.2,3.0],[16.2,6.5],[15.0,6.5],[11.5,6.5],[12.5,5.5],[12.5,3.0]]]}},
        {"type":"Feature","id":"Extreme-Nord","properties":{"region":"Extrême-Nord"},
         "geometry":{"type":"Polygon","coordinates":[[[13.5,10.0],[15.2,10.0],[15.2,13.0],[14.0,13.0],[13.0,12.5],[12.5,11.5],[13.0,10.5],[13.5,10.0]]]}},
        {"type":"Feature","id":"Littoral","properties":{"region":"Littoral"},
         "geometry":{"type":"Polygon","coordinates":[[[9.2,3.5],[10.5,3.5],[10.5,5.0],[9.8,5.2],[9.2,4.8],[8.8,4.2],[9.2,3.5]]]}},
        {"type":"Feature","id":"Nord","properties":{"region":"Nord"},
         "geometry":{"type":"Polygon","coordinates":[[[12.5,8.5],[15.0,8.5],[15.2,10.0],[13.5,10.0],[13.0,10.5],[12.5,10.0],[12.0,9.0],[12.5,8.5]]]}},
        {"type":"Feature","id":"Nord-Ouest","properties":{"region":"Nord-Ouest"},
         "geometry":{"type":"Polygon","coordinates":[[[9.5,5.5],[11.0,5.5],[11.0,7.0],[10.0,7.0],[9.2,6.5],[9.0,5.8],[9.5,5.5]]]}},
        {"type":"Feature","id":"Ouest","properties":{"region":"Ouest"},
         "geometry":{"type":"Polygon","coordinates":[[[9.8,5.0],[11.0,5.0],[11.0,5.5],[9.5,5.5],[9.0,5.3],[9.2,4.8],[9.8,5.0]]]}},
        {"type":"Feature","id":"Sud","properties":{"region":"Sud"},
         "geometry":{"type":"Polygon","coordinates":[[[10.0,2.0],[12.5,2.0],[12.5,3.0],[10.0,3.0],[9.5,3.2],[9.5,2.5],[10.0,2.0]]]}},
        {"type":"Feature","id":"Sud-Ouest","properties":{"region":"Sud-Ouest"},
         "geometry":{"type":"Polygon","coordinates":[[[8.5,3.8],[9.2,3.5],[9.5,3.2],[9.5,4.5],[9.0,5.3],[8.5,5.0],[8.3,4.5],[8.5,3.8]]]}},
    ]
}
INFO_REGIONS = {
    "Adamaoua":    {"chef_lieu":"Ngaoundere","pop":"1.2M","pluie":"1200-1500mm","temp":"18-26C","altitude":"900-1500m","cultures_top":["Mais","Sorgho","Manioc","Haricot"],"richesse":"Elevage bovin"},
    "Centre":      {"chef_lieu":"Yaounde (Capitale)","pop":"4.1M","pluie":"1500-2000mm","temp":"22-29C","altitude":"300-900m","cultures_top":["Mais","Manioc","Cacao","Plantain","Tomate"],"richesse":"Cacao, maraicher"},
    "Est":         {"chef_lieu":"Bertoua","pop":"0.9M","pluie":"1500-2000mm","temp":"23-29C","altitude":"400-900m","cultures_top":["Manioc","Plantain","Mais","Cacao"],"richesse":"Foret tropicale"},
    "Extreme-Nord":{"chef_lieu":"Maroua","pop":"4.2M","pluie":"300-700mm","temp":"26-42C","altitude":"300-600m","cultures_top":["Mil","Sorgho","Arachide","Coton"],"richesse":"Coton, elevage"},
    "Extrême-Nord":{"chef_lieu":"Maroua","pop":"4.2M","pluie":"300-700mm","temp":"26-42C","altitude":"300-600m","cultures_top":["Mil","Sorgho","Arachide","Coton"],"richesse":"Coton, elevage"},
    "Littoral":    {"chef_lieu":"Douala (Cap. eco.)","pop":"3.8M","pluie":"2000-4000mm","temp":"24-32C","altitude":"0-200m","cultures_top":["Plantain","Palmier","Mais","Cacao"],"richesse":"Port, palmier"},
    "Nord":        {"chef_lieu":"Garoua","pop":"2.3M","pluie":"800-1200mm","temp":"22-38C","altitude":"200-500m","cultures_top":["Sorgho","Mil","Arachide","Coton"],"richesse":"Coton, riz"},
    "Nord-Ouest":  {"chef_lieu":"Bamenda","pop":"1.8M","pluie":"1700-2500mm","temp":"15-24C","altitude":"900-2500m","cultures_top":["Cafe Arabica","Mais","Pomme de terre"],"richesse":"Cafe arabica"},
    "Ouest":       {"chef_lieu":"Bafoussam","pop":"2.0M","pluie":"1500-2200mm","temp":"16-26C","altitude":"1000-2200m","cultures_top":["Cafe","Mais","Plantain","Pomme de terre"],"richesse":"Cafe arabica"},
    "Sud":         {"chef_lieu":"Ebolowa","pop":"0.7M","pluie":"1500-2200mm","temp":"23-28C","altitude":"500-900m","cultures_top":["Manioc","Plantain","Cacao","Mais"],"richesse":"Cacao, foret"},
    "Sud-Ouest":   {"chef_lieu":"Buea","pop":"1.4M","pluie":"3000-10000mm","temp":"22-28C","altitude":"0-4095m","cultures_top":["Plantain","Palmier","Cacao","Hevea"],"richesse":"Plantations industr."},
}

COULEURS_ZONES = {
    "Guinéenne forestière":     "#1b5e20",
    "Bimodale subéquatoriale":  "#43a047",
    "Hautes terres":            "#f39c12",
    "Soudano-sahélienne":       "#e67e22",
    "Sahélienne":               "#c0392b",
}
DESC_ZONES = {
    "Guinéenne forestière": {
        "regions":"Sud, Est, Sud-Ouest","pluie":"1500-10000mm/an","temp":"22-30C",
        "saisons":"4 saisons","sols":"Ferrallitiques tres fertiles",
        "cultures":"Cacao, Cafe Robusta, Plantain, Manioc, Palmier, Hevea",
        "desc":"Zone de foret dense tropicale. Humidite permanente. Sol tres fertile. Biodiversite maximale.","icone":"Foret dense"
    },
    "Bimodale subéquatoriale": {
        "regions":"Centre, Littoral","pluie":"1400-2000mm/an","temp":"23-29C",
        "saisons":"4 saisons bien marquees","sols":"Ferrallitiques a hydromorphes",
        "cultures":"Mais, Manioc, Plantain, Cacao, Tomate, Legumes",
        "desc":"Zone des capitales (Yaounde, Douala). Agriculture diversifiee et intensive.","icone":"Savane arboree"
    },
    "Hautes terres": {
        "regions":"Ouest, Nord-Ouest","pluie":"1500-2500mm/an","temp":"15-26C",
        "saisons":"2 saisons","sols":"Volcaniques noirs tres fertiles (andosols)",
        "cultures":"Cafe Arabica, Mais, Pomme de terre, Haricot, Choux",
        "desc":"Plateaux et montagnes. Sols volcaniques d'exception. Cafe arabica repute.","icone":"Montagnes"
    },
    "Soudano-sahélienne": {
        "regions":"Adamaoua, Nord","pluie":"800-1500mm/an","temp":"20-38C",
        "saisons":"2 saisons","sols":"Ferrugineux tropicaux, moyennement fertiles",
        "cultures":"Sorgho, Mil, Arachide, Coton, Riz (bas-fonds), Mais",
        "desc":"Savane arboree. Elevage bovin transhumant important. Coton = culture de rente principale.","icone":"Savane"
    },
    "Sahélienne": {
        "regions":"Extreme-Nord","pluie":"300-700mm/an","temp":"25-42C",
        "saisons":"1 courte saison (3-4 mois)","sols":"Sableux a argileux (harde)",
        "cultures":"Mil, Sorgho, Arachide, Coton, Sesame, Oignon",
        "desc":"Zone aride. Agriculture tres vulnerable aux aleas climatiques. Irrigation vitale.","icone":"Semi-aride"
    },
}
def show():
    st.markdown("""
    <div class="main-header">
        <div>
            <h1>Carte Interactive du Cameroun</h1>
            <p>Visualisation geographique des cultures, du climat et des performances agricoles</p>
        </div>
        <div class="badge-live">10 Regions - Donnees temps reel</div>
    </div>
    """, unsafe_allow_html=True)
    df = get_all_fiches()
    tab1, tab2, tab3, tab4 = st.tabs([
        "Carte choroplèthe",
        "Exploitations GPS",
        "Profils climatiques",
        "Zones agro-écologiques"
    ])
    with tab1:
        indicateur = st.radio(
            "Indicateur a visualiser",
            ["Rendement moyen (kg/ha)","Nombre de fiches","Superficie totale (ha)",
             "Pct Engrais","Pct Irrigation","Revenu moyen (FCFA)"],
            horizontal=True
        )
        if not df.empty:
            agg = df.groupby("region").agg(
                rdmt_moy   =("rendement_kg_ha","mean"),
                nb_fiches  =("rendement_kg_ha","count"),
                superficie =("superficie_ha","sum"),
                pct_engrais=("type_engrais", lambda x:(x!="Aucun").mean()*100),
                pct_irr    =("irrigation",   lambda x:(x=="Oui").mean()*100),
                revenu_moy =("revenu_estime","mean"),
            ).reset_index()
        else:
            agg = pd.DataFrame({
                "region":    list(COORDS_REGIONS.keys()),
                "rdmt_moy":  [1400,1600,1200,850,2100,950,1800,2200,1350,2800],
                "nb_fiches": [8,15,6,12,18,9,7,11,5,10],
                "superficie":[45,120,38,80,95,60,42,75,30,55],
                "pct_engrais":[55,72,40,30,80,45,65,78,38,85],
                "pct_irr":   [20,35,15,60,45,55,25,30,18,40],
                "revenu_moy":[180000,320000,150000,95000,450000,120000,280000,350000,130000,520000],
            })
        col_map = {
            "Rendement moyen (kg/ha)":("rdmt_moy","Greens","kg/ha"),
            "Nombre de fiches":       ("nb_fiches","Blues","fiches"),
            "Superficie totale (ha)": ("superficie","YlGn","ha"),
            "Pct Engrais":            ("pct_engrais","RdYlGn","%"),
            "Pct Irrigation":         ("pct_irr","Blues","%"),
            "Revenu moyen (FCFA)":    ("revenu_moy","Oranges","FCFA"),
        }
        val_col, colorscale, unite = col_map[indicateur]
        val_dict = dict(zip(agg["region"], agg[val_col]))
        # Labels sur la carte
        lats  = [c["lat"]  for c in COORDS_REGIONS.values()]
        lons  = [c["lon"]  for c in COORDS_REGIONS.values()]
        regs  = list(COORDS_REGIONS.keys())
        texts = [f"{r}<br>{val_dict.get(r,0):,.0f} {unite}" for r in regs]
        hovers= [
            f"<b>{r}</b><br>"
            f"Chef-lieu: {INFO_REGIONS.get(r,{}).get('chef_lieu','')}<br>"
            f"Population: {INFO_REGIONS.get(r,{}).get('pop','')}<br>"
            f"Pluie: {INFO_REGIONS.get(r,{}).get('pluie','')}<br>"
            f"Temperature: {INFO_REGIONS.get(r,{}).get('temp','')}<br>"
            f"Cultures: {', '.join(INFO_REGIONS.get(r,{}).get('cultures_top',[])[:3])}<br>"
            f"{indicateur}: <b>{val_dict.get(r,0):,.0f} {unite}</b>"
            for r in regs
        ]
        fig = go.Figure()
        # Bulles par région colorées par valeur
        fig.add_trace(go.Scattermapbox(
            lat=lats, lon=lons,
            mode="markers+text",
            marker=dict(
                size=[max(20, min(60, val_dict.get(r,0)/max(val_dict.values() or [1])*60)) for r in regs],
                color=[val_dict.get(r,0) for r in regs],
                colorscale=colorscale,
                showscale=True,
                colorbar=dict(title=unite, thickness=14, len=0.7),
                opacity=0.82,
            ),
            text=[r.replace("Extrême-","EN-") for r in regs],
            textposition="top center",
            textfont=dict(size=10, color="white"),
            hovertext=hovers,
            hoverinfo="text",
            name=indicateur,
        ))
        fig.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                zoom=4.8,
                center={"lat":5.8,"lon":12.3},
            ),
            height=540,
            margin=dict(t=10,b=0,l=0,r=0),
        )
        st.plotly_chart(fig, use_container_width=True)
        # Classement
        col_l, col_r = st.columns([2,1])
        with col_l:
            st.markdown("**Fiche détaillée région**")
            reg_det = st.selectbox("Region", list(INFO_REGIONS.keys())[:10], key="det2")
            info = INFO_REGIONS.get(reg_det, {})
            d1,d2,d3,d4 = st.columns(4)
            pairs = [
                (d1,"Chef-lieu",info.get("chef_lieu","—")),
                (d2,"Population",info.get("pop","—")),
                (d3,"Temperature",info.get("temp","—")),
                (d4,"Pluviometrie",info.get("pluie","—")),
            ]
            for col,label,val in pairs:
                with col:
                    st.markdown(f"""
                    <div style='background:white;border-radius:10px;padding:.8rem;
                                box-shadow:0 1px 6px rgba(0,0,0,.06);border-top:3px solid #43a047;'>
                        <div style='font-size:.7rem;color:#78909c;text-transform:uppercase;font-weight:700;'>{label}</div>
                        <div style='font-size:.95rem;font-weight:800;color:#1b5e20;margin-top:.2rem;'>{val}</div>
                    </div>
                    """, unsafe_allow_html=True)
            cult_str = " · ".join(info.get("cultures_top",[]))
            st.markdown(f"""
            <div style='background:#e8f5e9;border-radius:10px;padding:.9rem 1.2rem;
                        margin-top:.7rem;border:1px solid #a5d6a7;'>
                <b style='color:#1b5e20;'>Cultures: {cult_str}</b><br>
                <span style='font-size:.85rem;color:#37474f;'>
                    Altitude: {info.get("altitude","—")} | Richesse: {info.get("richesse","—")}
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col_r:
            st.markdown("**Classement regions**")
            top = agg.sort_values(val_col, ascending=False)[["region",val_col]]
            for i,(_, row) in enumerate(top.iterrows()):
                medals = [""," "," "] + [" "]
                coul   = COULEURS_REGIONS.get(row["region"],"#43a047")
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;padding:.35rem .7rem;
                            margin-bottom:3px;border-radius:7px;background:white;
                            border-left:3px solid {coul};box-shadow:0 1px 4px rgba(0,0,0,.05);'>
                    <span style='font-size:.8rem;font-weight:700;color:#1b5e20;'>
                        {medals[i] if i < len(medals) else "🥇"} {row["region"]}
                    </span>
                    <span style='font-size:.78rem;color:#546e7a;'>{row[val_col]:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
    with tab2:
        if df.empty:
            st.info("Saisissez des fiches avec coordonnees GPS pour afficher la carte.")
            return
        df_gps = df.dropna(subset=["coordonnees_lat","coordonnees_lon"])
        df_gps = df_gps[
            df_gps["coordonnees_lat"].between(1.6,13.1) &
            df_gps["coordonnees_lon"].between(8.3,16.2)
        ]
        c1,c2 = st.columns([1,3])
        with c1:
            couleur_opt = st.radio("Colorier par",["culture","region","type_engrais","irrigation"])
            taille_opt  = st.radio("Taille par",  ["rendement_kg_ha","superficie_ha","revenu_estime"])
            style_map   = st.selectbox("Style carte",
                ["carto-positron","open-street-map","carto-darkmatter"])
            filtre_cult = st.multiselect("Cultures", sorted(df_gps["culture"].unique()),
                                         default=list(sorted(df_gps["culture"].unique()))[:5])
            filtre_reg  = st.multiselect("Regions",  sorted(df_gps["region"].unique()),
                                         default=list(sorted(df_gps["region"].unique())))
        with c2:
            dm = df_gps[df_gps["culture"].isin(filtre_cult) & df_gps["region"].isin(filtre_reg)]
            if dm.empty:
                st.warning("Aucun point apres filtrage.")
            else:
                fig2 = px.scatter_mapbox(
                    dm, lat="coordonnees_lat", lon="coordonnees_lon",
                    color=couleur_opt, size=taille_opt, size_max=20,
                    hover_name="nom_exploitant",
                    hover_data={"culture":True,"region":True,
                                "rendement_kg_ha":":.0f","superficie_ha":":.2f",
                                "coordonnees_lat":False,"coordonnees_lon":False},
                    color_discrete_map=COULEURS_REGIONS if couleur_opt=="region" else None,
                    color_discrete_sequence=px.colors.qualitative.G10,
                    zoom=5, center={"lat":5.8,"lon":12.3},
                    mapbox_style=style_map, height=500,
                )
                fig2.update_layout(margin=dict(t=10,b=0,l=0,r=0),
                    legend=dict(bgcolor="rgba(255,255,255,.85)",
                                bordercolor="#a5d6a7",borderwidth=1))
                st.plotly_chart(fig2, use_container_width=True)
                m1,m2,m3,m4 = st.columns(4)
                with m1: st.metric("Points GPS", len(dm))
                with m2: st.metric("Rdmt moyen", f"{dm['rendement_kg_ha'].mean():,.0f} kg/ha")
                with m3: st.metric("Cultures", dm["culture"].nunique())
                with m4: st.metric("Regions",  dm["region"].nunique())
    with tab3:
        c1,c2 = st.columns([1,2])
        with c1:
            reg_clim = st.selectbox("Region", list(COORDS_REGIONS.keys()), key="t3r")
            graphique = st.radio("Graphique",["Pluviometrie","Temperatures","Humidite","Vue complete"])
            comp2 = st.checkbox("Comparer une 2e region")
            reg2  = None
            if comp2:
                reg2 = st.selectbox("Region 2",[r for r in COORDS_REGIONS if r!=reg_clim])
        with c2:
            df_c  = get_climat_region(reg_clim)
            if df_c.empty:
                df_c = pd.DataFrame({"mois":range(1,13),"pluie_mm":[20,25,80,140,185,155,75,90,210,280,110,30],
                    "temp_min_c":[18,19,20,20,19,18,17,17,18,18,18,18],
                    "temp_max_c":[30,31,29,29,27,26,25,25,27,27,28,29],
                    "humidite_pct":[68,65,78,82,85,88,86,85,88,90,83,72],
                    "type_saison":["PS","GS","GP","GP","GP","GP","PP","PP","PP","PP","PS","PS"]})
            if graphique == "Pluviometrie":
                fig_r = go.Figure()
                fig_r.add_trace(go.Bar(x=MOIS_NOMS, y=df_c["pluie_mm"], name=reg_clim,
                    marker_color=["#0d47a1" if p>200 else "#1976d2" if p>100 else "#64b5f6" if p>30 else "#e3f2fd" for p in df_c["pluie_mm"]],
                    text=df_c["pluie_mm"].round(0), textposition="outside"))
                if comp2 and reg2:
                    df_c2 = get_climat_region(reg2)
                    if not df_c2.empty:
                        fig_r.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c2["pluie_mm"],
                            name=reg2, line=dict(color="#43a047",width=2), mode="lines+markers"))
                fig_r.update_layout(title=f"Pluviometrie — {reg_clim}", yaxis_title="mm",
                    height=380, template="plotly_white", margin=dict(t=50,b=20,l=20,r=20))
                st.plotly_chart(fig_r, use_container_width=True)
            elif graphique == "Temperatures":
                fig_t = go.Figure()
                fig_t.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c["temp_max_c"],
                    fill="tonexty", name="T Max", line=dict(color="#ef5350",width=2),
                    fillcolor="rgba(239,83,80,.15)"))
                fig_t.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c["temp_min_c"],
                    fill="tozeroy", name="T Min", line=dict(color="#42a5f5",width=2),
                    fillcolor="rgba(66,165,245,.15)"))
                fig_t.update_layout(title=f"Temperatures — {reg_clim}", yaxis_title="C",
                    height=380, template="plotly_white", margin=dict(t=50,b=20,l=20,r=20))
                st.plotly_chart(fig_t, use_container_width=True),
            elif graphique == "Humidite":
                fig_h = px.area(x=MOIS_NOMS, y=df_c["humidite_pct"],
                    color_discrete_sequence=["#26c6da"], template="plotly_white",
                    title=f"Humidite — {reg_clim}",
                    labels={"x":"Mois","y":"Humidite (%)"})
                fig_h.update_layout(height=380, margin=dict(t=50,b=20,l=20,r=20),
                    yaxis=dict(range=[0,100],ticksuffix="%"))
                st.plotly_chart(fig_h, use_container_width=True)
            else:  # Vue complete
                fig_comb = make_subplots(rows=2,cols=2,
                    subplot_titles=("Pluie (mm)","Temperatures (C)","Humidite (%)","Repartition saisons"),
                    vertical_spacing=0.14, horizontal_spacing=0.08)
                fig_comb.add_trace(go.Bar(x=MOIS_NOMS, y=df_c["pluie_mm"],
                    marker_color="#1976d2", showlegend=False), row=1, col=1)
                fig_comb.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c["temp_max_c"],
                    line=dict(color="#ef5350"), name="TMax"), row=1, col=2)
                fig_comb.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c["temp_min_c"],
                    line=dict(color="#42a5f5"), name="TMin"), row=1, col=2)
                fig_comb.add_trace(go.Scatter(x=MOIS_NOMS, y=df_c["humidite_pct"],
                    fill="tozeroy", line=dict(color="#26c6da"), showlegend=False), row=2, col=1)
                sais_colors={"Grande saison des pluies":"#1565c0","Petite saison des pluies":"#42a5f5",
                             "Grande saison seche":"#e65100","Petite saison seche":"#ffb74d","GP":"#1565c0","PP":"#42a5f5","GS":"#e65100","PS":"#ffb74d"}
                sais_vals = df_c["type_saison"].tolist() if "type_saison" in df_c.columns else [""]*12
                for i,(m,s) in enumerate(zip(MOIS_NOMS,sais_vals)):
                    fig_comb.add_trace(go.Bar(x=[m],y=[1],marker_color=sais_colors.get(str(s),"#78909c"),
                        showlegend=False,hovertext=str(s)), row=2, col=2)
                fig_comb.update_layout(height=480, template="plotly_white",
                    title_text=f"Vue climatique complete — {reg_clim}",
                    margin=dict(t=60,b=20,l=20,r=20))
                st.plotly_chart(fig_comb, use_container_width=True)
        # Calendrier cultural
        st.markdown("---")
        st.markdown(f"**Calendrier cultural — {reg_clim}**")
        cal_data = {
            "Maïs":    ["","","S","S","","","","","","R","R",""],
            "Manioc":  ["S","S","","","","","","","","","R","R"],
            "Cacao":   ["","","","","","","","","","R","R",""],
            "Plantain":["S","","","","","","","","R","R","",""],
            "Sorgho":  ["","","","","S","S","","","R","R","",""],
            "Tomate":  ["","","","S","S","","R","","","","S","S"],
            "Arachide":["","","","S","S","","","R","","","",""],
            "Café":    ["","","","","","","","","","R","R",""],
        }
        leg = {"S":"Semis","R":" Recolte","":"—"}
        cultures_reg = CULTURES_PAR_REGION.get(reg_clim, list(cal_data.keys()))[:5]
        rows = [[c]+[leg.get(cal_data.get(c,[""]*(i+1))[i],"—") for i in range(12)] for c in cultures_reg if c in cal_data]
        if rows:
            df_cal = pd.DataFrame(rows, columns=["Culture"]+MOIS_NOMS)
            st.dataframe(df_cal, use_container_width=True, hide_index=True)
    with tab4:
        zones_rows = []
        for zone, regs in ZONES_AGROECO.items():
            for r in regs:
                c = COORDS_REGIONS.get(r,{})
                info_r = INFO_REGIONS.get(r,{})
                zones_rows.append({
                    "zone":r,"region":r,"lat":c.get("lat",5),"lon":c.get("lon",12),
                    "cultures":", ".join(info_r.get("cultures_top",[])[:3]),
                    "zone_eco":zone,
                })
        df_z = pd.DataFrame(zones_rows)
        fig_z = px.scatter_mapbox(
            df_z, lat="lat", lon="lon",
            color="zone_eco", text="region",
            color_discrete_map=COULEURS_ZONES,
            size=[35]*len(df_z), size_max=35,
            hover_name="region",
            hover_data={"zone_eco":True,"cultures":True,"lat":False,"lon":False},
            zoom=4.5, center={"lat":5.8,"lon":12.3},
            mapbox_style="carto-positron", height=460,
        )
        fig_z.update_traces(textposition="top center", textfont=dict(size=10,color="#1b5e20"))
        fig_z.update_layout(margin=dict(t=10,b=0,l=0,r=0),
            legend=dict(title="Zone agro-ecologique",orientation="h",y=-0.1,
                        bgcolor="rgba(255,255,255,.85)",bordercolor="#a5d6a7",borderwidth=1))
        st.plotly_chart(fig_z, use_container_width=True)
        st.markdown("---")
        st.markdown("**Caracteristiques des zones agro-ecologiques**")
        for zone_name, info_z in DESC_ZONES.items():
            coul = COULEURS_ZONES.get(zone_name,"#43a047")
            with st.expander(f"{zone_name} — {info_z['regions']}"):
                za,zb,zc = st.columns(3)
                with za:
                    st.markdown(f"**Pluviometrie:** {info_z['pluie']}\n\n**Temperature:** {info_z['temp']}")
                with zb:
                    st.markdown(f"**Saisons:** {info_z['saisons']}\n\n**Sols:** {info_z['sols']}")
                with zc:
                    st.markdown(f"**Cultures:** {info_z['cultures']}")
                st.markdown(f"""
                <div style='background:{coul}22;border-left:4px solid {coul};border-radius:8px;
                            padding:.8rem 1.2rem;margin-top:.5rem;color:#37474f;font-size:.9rem;'>
                    {info_z['desc']}
                </div>""", unsafe_allow_html=True)
        # Comparaison par zone si données dispo
        full_df = get_all_fiches()
        if not full_df.empty:
            reg_to_zone = {r:z for z,regs in ZONES_AGROECO.items() for r in regs}
            full_df["zone_eco"] = full_df["region"].map(reg_to_zone).fillna("Autre")
            comp_z = full_df.groupby("zone_eco").agg(
                Nb=("rendement_kg_ha","count"),
                Rdmt_moy=("rendement_kg_ha","mean"),
                Superficie=("superficie_ha","sum"),
                Pct_eng=("type_engrais", lambda x:(x!="Aucun").mean()*100),
            ).reset_index()
            comp_z.columns = ["Zone","Nb fiches","Rdmt moyen (kg/ha)","Superficie (ha)","Pct Engrais"]
            for col in ["Rdmt moyen (kg/ha)","Superficie (ha)","Pct Engrais"]:
                comp_z[col] = comp_z[col].round(1)
            st.markdown("**Comparaison performances par zone agro-ecologique**")
            st.dataframe(comp_z, use_container_width=True, hide_index=True)