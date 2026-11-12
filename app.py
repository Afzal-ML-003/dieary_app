import streamlit as st
import json, base64, datetime as dt

st.set_page_config(page_title="Kinza Memories", page_icon="🦋", layout="centered")

TOTAL_PAGES = 20

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:wght@500;700&family=Dancing+Script:wght@500;700&display=swap');
.stApp { background: linear-gradient(160deg, #FFF9E6 0%, #FBEBB5 100%); }
html, body, [class*="css"] { font-family: 'Playfair Display', serif; color: #5C4410; }
.title { font-family: 'Great Vibes', cursive; font-size: 54px; color: #B8860B;
         text-align: center; margin: 0; line-height: 1.1; text-shadow: 1px 2px 3px #e6cf8a; }
.sub { text-align:center; font-family:'Dancing Script',cursive; font-size:22px; color:#8a6a1c; }
.paper { background: #FFFDF5; border: 2px solid #D4AF37; border-radius: 18px;
         padding: 14px 18px; box-shadow: 0 6px 18px rgba(184,134,11,.25); margin-bottom: 14px; }
.datebig { font-family:'Dancing Script',cursive; font-size:30px; color:#B8860B; text-align:center; }
.pageno { text-align:center; font-size:14px; letter-spacing:3px; color:#a88a3a; }
.stTextArea textarea { font-family:'Dancing Script',cursive !important; font-size:24px !important;
    line-height:34px !important; background: repeating-linear-gradient(#FFFDF5, #FFFDF5 33px, #EBD48A 34px) !important;
    color:#4a3708 !important; border:1.5px solid #D4AF37 !important; border-radius:12px !important; }
.stTextInput input { font-family:'Playfair Display',serif; border:1.5px solid #D4AF37 !important;
    background:#FFFDF5 !important; border-radius:10px !important; }
.stButton button, .stDownloadButton button { background: linear-gradient(135deg,#E6C35C,#B8860B);
    color:white; border:none; border-radius:25px; font-weight:700; }
.avatar { display:block; margin:8px auto; width:160px; height:160px; border-radius:50%;
          object-fit:cover; border:4px solid #D4AF37; box-shadow:0 4px 14px rgba(184,134,11,.4); }
#MainMenu, footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ---------- SVG art ----------
def butterfly(size=90):
    return f"""
<div style="text-align:center">
<svg width="{size}" height="{size*0.8}" viewBox="0 0 120 96" xmlns="http://www.w3.org/2000/svg">
 <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#F6DE8D"/><stop offset="1" stop-color="#B8860B"/></linearGradient></defs>
 <path d="M60 48 C40 5, 5 5, 10 35 C13 55, 40 58, 60 48Z" fill="url(#g)" stroke="#8a6508" stroke-width="1.5"/>
 <path d="M60 48 C80 5, 115 5, 110 35 C107 55, 80 58, 60 48Z" fill="url(#g)" stroke="#8a6508" stroke-width="1.5"/>
 <path d="M60 50 C42 55, 22 70, 35 88 C48 92, 58 70, 60 50Z" fill="#E6C35C" stroke="#8a6508" stroke-width="1.5"/>
 <path d="M60 50 C78 55, 98 70, 85 88 C72 92, 62 70, 60 50Z" fill="#E6C35C" stroke="#8a6508" stroke-width="1.5"/>
 <circle cx="30" cy="28" r="6" fill="#FFF3C4"/><circle cx="90" cy="28" r="6" fill="#FFF3C4"/>
 <ellipse cx="60" cy="52" rx="3.5" ry="22" fill="#5C4410"/>
 <path d="M58 30 C52 16, 46 12, 42 14 M62 30 C68 16, 74 12, 78 14" stroke="#5C4410" fill="none" stroke-width="1.8"/>
</svg></div>"""

LOGO = """
<div style="text-align:center">
<svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
 <defs><radialGradient id="r"><stop offset="0" stop-color="#FFF3C4"/><stop offset="1" stop-color="#D4AF37"/></radialGradient></defs>
 <circle cx="75" cy="75" r="70" fill="url(#r)" stroke="#8a6508" stroke-width="3"/>
 <circle cx="75" cy="75" r="60" fill="none" stroke="#8a6508" stroke-width="1.2" stroke-dasharray="3 4"/>
 <rect x="42" y="70" width="66" height="44" rx="4" fill="#FFFDF5" stroke="#8a6508" stroke-width="2"/>
 <line x1="75" y1="70" x2="75" y2="114" stroke="#8a6508" stroke-width="2"/>
 <path d="M75 62 C62 30, 38 32, 42 52 C44 64, 62 66, 75 62Z" fill="#B8860B"/>
 <path d="M75 62 C88 30, 112 32, 108 52 C106 64, 88 66, 75 62Z" fill="#B8860B"/>
 <ellipse cx="75" cy="64" rx="2.5" ry="14" fill="#5C4410"/>
 <text x="75" y="134" text-anchor="middle" font-family="Great Vibes, cursive" font-size="16" fill="#5C4410">K M</text>
</svg></div>"""

# ---------- State ----------
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "", "address": "", "phone": "", "photo": ""}
if "pages" not in st.session_state:
    st.session_state.pages = {}
if "page" not in st.session_state:
    st.session_state.page = 0

def go(delta):
    st.session_state.page = max(0, min(TOTAL_PAGES, st.session_state.page + delta))

def page_label(i):
    return "Cover" if i == 0 else f"Page {i}"

# ---------- Header ----------
st.markdown(LOGO, unsafe_allow_html=True)
st.markdown('<p class="title">Kinza Memories</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">~ my little golden diary ~</p>', unsafe_allow_html=True)

# ---------- Navigation ----------
c1, c2, c3 = st.columns([1, 2, 1])
c1.button("⬅ Prev", on_click=go, args=(-1,), use_container_width=True)
c3.button("Next ➡", on_click=go, args=(1,), use_container_width=True)
c2.selectbox("Go to", list(range(TOTAL_PAGES + 1)), key="page",
             format_func=page_label, label_visibility="collapsed")
p = st.session_state.page

# ---------- Cover page ----------
if p == 0:
    st.markdown(butterfly(110), unsafe_allow_html=True)
    st.markdown('<div class="paper">', unsafe_allow_html=True)
    prof = st.session_state.profile
    pic = st.file_uploader("📸 Apni pic lagayen", type=["png", "jpg", "jpeg"])
    if pic is not None:
        prof["photo"] = base64.b64encode(pic.getvalue()).decode()
    if prof["photo"]:
        st.markdown(f'<img class="avatar" src="data:image/png;base64,{prof["photo"]}">',
                    unsafe_allow_html=True)
    prof["name"] = st.text_input("Name", prof["name"])
    prof["address"] = st.text_input("Address", prof["address"])
    prof["phone"] = st.text_input("Phone number", prof["phone"])
    st.markdown('</div>', unsafe_allow_html=True)
    if prof["name"]:
        st.markdown(f'<div class="datebig">Welcome, {prof["name"]} 🦋</div>', unsafe_allow_html=True)

# ---------- Diary pages ----------
else:
    data = st.session_state.pages.setdefault(
        p, {"date": dt.date.today().isoformat(), "time": dt.datetime.now().strftime("%H:%M"),
            "title": "", "text": ""})
    st.markdown(butterfly(90), unsafe_allow_html=True)
    st.markdown(f'<div class="pageno">— PAGE {p} OF {TOTAL_PAGES} —</div>', unsafe_allow_html=True)
    st.markdown('<div class="paper">', unsafe_allow_html=True)

    d = st.date_input("📅 Date (calendar)", dt.date.fromisoformat(data["date"]), key=f"d{p}")
    t = st.time_input("⏰ Time", dt.time.fromisoformat(data["time"]), key=f"t{p}")
    data["date"], data["time"] = d.isoformat(), t.strftime("%H:%M")
    st.markdown(f'<div class="datebig">{d.strftime("%A, %d %B %Y")} · {t.strftime("%I:%M %p")}</div>',
                unsafe_allow_html=True)

    data["title"] = st.text_input("Title", data["title"], key=f"ti{p}")
    data["text"] = st.text_area("Dear diary...", data["text"], height=360, key=f"tx{p}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Backup ----------
with st.expander("💾 Backup / Restore"):
    backup = json.dumps({"profile": st.session_state.profile,
                         "pages": st.session_state.pages}, ensure_ascii=False)
    st.download_button("Download diary backup", backup, "kinza_memories.json", "application/json")
    up = st.file_uploader("Restore backup", type=["json"], key="restore")
    if up is not None and st.button("Restore now"):
        obj = json.loads(up.getvalue().decode("utf-8"))
        st.session_state.profile = obj["profile"]
        st.session_state.pages = {int(k): v for k, v in obj["pages"].items()}
        st.rerun()
