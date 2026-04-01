import streamlit as st
import random
import pandas as pd
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="HARMONIA | O2 Style", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# FUNKCJE POMOCNICZE DO TŁA
# ============================================================

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_jpg_as_page_bg(jpg_file):
    try:
        bin_str = get_base64_of_bin_file(jpg_file)
        page_bg_img = f'''
        <style>
        /* Przypinamy zdjęcie do głównego kontenera Streamlit */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Robimy górny pasek Streamlit całkowicie przezroczystym */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* KLUCZOWE: Wyłączamy awaryjny jasny gradient z pliku style.css, żeby odsłonić zdjęcie! */
        body::before {{
            display: none !important;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Jeśli nie ma zdjęcia, zostawiamy awaryjny gradient

# ============================================================
# KONFIGURACJA TŁA I STYLU
# ============================================================

# Ładujemy Twoje zdjęcie
set_jpg_as_page_bg('tlo_harmonia.jpg') 

# 2. Następnie ładujemy CSS, który nadpisze style Streamlit
with open("style.css", "r", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("clothes.csv")
    except:
        data = []
        brands = ["Nike", "Adidas", "ZARA", "H&M", "Gucci", "Prada", "Uniqlo"]
        types = ["jacket", "shoes", "pants", "tshirt", "shorts", "hoodie"]
        colors = ["black", "white", "navy", "gray", "red", "green", "beige"]
        for i in range(250):
            t = random.choice(types)
            data.append({
                "id": i, "name": f"{t.capitalize()}_{i}",
                "price": random.randint(40, 950), "value": random.randint(100, 1600),
                "type": t, "brand": random.choice(brands).lower(), "color": random.choice(colors)
            })
        return pd.DataFrame(data)

df_raw = load_data()
products_list = df_raw.to_dict('records')

# ============================================================
# HARMONY SEARCH ENGINE
# ============================================================
class HarmonyStylist:
    def __init__(self, pool, budget, target_types, HMS=15, HMCR=0.85, PAR=0.3, NI=4000):
        self.pool = pool
        self.budget = budget
        self.target_types = target_types
        self.HMS = HMS
        self.HMCR = HMCR
        self.PAR = PAR
        self.iterations = NI
        self.harmony_memory = []
        self.harmony_scores = []

    def _evaluate(self, indices):
        if not indices: return 0
        total_price = sum(self.pool[idx]['price'] for idx in indices)
        if total_price > self.budget: return 0
        types_present = {self.pool[idx]['type'] for idx in indices}
        if len(types_present) < len(self.target_types): return 0
        return sum(self.pool[idx]['value'] for idx in indices)

    def _generate_harmony(self, source_pool_indices=None):
        selection = []
        full_indices = list(range(len(self.pool)))
        for t in self.target_types:
            candidates = [idx for idx in (source_pool_indices or full_indices) if self.pool[idx]['type'] == t]
            if not candidates:
                candidates = [idx for idx in full_indices if self.pool[idx]['type'] == t]
            if candidates:
                selection.append(random.choice(candidates))
        return selection

    def run(self):
        for _ in range(self.HMS):
            sol = self._generate_harmony()
            self.harmony_memory.append(sol)
            self.harmony_scores.append(self._evaluate(sol))

        for _ in range(self.iterations):
            if random.random() < self.HMCR:
                mem_indices = list(set([idx for sol in self.harmony_memory for idx in sol]))
                new_sol = self._generate_harmony(mem_indices)
                if random.random() < self.PAR:
                    idx_to_change = random.randrange(len(new_sol))
                    t_type = self.target_types[idx_to_change]
                    all_of_type = [i for i, p in enumerate(self.pool) if p['type'] == t_type]
                    if all_of_type: new_sol[idx_to_change] = random.choice(all_of_type)
            else:
                new_sol = self._generate_harmony()

            new_score = self._evaluate(new_sol)
            worst_score = min(self.harmony_scores)
            if new_score > worst_score and new_sol not in self.harmony_memory:
                idx_replace = self.harmony_scores.index(worst_score)
                self.harmony_memory[idx_replace] = new_sol
                self.harmony_scores[idx_replace] = new_score

        results = []
        sorted_idx = sorted(range(len(self.harmony_scores)), key=lambda k: self.harmony_scores[k], reverse=True)
        for i in sorted_idx:
            if self.harmony_scores[i] > 0:
                sol = self.harmony_memory[i]
                results.append({'items': [self.pool[idx] for idx in sol], 'score': self.harmony_scores[i], 'cost': sum(self.pool[idx]['price'] for idx in sol)})
            if len(results) >= 3: break
        return results

# ============================================================
# UI LAYOUT
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">HARMONIA</div>
    <div class="hero-sub">AI Stylist</div>
</div>
<div class="algo-strip">
    <span>Engine: <b>Harmony Search</b></span>
    <span>Status: <b>Ready</b></span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
col_cfg, col_res = st.columns([1, 2], gap="large")

with col_cfg:
    st.subheader("Parameters")
    u_budget = st.number_input("Max Budget (PLN)", 100, 10000, 1500)
    u_types = st.multiselect("Elements (1 per cat)", 
                             options=sorted(df_raw['type'].unique()), 
                             default=["jacket", "pants", "shoes"])
    u_colors = st.multiselect("Colors", options=sorted(df_raw['color'].unique()))
    u_brands = st.multiselect("Brands", options=sorted(df_raw['brand'].unique()))
    
    generate_btn = st.button("Generate Collection")

with col_res:
    st.subheader("Results")
    if generate_btn:
        pool = products_list
        if u_colors: pool = [p for p in pool if p['color'] in u_colors]
        if u_brands: pool = [p for p in pool if p['brand'] in u_brands]
        
        available_types = {p['type'] for p in pool}
        missing = [t for t in u_types if t not in available_types]
        
        if missing:
            st.error(f"Missing items for: {', '.join(missing)} with current filters.")
        elif not u_types:
            st.warning("Please select at least one category.")
        else:
            engine = HarmonyStylist(pool, u_budget, u_types)
            with st.spinner("Processing..."):
                results = engine.run()

            if not results:
                st.warning("No valid set found within budget. Try increasing it.")
            else:
                # Rozszerzony słownik kolorów (teraz zawiera blue, yellow, itp.)
                c_dots = {
                    "black": "#1A1A1A", 
                    "white": "#F8F8F8", 
                    "gray": "#8D99AE", 
                    "red": "#EF233C", 
                    "green": "#2A9D8F", 
                    "blue": "#3A86FF",    
                    "yellow": "#FFBE0B",  
                    "navy": "#1B263B",    
                    "beige": "#E9C46A"    
                }

                for i, res in enumerate(results):
                    set_num = f"0{i+1}"
                    
                    # UWAGA: Kod celowo "przyklejony" do lewej krawędzi (bez wcięć), 
                    # aby Streamlit nie traktował go jako "Bloku Kodu" w Markdown.
                    html_content = f"""<div class="result-card">
<div class="card-header">
<div class="card-number">{set_num}</div>
<div class="card-stats">
Fitness: {int(res['score'])}<br>
Total: {res['cost']} PLN
</div>
</div>"""
                    
                    for item in res['items']:
                        # Pobiera kolor ze słownika, domyślnie szary jeśli go nie ma
                        dot_color = c_dots.get(item['color'], "#888888")
                        
                        html_content += f"""
<div class="product-row">
<div class="product-info">
<span class="type-badge">{item['type']}</span>
<span class="color-dot" style="background-color: {dot_color};"></span>
<b>{item['brand'].upper()}</b> {item['name']}
</div>
<div class="product-price">{item['price']} PLN</div>
</div>"""
                        
                    html_content += "</div>"
                    
                    st.markdown(html_content, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)