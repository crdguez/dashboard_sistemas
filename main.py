import streamlit as st
from funciones import *
from sympy import *

x, y, z, t = symbols('x y z t')

a, b, c, d, k = symbols('a b c d k', real = True)


st.title("Resolución de Sistemas de 2º bachillerato")

st.info("Escribe el sistema en formato sympy. **Ejemplo:** [Eq(y+z,40),Eq(x,y+10),Eq(y-3*z,0)]")
sist=S(st.text_input("Sistema", value="[Eq(y+z,40),Eq(x,y+10),Eq(y-3*z,0)]"))

st.write(sist)
# sist=[Eq(y+z,40),Eq(x,y+10),Eq(y-3*z,0)]

st.write("Dado el sistema:")
st.write(sistema_a_latex(sist))
# st.latex(latex(solve(sist)))


# st.write(discusion_solucion(sist2, k=k, resol=True))
for linea in discusion_solucion(sist, k=k, resol=True)['solucion_markdown'] :
  st.write(linea)

# st.write(discusion_solucion(sist, k=k, resol=True)['solucion_markdown'])
st.latex(r"Discute y resuelve el siguiente sistema:  \\ " + \
         sistema_a_latex(sist))
st.latex(discusion_solucion(sist, k=k, resol=True)['solucion_latex'])
