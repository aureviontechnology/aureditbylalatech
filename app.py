import streamlit as st
import pandas as pd
import plotly.express as px  # <-- Modulus px sudah ditambahkan di sini
import plotly.graph_objects as go
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="J-SOX LOGIN PORTAL",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS dengan Kontras Tinggi & Styling Tepat Di Tengah
custom_css = """
<style>
    /* Gradient Background Utama */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #1e3c72 50%, #2a085c 100%);
        color: #ffffff !important;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }

    /* Container Header Utama */
    .main-header {
        text-align: center !important;
        padding: 2rem 0rem 2rem 0rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    .main-header h1 {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4d4d, #4d94ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 auto !important;
        line-height: 1.1;
        text-align: center !important;
        width: 100%;
    }
    .main-header h2 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4d4d, #4d94ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem auto 0.8rem auto !important;
        line-height: 1.2;
        text-align: center !important;
        width: 100%;
    }
    .main-header p {
        color: #e2e8f0 !important;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-align: center !important;
        margin: 0 auto !important;
        width: 100%;
    }

    .dept-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff !important;
        text-align: center !important;
        margin-bottom: 12px;
        width: 100%;
    }

    div[data-testid="column"] {
        border-radius: 12px;
        text-align: center !important;
    }
    
    /* Tombol Pilihan Departemen Utama */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #ff4d4d;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff4d4d 0%, #f92b2b 100%);
        color: #ffffff !important;
        border-color: #ffffff;
        box-shadow: 0 4px 15px rgba(255, 77, 77, 0.4);
    }

    /* Form Container */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-radius: 16px !important;
        border: 2px solid #ff4d4d !important;
        padding: 1.8rem !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7) !important;
    }

    label, div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }

    /* Input Field & Password Styling */
    .stTextInput > div > div > input, .stDateInput > div > div > input {
        background-color: #f1f5f9 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 8px !important;
        border: 2px solid #cbd5e1 !important;
    }
    .stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus {
        border-color: #ff4d4d !important;
        box-shadow: 0 0 8px rgba(255, 77, 77, 0.8) !important;
        background-color: #ffffff !important;
    }

    /* Styling Tombol Form Login & Input */
    div[data-testid="stForm"] .stButton > button {
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 0.6rem 1rem !important;
        border-radius: 8px !important;
    }

    /* Tombol Submit Form (Kiri) */
    div[data-testid="stForm"] [data-testid="column"]:nth-of-type(1) .stButton > button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border: 1px solid #34d399 !important;
    }

    /* Tombol Cancel Form (Kanan) */
    div[data-testid="stForm"] [data-testid="column"]:nth-of-type(2) .stButton > button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        border: 1px solid #f87171 !important;
    }

    /* Selectbox Styling */
    div[data-baseweb="select"] > div {
        background-color: #f1f5f9 !important;
        color: #000000 !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }

    /* Style Kartu Metrik J-SOX */
    .metric-card {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .metric-title {
        font-size: 1rem;
        color: #f1f5f9 !important;
        font-weight: 700;
    }
    .metric-val {
        font-size: 2.3rem;
        font-weight: bold;
        margin: 5px 0;
    }
    .metric-pct {
        font-size: 0.9rem;
        color: #cbd5e1 !important;
        font-weight: 600;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Data 9 Departemen & State Management
DEPARTMENTS = [
    {"id": "audit", "name": "Internal Audit", "icon": "🔍"},
    {"id": "procurement", "name": "Procurement", "icon": "🛒"},
    {"id": "it", "name": "IT", "icon": "💻"},
    {"id": "finance_accounting", "name": "Finance and Accounting", "icon": "💰"},
    {"id": "marketing", "name": "Marketing", "icon": "📈"},
    {"id": "hr_ga", "name": "HR & GA", "icon": "👥"},
    {"id": "ppic", "name": "PPIC", "icon": "📦"},
    {"id": "management_system", "name": "Management System", "icon": "📊"},
    {"id": "corporate_function", "name": "Corporate Function", "icon": "🏢"}
]

if 'selected_dept' not in st.session_state:
    st.session_state.selected_dept = None
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# Inisialisasi Data Kaizen Request di Session State
if 'kaizen_list' not in st.session_state:
    st.session_state.kaizen_list = [
        {"No": 1, "Tema Kaizen": "Kontrol approval PO", "Departemen": "Procurement", "PIC (BPO)": "BPO A", "Target Selesai": "15/10/2026", "Status": "Dalam Proses"},
        {"No": 2, "Tema Kaizen": "Pemisahan tugas", "Departemen": "Finance and Accounting", "PIC (BPO)": "BPO B", "Target Selesai": "20/10/2026", "Status": "Terlambat"},
        {"No": 3, "Tema Kaizen": "Rekonsiliasi GR-IR", "Departemen": "Finance and Accounting", "PIC (BPO)": "BPO C", "Target Selesai": "30/10/2026", "Status": "Dalam Proses"},
        {"No": 4, "Tema Kaizen": "Update SOP P2P", "Departemen": "Procurement", "PIC (BPO)": "BPO D", "Target Selesai": "10/11/2026", "Status": "Dalam Proses"},
        {"No": 5, "Tema Kaizen": "Audit Keamanan Jaringan", "Departemen": "IT", "PIC (BPO)": "BPO A", "Target Selesai": "05/09/2026", "Status": "Selesai"}
    ]

# ==========================================
# 4. HALAMAN DASHBOARD SETELAH LOGIN
# ==========================================
if st.session_state.logged_in_user:
    user_dept = st.session_state.logged_in_user['dept_id']
    username = st.session_state.logged_in_user['username']
    
    # Top Bar / Navigasi
    top_col1, top_col2 = st.columns([8, 2])
    with top_col1:
        st.markdown(f"### 👤 Selamat Datang, <span style='color:#00d2ff;'>{username}</span> (`{st.session_state.logged_in_user['dept_name']}`)", unsafe_allow_html=True)
    with top_col2:
        if st.button("🔴 Logout", key="btn_logout"):
            st.session_state.logged_in_user = None
            st.session_state.selected_dept = None
            st.rerun()

    st.write("---")

    # -------------------------------------------------------------
    # A. KHUSUS TAMPILAN DASHBOARD INTERNAL AUDIT (J-SOX MONITORING)
    # -------------------------------------------------------------
    if user_dept == "audit":
        st.markdown("<h2 style='text-align: center; color: #ffffff;'>J-SOX Activity Plan Monitoring</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #e2e8f0; font-size:1.1rem;'>Pemantauan dan pencapaian aktivitas J-SOX secara real-time</p>", unsafe_allow_html=True)
        st.write("")

        # Filter Atas (Tahun Fiskal, Periode 4 Bulan, Departemen, PIC)
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            selected_year = st.selectbox(
                "Tahun Grafik", 
                ["2025/2026", "2026/2027"]
            )
        with f_col2:
            selected_period = st.selectbox(
                "Periode (4 Bulan)", 
                [
                    "Semua (1 Tahun)",
                    "April - Juli", 
                    "Agustus - November", 
                    "Desember - Maret"
                ]
            )
        with f_col3:
            st.selectbox("Departemen Filter", ["Semua", "Procurement", "IT", "Finance and Accounting", "Marketing", "HR & GA", "PPIC", "Management System", "Corporate Function"])
        with f_col4:
            st.selectbox("PIC Filter (BPO)", ["Semua", "BPO A", "BPO B", "BPO C", "BPO D"])

        st.write("")

        # BACKEND CALCULATIONS (HITUNG JUMLAH KAIZEN & PERSENTASE)
        df_kaizen = pd.DataFrame(st.session_state.kaizen_list)
        
        total_kaizen = len(df_kaizen)
        cnt_selesai = len(df_kaizen[df_kaizen['Status'] == 'Selesai'])
        cnt_progres = len(df_kaizen[df_kaizen['Status'] == 'Dalam Proses'])
        cnt_terlambat = len(df_kaizen[df_kaizen['Status'] == 'Terlambat'])

        pct_selesai = round((cnt_selesai / total_kaizen * 100), 1) if total_kaizen > 0 else 0
        pct_progres = round((cnt_progres / total_kaizen * 100), 1) if total_kaizen > 0 else 0
        pct_terlambat = round((cnt_terlambat / total_kaizen * 100), 1) if total_kaizen > 0 else 0

        # Summary Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #4d94ff;">
                <div class="metric-title">Total Kaizen Request</div>
                <div class="metric-val" style="color: #4d94ff;">{total_kaizen}</div>
                <div class="metric-pct">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #2ecc71;">
                <div class="metric-title">Selesai (Implemented)</div>
                <div class="metric-val" style="color: #2ecc71;">{cnt_selesai}</div>
                <div class="metric-pct">{pct_selesai}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #ff9f43;">
                <div class="metric-title">Outstanding (Dalam Proses)</div>
                <div class="metric-val" style="color: #ff9f43;">{cnt_progres}</div>
                <div class="metric-pct">{pct_progres}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #ff4d4d;">
                <div class="metric-title">Terlambat</div>
                <div class="metric-val" style="color: #ff4d4d;">{cnt_terlambat}</div>
                <div class="metric-pct">{pct_terlambat}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # Row Baris Kedua: Grafik
        g_col1, g_col2, g_col3 = st.columns([1, 1.2, 1.5])

        # Grafik 1: Donut Chart Status
        with g_col1:
            st.markdown("<h5 style='color:#ffffff; text-align:center;'>Status Activity Plan</h5>", unsafe_allow_html=True)
            labels = ['Selesai', 'Dalam Proses', 'Terlambat']
            values = [cnt_selesai, cnt_progres, cnt_terlambat]
            colors = ['#2ecc71', '#ff9f43', '#ff4d4d']
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=.6,
                marker=dict(colors=colors),
                textinfo='percent',
                textfont=dict(color='#ffffff', size=14)
            )])
            fig_donut.update_layout(
                showlegend=True,
                margin=dict(l=10, r=10, t=20, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#ffffff", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="#ffffff"))
            )
            fig_donut.add_annotation(text=f"{total_kaizen}<br>Request", x=0.5, y=0.5, font_size=18, showarrow=False, font=dict(color="#ffffff", family="sans-serif"))
            st.plotly_chart(fig_donut, use_container_width=True)

        # Grafik 2: Progress per Departemen
        with g_col2:
            st.markdown("<h5 style='color:#ffffff; text-align:center;'>Progress per Departemen</h5>", unsafe_allow_html=True)
            dept_counts = df_kaizen['Departemen'].value_counts().reset_index()
            dept_counts.columns = ['Departemen', 'Jumlah']
            
            fig_bar = px.bar(dept_counts, x='Jumlah', y='Departemen', orientation='h', text='Jumlah')
            fig_bar.update_traces(marker_color='#4d94ff', textposition='outside', textfont=dict(color="#ffffff", size=13))
            fig_bar.update_layout(
                xaxis=dict(showgrid=False, title="", tickfont=dict(color="#ffffff")),
                yaxis=dict(title="", tickfont=dict(color="#ffffff", size=13)),
                margin=dict(l=10, r=20, t=20, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#ffffff")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Grafik 3: Target vs Implemented (2 Bar Berdampingan per Bulan)
        with g_col3:
            st.markdown("<h5 style='color:#ffffff; text-align:center;'>Target vs Implemented</h5>", unsafe_allow_html=True)
            
            all_months = ['Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des', 'Jan', 'Feb', 'Mar']
            target_data_all = [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40]
            implemented_data_all = [10, 12, 15, 18, 19, 21, 24, 26, 29, 31, 35, 38]

            if selected_period == "April - Juli":
                months_filtered = all_months[0:4]
                target_filtered = target_data_all[0:4]
                implemented_filtered = implemented_data_all[0:4]
            elif selected_period == "Agustus - November":
                months_filtered = all_months[4:8]
                target_filtered = target_data_all[4:8]
                implemented_filtered = implemented_data_all[4:8]
            elif selected_period == "Desember - Maret":
                months_filtered = all_months[8:12]
                target_filtered = target_data_all[8:12]
                implemented_filtered = implemented_data_all[8:12]
            else:
                months_filtered = all_months
                target_filtered = target_data_all
                implemented_filtered = implemented_data_all

            fig_2bar = go.Figure()
            
            fig_2bar.add_trace(go.Bar(
                x=months_filtered, 
                y=target_filtered, 
                name='Target (Total Kaizen)', 
                marker_color='#4d94ff',
                text=target_filtered,
                textposition='auto'
            ))
            
            fig_2bar.add_trace(go.Bar(
                x=months_filtered, 
                y=implemented_filtered, 
                name='Implemented (Selesai)', 
                marker_color='#2ecc71',
                text=implemented_filtered,
                textposition='auto'
            ))

            fig_2bar.update_layout(
                barmode='group',
                xaxis=dict(tickfont=dict(color="#ffffff")),
                yaxis=dict(tickfont=dict(color="#ffffff"), showgrid=False),
                margin=dict(l=10, r=10, t=20, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#ffffff"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="#ffffff"))
            )
            st.plotly_chart(fig_2bar, use_container_width=True)

        st.write("")

        # FORM INPUT PENGISIAN DATA KAIZEN REQUEST (INTERNAL AUDIT)
        st.markdown("<h4 style='color:#00d2ff; text-align:center;'>➕ Tambah Kaizen Request Baru (Internal Audit)</h4>", unsafe_allow_html=True)
        
        with st.form("form_add_kaizen"):
            c_input1, c_input2 = st.columns(2)
            with c_input1:
                input_tema = st.text_input("Tema Kaizen", placeholder="Masukkan tema kaizen...")
                input_dept = st.selectbox("Departemen", [d["name"] for d in DEPARTMENTS])
            with c_input2:
                input_pic = st.selectbox("PIC (BPO)", ["BPO A", "BPO B", "BPO C", "BPO D", "BPO E"])
                input_target = st.date_input("Target Selesai", datetime.now())
                input_status = st.selectbox("Status", ["Dalam Proses", "Selesai", "Terlambat"])

            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                submit_kaizen = st.form_submit_button("Simpan Data 💾")
            with btn_col2:
                clear_kaizen = st.form_submit_button("Reset Form 🔄")

            if submit_kaizen:
                if input_tema.strip() != "":
                    new_no = len(st.session_state.kaizen_list) + 1
                    formatted_date = input_target.strftime("%d/%m/%Y")
                    
                    new_entry = {
                        "No": new_no,
                        "Tema Kaizen": input_tema,
                        "Departemen": input_dept,
                        "PIC (BPO)": input_pic,
                        "Target Selesai": formatted_date,
                        "Status": input_status
                    }
                    st.session_state.kaizen_list.append(new_entry)
                    st.success("Data Kaizen Request berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Tema Kaizen tidak boleh kosong!")

        st.write("")
        st.write("---")

        # TABEL KAIZEN REQUEST DENGAN OPSI UPDATE RETARGET & STATUS
        st.markdown("<h5 style='color:#ffffff; text-align:center;'>Daftar Outstanding Kaizen Request (Retarget Selesai & Update Status)</h5>", unsafe_allow_html=True)
        st.write("")

        h_c1, h_c2, h_c3, h_c4, h_c5, h_c6, h_c7 = st.columns([0.5, 2.5, 2, 1.2, 1.5, 1.5, 2])
        with h_c1: st.markdown("**No**")
        with h_c2: st.markdown("**Tema Kaizen**")
        with h_c3: st.markdown("**Departemen**")
        with h_c4: st.markdown("**PIC**")
        with h_c5: st.markdown("**Target Selesai**")
        with h_c6: st.markdown("**Status**")
        with h_c7: st.markdown("**Retarget Selesai**")

        st.markdown("<hr style='margin: 5px 0px 15px 0px; border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

        for idx, item in enumerate(st.session_state.kaizen_list):
            row_c1, row_c2, row_c3, row_c4, row_c5, row_c6, row_c7 = st.columns([0.5, 2.5, 2, 1.2, 1.5, 1.5, 2])
            
            with row_c1:
                st.write(f"**{item['No']}**")
            with row_c2:
                st.write(item['Tema Kaizen'])
            with row_c3:
                st.write(item['Departemen'])
            with row_c4:
                st.write(item['PIC (BPO)'])
            with row_c5:
                st.write(f"📅 `{item['Target Selesai']}`")
            with row_c6:
                new_status = st.selectbox(
                    f"Status_{idx}", 
                    options=["Dalam Proses", "Selesai", "Terlambat"], 
                    index=["Dalam Proses", "Selesai", "Terlambat"].index(item['Status']),
                    key=f"status_select_{idx}",
                    label_visibility="collapsed"
                )
                if new_status != item['Status']:
                    st.session_state.kaizen_list[idx]['Status'] = new_status
                    st.rerun()

            with row_c7:
                c_date, c_btn = st.columns([1.2, 0.8])
                with c_date:
                    new_retarget_date = st.date_input(
                        f"retarget_{idx}", 
                        value=datetime.now(), 
                        key=f"retarget_date_{idx}",
                        label_visibility="collapsed"
                    )
                with c_btn:
                    if st.button("Update 🔄", key=f"btn_retarget_{idx}"):
                        st.session_state.kaizen_list[idx]['Target Selesai'] = new_retarget_date.strftime("%d/%m/%Y")
                        st.success(f"Target selesai No {item['No']} berhasil di-retarget!")
                        st.rerun()

            st.markdown("<hr style='margin: 8px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # B. TAMPILAN UNTUK DEPARTEMEN LAINNYA
    # -------------------------------------------------------------
    else:
        st.info(f"Anda berhasil masuk ke Portal Dashboard **{st.session_state.logged_in_user['dept_name']}**.")
        st.write("Silakan pilih menu operasional departemen Anda pada panel ini.")

# ==========================================
# 5. TAMPILAN PILIHAN DEPARTEMEN & FORM LOGIN
# ==========================================
else:
    st.markdown("""
    <div class="main-header">
        <h1>J-SOX DASHBOARD</h1>
        <h2>MONITORING ACTIVITY</h2>
        <p>SILAHKAN PILIH DEPARTEMEN ANDA</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3, col1, col2, col3]

    for idx, dept in enumerate(DEPARTMENTS):
        with cols[idx]:
            st.markdown(f'<div class="dept-title">{dept["icon"]} {dept["name"]}</div>', unsafe_allow_html=True)
            
            if st.button("Login", key=f"btn_{dept['id']}"):
                st.session_state.selected_dept = dept
                st.rerun()

    if st.session_state.selected_dept:
        st.write("---")
        dept_info = st.session_state.selected_dept
        
        _, form_col, _ = st.columns([1, 2, 1])
        
        with form_col:
            with st.form("login_form"):
                st.markdown(f"<h3 style='text-align: center; color: #ff4d4d;'>Login {dept_info['name']}</h3>", unsafe_allow_html=True)
                
                username = st.text_input("Username / NIK", placeholder="Masukkan username...")
                password = st.text_input("Password", type="password", placeholder="Masukkan password...")
                
                col_submit, col_cancel = st.columns(2)
                with col_submit:
                    submit_button = st.form_submit_button("Masuk 🔑")
                with col_cancel:
                    cancel_button = st.form_submit_button("Batal ❌")

                if submit_button:
                    if username and password:
                        st.session_state.logged_in_user = {
                            "username": username,
                            "dept_id": dept_info['id'],
                            "dept_name": dept_info['name']
                        }
                        st.rerun()
                    else:
                        st.error("Username dan Password tidak boleh kosong!")
                
                if cancel_button:
                    st.session_state.selected_dept = None
                    st.rerun()