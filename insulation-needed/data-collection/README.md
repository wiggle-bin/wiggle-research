
# Understanding Box Temperature Regulation

To understand how well your box regulates temperature (like a house), focus on **thermal mass**, **thermal resistance**, **time constant (τ)**, and **t90**.

---

## 1. Thermal Mass (`C_total`)

- **Definition:** Amount of energy the contents can store per °C.  
- **Interpretation:**  
  - Large C → temperature changes slowly in response to outside fluctuations.  
  - Small C → temperature reacts quickly; little regulation.

**Example:**  
- Box with 5 L water + soil: C ≈ 40–50 kJ/K → changes slowly.  
- Box with air only: C ≈ 100 J/K → changes very fast.

---

## 2. Thermal Resistance (`R_total`)

- **Definition:** How much the box walls resist heat transfer.  
- **Interpretation:**  
  - High R → less heat lost → inside temperature changes slowly.  
  - Low R → heat flows easily → inside temperature quickly follows outside.

**Example:**  
- 50 mm wool: R ≈ 1.2 K/W → good insulation.  
- No insulation: R ≈ 0.1 K/W → poor insulation.

---

## 3. Time Constant (`τ`)

\[tau = C_\text{total} \cdot R_\text{total}\]

- **Definition:** Characteristic time for the box to respond to outside changes.  
- **Interpretation:**  
  - Large τ → box lags behind outside temperature; smooths swings.  
  - Small τ → box responds quickly; minimal regulation.

**Rule of thumb:**  
- τ ≈ 1 h → poor regulation  
- τ ≈ 10–20 h → moderate regulation (like a small house)  
- τ > 24 h → strong regulation; very slow changes

---

## 4. t90 (Time to Reach 90% of Change)

- **Definition:** Approximate time to reach 90% of a step change in outside temperature.  
- **Interpretation:**  
  - Short t90 → poor regulation; inside quickly follows outside.  
  - Long t90 → good regulation; inside changes slowly.

\[t_{90} \approx 2.303 \cdot \tau\]

**Example:**  
- τ = 6 h → t90 ≈ 14 h → box takes half a day to nearly reach outside temperature.  
- τ = 24 h → t90 ≈ 55 h → box hardly changes overnight.

---

## 5. Putting It All Together

| Property       | Effect on Temperature Regulation       | House Analogy                        |
|----------------|--------------------------------------|--------------------------------------|
| **C_total**    | Slows response; absorbs/releases heat | Thick walls, floors, furniture, water tanks |
| **R_total**    | Reduces heat loss/gain; slows response | Wall/roof insulation, double glazing |
| **τ (time constant)** | Combines mass & insulation; indicates lag | Overall thermal inertia of the building |
| **t90**        | Practical lag for ~90% change        | How long indoor temp takes to catch up to outside |

**Interpretation Guide:**

| τ or t90       | Regulation Level      | Notes |
|----------------|--------------------|-------|
| τ < 6 h        | Poor               | Box follows outdoor temperature closely |
| τ ≈ 10–20 h    | Moderate           | Buffers day/night swings (like a small house) |
| τ > 24 h       | Strong             | Very slow indoor temperature changes; excellent regulation |

## 6. CSV Columns Explanation

| Column Name       | Units    | Description |
|------------------|---------|-------------|
| `h_out (W/m2K)`  | W/m²·K | External convective heat transfer coefficient. Represents how quickly heat is lost to the surrounding air. Typical values: 5 W/m²·K (calm/sheltered), 10 W/m²·K (moderate wind). |
| `insulation (mm)` | mm      | Thickness of the insulation (sheep wool) around the box. Determines thermal resistance through the walls. |
| `water (L)`       | L       | Volume of water inside the box (optional thermal mass). Adds to the heat capacity of the contents. |
| `C_total (J/K)`   | J/K     | Total heat capacity of the box contents (soil + water + baseline material). Determines how much energy is needed to change the box temperature by 1 °C. |
| `R_total (K/W)`   | K/W     | Total thermal resistance of the box walls and convection combined: <br>`R_total = R_insulation + R_convection` <br>Higher R_total → slower heat loss. |
| `tau (s)`         | s       | **Time constant** of the system: <br>`tau = C_total * R_total` <br>Represents the characteristic time for the box temperature to respond to changes in outside temperature. |
| `tau (hours)`     | hours   | Time constant converted to hours (for convenience). |
| `t90 (hours)`     | hours   | Approximate time to reach **90% of the change** in box temperature due to an external step change: <br>`t90 ≈ -tau * ln(0.1) ≈ 2.303 * tau` <br>Useful to estimate how long the box “lags” behind outdoor temperature changes. |

## Summary

- **C_total:** how much energy the contents can store (thermal mass).  
- **R_total:** how well the box resists losing heat.  
- **tau:** combines mass and insulation to show response time.  
- **t90:** practical measure of “how long it takes for the box to almost reach outdoor temperature."

