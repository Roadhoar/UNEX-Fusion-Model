
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="UN-EX Fusion Dashboard", layout="wide")

st.title("🔬 UN-EX Plasma Confinement Simulation")
st.markdown("Interactively explore how temperature, magnetic field, entropy, and harmonic tuning affect plasma confinement.")

# Sliders
T = st.slider("Plasma Temperature (keV)", 1.0, 20.0, 5.0)
B = st.slider("Magnetic Field Strength (T)", 0.5, 10.0, 3.0)
S_local = st.slider("Local Entropy (S_local)", 0.0, 1.0, 0.2)
E_harmonic = st.slider("Harmonic Energy (E_harmonic)", 0.0, 1.0, 0.5)

# Constants
alpha = 1.0
beta = 1.0
gamma = 1.0

# UN-EX Diffusion and Energy Confinement Time
D_unex = alpha * (T / B) - beta * E_harmonic + gamma * S_local
tau_E = T / D_unex if D_unex > 0 else 0
Q_ratio = T * tau_E / 10.0  # Example proxy

# Classical Models
D_bohm = T / B
D_neo = T / (B**2)

# Plotting
fig, ax = plt.subplots()
labels = ["UN-EX", "Bohm", "Neoclassical"]
values = [D_unex, D_bohm, D_neo]
ax.bar(labels, values, color=["cyan", "gray", "orange"])
ax.set_ylabel("Diffusion Coefficient (D)")
ax.set_title("Diffusion Comparison")

st.pyplot(fig)

# Output Metrics
st.metric("UN-EX D", f"{D_unex:.3f}")
st.metric("Confinement Time (τ_E)", f"{tau_E:.3f} s")
st.metric("Estimated Q", f"{Q_ratio:.2f}")
