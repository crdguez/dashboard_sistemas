import streamlit as st
from funciones import *
from sympy import *

init_session()

a, b, c, d = symbols('a b c d', real = True)


st.title("Resolución de Sistemas de 2º bachillerato")

sist2=[Eq(y+z,40),Eq(x,y+10),Eq(y-3*z,0)]
st.write(discusion_solucion(sist2))


