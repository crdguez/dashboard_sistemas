import streamlit as st
from funciones import *
from sympy import *

x, y, z, t = symbols('x y z t')

a, b, c, d, k = symbols('a b c d k', real = True)


st.title("Resolución de Sistemas de 2º bachillerato")

sist=[Eq(y+z,40),Eq(x,y+10),Eq(y-3*z,0)]
st.write("Dado el sistema:")
st.write(sistema_a_latex(sist))
# st.latex(latex(solve(sist)))


# st.write(discusion_solucion(sist2, k=k, resol=True))
st.write(discusion_solucion(sist, k=k, resol=True)['solucion_latex'])
st.latex(discusion_solucion(sist, k=k, resol=True)['solucion_latex'])


