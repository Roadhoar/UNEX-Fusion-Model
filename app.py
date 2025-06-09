
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="UN-EX Fusion Dashboard", layout="wide")

st.title("🧪 UN-EX Plasma Confinement Simulation")
st.markdown("Explore live plasma confinement with interactive sliders, smart mode sweep, and model comparison.")

tabs = st.tabs(["🔬 Simulation", "🤖 Smart Q Sweep", "📊 Model Comparison"])

# --- Constants ---
alpha = 1.0
beta = 1.0
gamma = 1.0

# --- Tab 1: Manual Simulation ---
with tabs[0]:
    st.subheader("Manual Tuning Mode")

    T = st.slider("Plasma Temperature (keV)", 1.0, 20.0, 5.0)
    B = st.slider("Magnetic Field Strength (T)", 0.5, 10.0, 3.0)
    S_local = st.slider("Local Entropy (S_local)", 0.0, 1.0, 0.2)
    E_harmonic = st.slider("Harmonic Energy (E_harmonic)", 0.0, 1.0, 0.5)

    D_unex = alpha * (T / B) - beta * E_harmonic + gamma * S_local
    tau_E = T / D_unex if D_unex > 0 else 0
    Q_ratio = T * tau_E / 10.0  # Simplified proxy

    col1, col2, col3 = st.columns(3)
    col1.metric("UN-EX D", f"{D_unex:.3f}")
    col2.metric("τ_E (s)", f"{tau_E:.3f}")
    col3.metric("Q Estimate", f"{Q_ratio:.2f}")

# --- Tab 2: Smart Mode ---
with tabs[1]:
    st.subheader("Smart Mode: Maximize Q")
    sweep_depth = st.slider("Sweep Depth", 3, 30, 10)

    best_Q = 0
    best_params = {}

    T_fixed = 5.0
    B_fixed = 3.0

    Q_map = []
    for E in np.linspace(0, 1.0, sweep_depth):
        for S in np.linspace(0, 1.0, sweep_depth):
            D = alpha * (T_fixed / B_fixed) - beta * E + gamma * S
            tau = T_fixed / D if D > 0 else 0
            Q = T_fixed * tau / 10.0
            Q_map.append((E, S, Q))
            if Q > best_Q:
                best_Q = Q
                best_params = {"E": E, "S": S, "Q": Q}

    st.write(f"🔎 Best Q: {best_Q:.2f} at E={best_params['E']:.2f}, S={best_params['S']:.2f}")

    fig2, ax2 = plt.subplots()
    E_vals = [x[0] for x in Q_map]
    S_vals = [x[1] for x in Q_map]
    Q_vals = [x[2] for x in Q_map]

    scatter = ax2.scatter(E_vals, S_vals, c=Q_vals, cmap="viridis")
    ax2.set_xlabel("E_harmonic")
    ax2.set_ylabel("S_local")
    ax2.set_title("Q Sweep Heatmap")
    fig2.colorbar(scatter, ax=ax2, label="Q Value")

    st.pyplot(fig2)

# --- Tab 3: Compare Classical Models ---
with tabs[2]:
    st.subheader("Compare UN-EX to Classical Models")

    D_bohm = T / B
    D_neo = T / (B**2)

    fig3, ax3 = plt.subplots()
    ax3.bar(["UN-EX", "Bohm", "Neoclassical"], [D_unex, D_bohm, D_neo],
            color=["cyan", "gray", "orange"])
    ax3.set_ylabel("Diffusion Coefficient (D)")
    ax3.set_title("Diffusion Model Comparison")

    st.pyplot(fig3)
