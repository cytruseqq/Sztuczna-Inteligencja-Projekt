import streamlit as st
import random
import hashlib
import pandas as pd
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="HARMONIA | AI Stylist", layout="wide", initial_sidebar_state="collapsed")

# --- LOAD CSS FROM FILE ---
with open("style.css", "r", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# --- LOAD DATA ---
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

# --- HARMONY SEARCH ENGINE ---
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

# --- UI LAYOUT ---
st.markdown("""
<div class="hero">
    <div class="hero-title">Harmonia <em>Stylist</em></div>
</div>
<div class="algo-strip">
    <span>ENGINE: <b>HARMONY SEARCH</b></span>
    <span>STATUS: <b>SYSTEM READY</b></span>
    <span>VERSION: <b>3.0 PREM</b></span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
col_cfg, col_res = st.columns([1, 2])

with col_cfg:
    st.subheader("Configuration")
    u_budget = st.number_input("Maximum Budget (PLN)", 100, 10000, 1500)
    u_types = st.multiselect("Outfit Elements (1 per category)", 
                             options=sorted(df_raw['type'].unique()), 
                             default=["jacket", "pants", "shoes"])
    u_colors = st.multiselect("Preferred Colors", options=sorted(df_raw['color'].unique()))
    u_brands = st.multiselect("Preferred Brands", options=sorted(df_raw['brand'].unique()))

with col_res:
    st.subheader("Optimization Results")
    if st.button("✦ GENERATE 3 ALTERNATIVE SETS"):
        pool = products_list
        if u_colors: pool = [p for p in pool if p['color'] in u_colors]
        if u_brands: pool = [p for p in pool if p['brand'] in u_brands]
        
        # Check if all categories are still available after filtering
        available_types = {p['type'] for p in pool}
        missing = [t for t in u_types if t not in available_types]
        
        if missing:
            st.error(f"Missing items for: {', '.join(missing)} with current filters.")
        elif not u_types:
            st.warning("Please select at least one category.")
        else:
            engine = HarmonyStylist(pool, u_budget, u_types)
            with st.spinner("Improvising New Harmonies..."):
                results = engine.run()

            if not results:
                st.warning("No valid set found within budget. Try increasing it.")
            else:
                for i, res in enumerate(results):
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="card-header">
                            <span>ALTERNATIVE SET {i+1}</span>
                            <span style="color:#4ECDC4;">FITNESS: {int(res['score'])} | {res['cost']} PLN</span>
                        </div>
                    """, unsafe_allow_html=True)
                    for item in res['items']:
                        c_dots = {"black":"#000","white":"#fff","navy":"#000080","gray":"#808080","red":"#f00","green":"#008000","beige":"#f5f5dc"}
                        dot_color = c_dots.get(item['color'], "#888")
                        st.markdown(f"""
                        <div class="product-row">
                            <div>
                                <span class="type-badge">{item['type']}</span>
                                <span class="color-dot" style="background:{dot_color}"></span>
                                <b>{item['brand'].upper()}</b> — {item['name']}
                            </div>
                            <div>{item['price']} PLN</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    © ANS — Akademia Nauk Stosowanych · Harmonia Stylist v3.0 · Powered by Harmony Search
</div>
""", unsafe_allow_html=True)