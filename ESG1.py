import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configurazione pagina
st.set_page_config(
    page_title="GreenInvest+",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stili CSS personalizzati
def local_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E8449;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2E86C1;
            margin-top: 2rem;
        }
        .green-alert {
            background-color: #D5F5E3;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #1E8449;
        }
        .red-alert {
            background-color: #FADBD8;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #C0392B;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #7F8C8D;
            font-size: 0.8rem;
        }
        .highlight {
            background-color: #FEF9E7;
            padding: 0.2rem;
            border-radius: 0.2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Funzione per generare dati ESG simulati
def generate_esg_data():
    # Creazione di 5 strumenti finanziari simulati
    products = [
        "EcoGreen ETF", 
        "Sustainability Fund", 
        "Blue Ocean Bond", 
        "Carbon Zero Index", 
        "Future Energy Trust"
    ]
    
    esg_scores = [85, 72, 93, 65, 78]
    co2_emissions = [120, 200, 50, 180, 150]  # Tonnellate di CO2 (scope 1-2-3)
    green_activities = [25, 65, 82, 60, 45]   # Percentuale di attività green
    
    # Calcola greenwashing flag (ESG score > 80 ma % attività green < 30%)
    greenwashing = [(score > 80 and green < 30) for score, green in zip(esg_scores, green_activities)]
    
    # Creazione del DataFrame
    data = pd.DataFrame({
        'product': products,
        'esg_score': esg_scores,
        'co2_emissions': co2_emissions,
        'green_activities': green_activities,
        'greenwashing_flag': greenwashing
    })
    
    return data

# Funzione per visualizzare ESG score con barra colorata
def display_esg_score(score):
    if score >= 80:
        color = "green"
    elif score >= 60:
        color = "orange"
    else:
        color = "red"
    
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <span style="font-weight: bold;">ESG Score: {score}/100</span>
        <div style="background-color: #f0f0f0; border-radius: 5px; height: 20px; width: 100%;">
            <div style="background-color: {color}; width: {score}%; height: 100%; border-radius: 5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Funzione per comparare prodotti
def compare_products(data, product1, product2):
    df1 = data[data['product'] == product1].iloc[0]
    df2 = data[data['product'] == product2].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(product1)
        display_esg_score(df1['esg_score'])
        st.metric("Emissioni CO₂ (tonnellate)", df1['co2_emissions'])
        st.metric("Attività Green (%)", df1['green_activities'])
        if df1['greenwashing_flag']:
            st.markdown("""
            <div class="red-alert">
                ⚠️ <b>Greenwashing Alert</b>: Alto ESG score ma bassa percentuale di attività green.
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader(product2)
        display_esg_score(df2['esg_score'])
        st.metric("Emissioni CO₂ (tonnellate)", df2['co2_emissions'])
        st.metric("Attività Green (%)", df2['green_activities'])
        if df2['greenwashing_flag']:
            st.markdown("""
            <div class="red-alert">
                ⚠️ <b>Greenwashing Alert</b>: Alto ESG score ma bassa percentuale di attività green.
            </div>
            """, unsafe_allow_html=True)
    
    # Suggerimento comparativo
    st.markdown("### Analisi comparativa")
    
    if df1['esg_score'] > df2['esg_score'] and not df1['greenwashing_flag']:
        st.markdown(f"""
        <div class="green-alert">
            🔍 <b>{product1} è più sostenibile di {product2}</b> con un ESG Score superiore 
            (+{df1['esg_score'] - df2['esg_score']} punti) e minori emissioni CO₂.
        </div>
        """, unsafe_allow_html=True)
    elif df2['esg_score'] > df1['esg_score'] and not df2['greenwashing_flag']:
        st.markdown(f"""
        <div class="green-alert">
            🔍 <b>{product2} è più sostenibile di {product1}</b> con un ESG Score superiore 
            (+{df2['esg_score'] - df1['esg_score']} punti) e minori emissioni CO₂.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="green-alert">
            🔍 La comparazione tra <b>{product1}</b> e <b>{product2}</b> richiede un'analisi più dettagliata. 
            Controlla i livelli di attività green e verifica eventuali segnali di greenwashing.
        </div>
        """, unsafe_allow_html=True)
    
    # Grafico comparativo su radar chart
    st.subheader("Grafico comparativo")
    
    # Creare dati per grafico radar
    categories = ['ESG Score', 'Basse Emissioni', 'Attività Green']
    
    # Normalizzare i valori per il radar chart
    max_co2 = max(data['co2_emissions'])
    
    values1 = [
        df1['esg_score']/100,
        1 - (df1['co2_emissions']/max_co2),  # Invertiamo per far sì che meno emissioni = valore più alto
        df1['green_activities']/100
    ]
    
    values2 = [
        df2['esg_score']/100,
        1 - (df2['co2_emissions']/max_co2),
        df2['green_activities']/100
    ]
    
    # Creare il radar chart
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))
    
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Chiudere il poligono
    
    values1 += values1[:1]
    values2 += values2[:1]
    
    ax.plot(angles, values1, 'o-', linewidth=2, label=product1, color='green')
    ax.fill(angles, values1, alpha=0.25, color='green')
    
    ax.plot(angles, values2, 'o-', linewidth=2, label=product2, color='blue')
    ax.fill(angles, values2, alpha=0.25, color='blue')
    
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    st.pyplot(fig)

# Funzione principale per l'app
def main():
    # Applicare stili CSS
    local_css()
    
    # Sidebar - utilizziamo un'icona di testo invece di un'immagine
    st.sidebar.markdown("""
    <div style="background-color: #1E8449; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h2>🌱 GreenInvest+</h2>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.title("GreenInvest+")
    
    # Navigazione
    pages = ["Homepage", "Profilazione", "Dashboard Portafoglio ESG", 
             "Comparatore", "Partner & Marketplace", "Contatti"]
    
    selection = st.sidebar.radio("Navigazione", pages)
    
    # Generare dati (simulati)
    data = generate_esg_data()
    
    # Gestione delle pagine
    if selection == "Homepage":
        # Header
        st.markdown('<h1 class="main-header">GreenInvest+</h1>', unsafe_allow_html=True)
        
        # 3 colonne per layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Sostituiamo l'immagine con un header visivamente accattivante
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0; background: linear-gradient(to right, #1E8449, #2E86C1); padding: 50px; border-radius: 10px; color: white;">
                <h1 style="font-size: 3rem;">🌱 Investimenti Sostenibili</h1>
                <p style="font-size: 1.5rem;">Scopri il tuo impatto positivo sul pianeta</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="green-alert" style="text-align: center; font-size: 1.2rem;">
                <b>GreenInvest+ ti aiuta a scoprire quali investimenti sono davvero sostenibili.</b>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### La tua piattaforma di Open Finance per investimenti ESG
            
            GreenInvest+ utilizza i principi dell'**Open Finance** per analizzare e confrontare strumenti finanziari
            sulla base di criteri **Ambientali**, **Sociali** e di **Governance**.
            
            Scopri come i tuoi investimenti possono generare impatto positivo, evitando il greenwashing e 
            massimizzando la sostenibilità del tuo portafoglio.
            """)
            
            st.button("Inizia ora", help="Clicca per iniziare il tuo percorso di investimento sostenibile")

    elif selection == "Profilazione":
        st.markdown('<h1 class="main-header">Profilazione Utente</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        Prima di iniziare, abbiamo bisogno di alcune informazioni per personalizzare 
        la tua esperienza su GreenInvest+.
        """)
        
        # Form di profilazione
        with st.form("profiling_form"):
            profile_type = st.selectbox(
                "Scegli il tuo profilo", 
                ["Investitore Privato", "Consulente Finanziario"]
            )
            
            age = st.slider("Età", 18, 80, 35)
            
            experience = st.select_slider(
                "Esperienza negli investimenti",
                options=["Principiante", "Intermedio", "Avanzato", "Esperto"]
            )
            
            esg_interest = st.radio(
                "Interesse per le tematiche ESG",
                ["Alto", "Medio", "Basso"]
            )
            
            submitted = st.form_submit_button("Conferma profilo")
            
            if submitted:
                st.success("Profilo salvato con successo!")
                
                # Mostra risultato
                st.markdown("""
                ### Riepilogo profilo
                """)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**Tipo profilo**: {profile_type}")
                    st.info(f"**Età**: {age} anni")
                
                with col2:
                    st.info(f"**Esperienza**: {experience}")
                    st.info(f"**Interesse ESG**: {esg_interest}")
                
                # Suggerimento personalizzato
                if profile_type == "Investitore Privato":
                    if esg_interest == "Alto":
                        st.markdown("""
                        <div class="green-alert">
                            <b>Suggerimento</b>: Data la tua alta sensibilità alle tematiche ESG, 
                            ti consigliamo di esplorare i prodotti con punteggio superiore a 80 e 
                            verificare sempre la percentuale di attività green per evitare il greenwashing.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="green-alert">
                            <b>Suggerimento</b>: Anche con un interesse moderato per l'ESG, 
                            puoi trovare prodotti finanziari che bilanciano rendimento e sostenibilità.
                        </div>
                        """, unsafe_allow_html=True)
                else:  # Consulente finanziario
                    st.markdown("""
                    <div class="green-alert">
                        <b>Suggerimento</b>: Utilizza il comparatore per analizzare in dettaglio 
                        le caratteristiche ESG dei prodotti e offrire consulenze più precise ai tuoi clienti.
                    </div>
                    """, unsafe_allow_html=True)

    elif selection == "Dashboard Portafoglio ESG":
        st.markdown('<h1 class="main-header">Dashboard Portafoglio ESG</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        Esplora gli strumenti finanziari selezionati e le loro caratteristiche di sostenibilità.
        """)
        
        # Grafico generale dei punteggi ESG
        st.subheader("Panoramica ESG Score")
        
        chart_data = pd.DataFrame({
            'product': data['product'],
            'esg_score': data['esg_score']
        })
        
        # Utilizziamo un approccio diverso per il colore in base al valore
        # Creiamo una colonna per il colore
        chart_data['color'] = chart_data['esg_score'].apply(
            lambda x: 'green' if x > 80 else ('orange' if x > 60 else 'red')
        )
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('product', sort=None, title='Prodotto Finanziario'),
            y=alt.Y('esg_score', title='ESG Score'),
            color=alt.Color('color:N', scale=None),  # Usa direttamente il valore del colore
            tooltip=['product', 'esg_score']
        ).properties(
            width=700,
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Mostra dettaglio di ogni prodotto
        st.subheader("Dettaglio prodotti finanziari")
        
        for i, row in data.iterrows():
            with st.expander(f"{row['product']} - ESG Score: {row['esg_score']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # ESG Score con barra colorata
                    display_esg_score(row['esg_score'])
                    
                    # Altre metriche
                    st.metric("Emissioni CO₂ (tonnellate)", row['co2_emissions'])
                    st.metric("Attività Green (%)", row['green_activities'])
                    
                    # Alert per greenwashing
                    if row['greenwashing_flag']:
                        st.markdown("""
                        <div class="red-alert">
                            ⚠️ <b>Greenwashing Alert</b>: Questo prodotto ha un alto ESG score 
                            ma una bassa percentuale di attività effettivamente green.
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # Mini grafico a torta per % attività green
                    fig, ax = plt.subplots(figsize=(3, 3))
                    sizes = [row['green_activities'], 100 - row['green_activities']]
                    labels = ['Green', 'Non-Green']
                    colors = ['#2ECC71', '#E74C3C']
                    
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                           startangle=90, wedgeprops={'width': 0.4})
                    ax.axis('equal')
                    
                    st.pyplot(fig)
        
        # Visualizzazione tabellare
        st.subheader("Vista tabellare")
        st.dataframe(data[['product', 'esg_score', 'co2_emissions', 'green_activities']])

    elif selection == "Comparatore":
        st.markdown('<h1 class="main-header">Comparatore Strumenti Finanziari</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        Confronta due strumenti finanziari per analizzare le loro caratteristiche ESG 
        e prendere decisioni di investimento più consapevoli.
        """)
        
        # Selezione prodotti da confrontare
        col1, col2 = st.columns(2)
        
        with col1:
            product1 = st.selectbox(
                "Seleziona il primo prodotto",
                data['product'].tolist(),
                index=0
            )
        
        with col2:
            product2 = st.selectbox(
                "Seleziona il secondo prodotto",
                data['product'].tolist(),
                index=1
            )
        
        # Confronto
        if product1 != product2:
            compare_products(data, product1, product2)
        else:
            st.warning("Per favore seleziona due prodotti diversi per il confronto.")

    elif selection == "Partner & Marketplace":
        st.markdown('<h1 class="main-header">Partner & Marketplace</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        GreenInvest+ collabora con istituzioni finanziarie, startup innovative e 
        organizzazioni di vari settori per arricchire la propria offerta di soluzioni sostenibili.
        """)
        
        # Creiamo 3 colonne per i partner
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; height: 300px;">
                <h3 style="color: #2E86C1">Intesa Sanpaolo</h3>
                <p><i>Incumbent Finanziario</i></p>
                <div style="background-color: #2E86C1; color: white; text-align: center; padding: 10px; border-radius: 5px; width: 150px; margin: 10px 0;">
                    <strong>Intesa Sanpaolo</strong>
                </div>
                <p>Intesa Sanpaolo fornisce accesso ai dati ESG dei propri prodotti finanziari, 
                   arricchendo GreenInvest+ con una vasta gamma di strumenti d'investimento certificati.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; height: 300px;">
                <h3 style="color: #2E86C1">Clarity AI</h3>
                <p><i>Startup Innovativa</i></p>
                <div style="background-color: #1E8449; color: white; text-align: center; padding: 10px; border-radius: 5px; width: 150px; margin: 10px 0;">
                    <strong>Clarity AI</strong>
                </div>
                <p>Clarity AI utilizza tecnologie di Intelligenza Artificiale per analizzare l'impatto ESG 
                   delle aziende, fornendo a GreenInvest+ dati affidabili e trasparenti.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; height: 300px;">
                <h3 style="color: #2E86C1">Coop</h3>
                <p><i>Partner di diverso settore</i></p>
                <div style="background-color: #E74C3C; color: white; text-align: center; padding: 10px; border-radius: 5px; width: 150px; margin: 10px 0;">
                    <strong>Coop</strong>
                </div>
                <p>Coop collabora con GreenInvest+ per promuovere l'educazione finanziaria sostenibile 
                   tra i suoi soci, offrendo workshop e contenuti formativi.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Marketplace
        st.markdown('<h2 class="sub-header">Marketplace Sostenibile</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        Esplora le opportunità di investimento sostenibile disponibili attraverso i nostri partner.
        """)
        
        # Simulazione card prodotti in marketplace
        marketplace_data = [
            {"name": "Green Bond Facility", "partner": "Intesa Sanpaolo", "min_investment": 5000, "expected_return": "2.5%", "impact": "Finanziamento progetti energie rinnovabili"},
            {"name": "Ocean Fund", "partner": "Clarity AI", "min_investment": 10000, "expected_return": "3.8%", "impact": "Protezione ecosistemi marini"},
            {"name": "Community Impact ETF", "partner": "Coop", "min_investment": 1000, "expected_return": "2.2%", "impact": "Sviluppo comunità locali sostenibili"}
        ]
        
        for i, item in enumerate(marketplace_data):
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                <h3>{item['name']}</h3>
                <p><b>Partner:</b> {item['partner']}</p>
                <p><b>Investimento minimo:</b> €{item['min_investment']}</p>
                <p><b>Rendimento atteso:</b> {item['expected_return']}</p>
                <p><b>Impatto:</b> {item['impact']}</p>
                <button style="background-color: #2E86C1; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                    Scopri di più
                </button>
            </div>
            """, unsafe_allow_html=True)

    elif selection == "Contatti":
        st.markdown('<h1 class="main-header">Contatti & Call to Action</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Sei pronto a investire in modo consapevole?
            
            GreenInvest+ ti offre gli strumenti per prendere decisioni finanziarie 
            allineate con i tuoi valori e con un futuro sostenibile.
            
            Compila il form qui a fianco per ricevere una consulenza personalizzata 
            o per creare il tuo primo portafoglio ESG.
            """)
            
            st.markdown("""
            ### Contattaci
            
            **Email**: info@greeninvestplus.example.com  
            **Telefono**: +39 02 1234567  
            **Sede**: Milano, Via Sostenibilità 123
            """)
            
            st.markdown("""
            <div class="green-alert">
                <b>La nostra missione</b>: Rendere gli investimenti sostenibili accessibili a tutti, 
                attraverso dati trasparenti e comparazioni oggettive.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.form("contact_form"):
                st.markdown("### Richiedi informazioni")
                
                name = st.text_input("Nome e Cognome")
                email = st.text_input("Email")
                phone = st.text_input("Telefono")
                
                interest = st.multiselect(
                    "Sono interessato a",
                    ["Investimenti ESG", "Consulenza finanziaria", "Corsi formativi", "Partnership"]
                )
                
                message = st.text_area("Messaggio")
                
                submitted = st.form_submit_button("Invia richiesta")
                
                if submitted:
                    st.success("Grazie per il tuo interesse! Ti contatteremo presto.")
        
        # Call to Action principale
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 2rem; background-color: #D5F5E3; border-radius: 10px;">
            <h2>Sei pronto a creare il tuo primo portafoglio ESG?</h2>
            <p style="font-size: 1.2rem;">Inizia ora il tuo percorso verso investimenti più sostenibili e consapevoli.</p>
            <button style="background-color: #1E8449; color: white; border: none; padding: 1rem 2rem; border-radius: 5px; font-size: 1.2rem; cursor: pointer; margin-top: 1rem;">
                Crea il tuo portafoglio ESG
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>GreenInvest+ | Progetto Universitario | Dati simulati a scopo dimostrativo</p>
        <p>© 2025 - Tutti i diritti riservati</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
