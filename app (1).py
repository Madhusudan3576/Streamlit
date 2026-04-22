import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Convergence Visualizer", layout="centered")

st.title("Algorithm Convergence Visualizer")

# -----------------------------
# USER INPUT
func = st.text_input("Enter function f(x)", "x**3 - x - 2")
dfunc = st.text_input("Enter derivative f'(x)", "3*x**2 - 1")
n_iter = st.slider("Iterations", 5, 20, 10)

def f(x):
    return eval(func)

def df(x):
    return eval(dfunc)

# -----------------------------
# AUTO INTERVAL FINDER
def find_interval(f, start=-10, end=10, step=0.5):
    x = start
    while x < end:
        try:
            if f(x) * f(x + step) < 0:
                return x, x + step
        except:
            pass
        x += step
    return None, None

a, b = find_interval(f)

if a is None:
    st.error("No valid interval found. Try different function.")
    st.stop()

st.success(f"Auto Interval Found: [{round(a,2)}, {round(b,2)}]")

# -----------------------------
# METHODS
def bisection(a, b, n):
    vals = []
    for _ in range(n):
        x = (a + b)/2
        vals.append(x)
        if f(a)*f(x) < 0:
            b = x
        else:
            a = x
    return vals

def regula(a, b, n):
    vals = []
    for _ in range(n):
        x = (a*f(b) - b*f(a)) / (f(b) - f(a))
        vals.append(x)
        if f(a)*f(x) < 0:
            b = x
        else:
            a = x
    return vals

def newton(x0, n):
    vals = []
    x = x0
    for _ in range(n):
        try:
            x = x - f(x)/df(x)
            vals.append(x)
        except:
            break
    return vals

x0 = (a + b)/2

b_vals = bisection(a,b,n_iter)
r_vals = regula(a,b,n_iter)
n_vals = newton(x0,n_iter)

# -----------------------------
# GRAPH 1: FUNCTION
st.subheader("Function Graph")

x = np.linspace(a-2, b+2, 200)
y = [f(i) for i in x]

fig1, ax1 = plt.subplots()
ax1.plot(x, y)
ax1.axhline(0)
ax1.set_title("f(x)")
ax1.set_xlabel("x (input value)")
ax1.set_ylabel("f(x) (function value)")
st.pyplot(fig1)

# -------- FUNCTION ANALYSIS --------
st.markdown("### Function Analysis")
st.write(f"""
- The function crosses the x-axis between **{round(a,2)} and {round(b,2)}**
- This confirms that a **root exists in this interval**
- Bisection and Regula Falsi require this condition
- Newton method starts from midpoint **{round(x0,2)}**
""")

# -----------------------------
# GRAPH 2: CONVERGENCE
st.subheader("Convergence Graph")

fig2, ax2 = plt.subplots()
ax2.plot(b_vals, label="Bisection")
ax2.plot(r_vals, label="Regula Falsi")
ax2.plot(n_vals, label="Newton")
ax2.legend()
ax2.set_title("Convergence")
ax2.set_xlabel("Iteration Number")
ax2.set_ylabel("Root Approximation")
st.pyplot(fig2)

# -------- SPEED ANALYSIS --------
st.markdown("### Convergence Speed Analysis")

def convergence_speed(vals):
    if len(vals) < 2:
        return float('inf')
    return abs(vals[-1] - vals[-2])

b_speed = convergence_speed(b_vals)
r_speed = convergence_speed(r_vals)
n_speed = convergence_speed(n_vals)

fastest = min(b_speed, r_speed, n_speed)

if fastest == n_speed:
    st.success("Newton Raphson converges fastest")
elif fastest == r_speed:
    st.success("Regula Falsi converges faster than Bisection")
else:
    st.success("Bisection is slowest but most stable")

st.write(f"""
- In this graph, the method whose curve becomes nearly horizontal in fewer iterations is converging faster  
- Newton stabilizes around iteration **{len(n_vals)}**, while others continue changing more gradually  
- Bisection shows smaller step-by-step changes, indicating slower convergence compared to the steeper approach of Newton  
""")

# -----------------------------
# GRAPH 3: ERROR
true_root = n_vals[-1] if len(n_vals)>0 else 0

def error(vals):
    return [abs(x-true_root) for x in vals]

st.subheader("Error Graph")

fig3, ax3 = plt.subplots()
ax3.plot(error(b_vals), label="Bisection")
ax3.plot(error(r_vals), label="Regula")
ax3.plot(error(n_vals), label="Newton")
ax3.legend()
ax3.set_title("Error Reduction")
ax3.set_xlabel("Iteration Number")
ax3.set_ylabel("Error (|approx - true root|)")
st.pyplot(fig3)

# -------- ERROR ANALYSIS --------
st.markdown("### Error Analysis")

def final_error(vals):
    return abs(vals[-1] - true_root) if vals else float('inf')

b_err = final_error(b_vals)
r_err = final_error(r_vals)
n_err = final_error(n_vals)

best = min(b_err, r_err, n_err)

if best == n_err:
    st.success("Newton has lowest error → most accurate")
elif best == r_err:
    st.success("Regula Falsi is more accurate than Bisection")
else:
    st.success("Bisection has highest error but guaranteed convergence")

st.write(f"""
- The curve that drops to near zero fastest represents the most accurate method  
- Newton’s error decreases sharply within the first few iterations, showing rapid accuracy improvement  
- Bisection’s error reduces gradually across iterations, indicating slower refinement of the root  
- A flatter curve near zero shows the method has already converged to a stable solution  
""")

# -----------------------------
# FINAL SUMMARY
st.subheader("Final Conclusion")

st.info("""
Newton → Fastest but needs derivative  
Regula Falsi → Balanced method  
Bisection → Slow but always converges  
""")