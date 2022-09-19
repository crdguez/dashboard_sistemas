from sympy import *

x, y, z, t = symbols('x y z t')

a, b, c, d, k = symbols('a b c d k', real = True)


def sistema_a_latex(sist) :
    """
    Convierte un sistema Sympy a código LaTeX
    """
    sist_latex = r"$\left\{ \begin{matrix}"
    for e in sist:
        sist_latex += latex(e)+r" \\ "  
    sist_latex += r"\end{matrix}\right.$"
    return(sist_latex)



def enunciado_dicusion(sist, k=k,lista=[]) :
    """
    Típico enunciado de discusión y resolución de un sistema con un parámetro
    """
    sistema_problema = sist
    texto_problema = r"""Considere el siguiente sistema de ecuaciones, dónde {}  es un parámetro real: $""".format(k)
    texto_problema += sistema_a_latex(sistema_problema)
    texto_problema += """$ Determine los valores del parámetro real {}, para los que este sistema es compatible determinado,  compatible indeterminado o incompatible.""".format(k)
    
    if lista :
        texto_problema +=r" \\ Resuelva el sistema cuando"
        texto_problema +=r"\begin{itemize}"
        for i in lista :
            texto_problema += r"\item {}={}".format(k,i)        
        texto_problema +=r"\end{itemize}"
    return(texto_problema)


def discusion_solucion(sist, k=k, resol=True) :
    """
    Discute y resuelve un sistema con un parámetro o sin él
    """
    d=dict()
    solucion_md=[]
    A, b = linear_eq_to_matrix(sist,[x,y,z])
    AA = A.row_join(b)
    AAs = AA.LUdecomposition()[1].applyfunc(nsimplify)
    
    if A.rank() < AA.rank():
        solucion_latex = r"Como $rg(A)={} < rg(A^*)={} \to$ S.I. \\ ".format(A.rank(),AA.rank())
        solucion_latex += r"Ya que escalonando la matriz ampliada: \\ $A^*= {} \thicksim {}$ \\".format(latex(AA),latex(AAs)).replace('[','(').replace(']',')')
        solucion_latex += r"${}={} \quad y \quad {}={}$".format(latex(AAs[:,:-1]),latex(A.det()),latex(AAs[:,1:]),latex(AAs[:,1:].det())).replace('[','|').replace(']','|')

    else :  
        pprint("Discusión y resolución por Gauss:")
        solucion_md.append("**Discusión y resolución por Gauss:** Escalonando la matriz ampliada tenemos")
        solucion_md.append(r"$A = {} \thicksim {}= A^*$.".format(latex(AA),latex(AAs)).replace('[','(').replace(']',')'))
        solucion_md.append("De los valores de la última fila podemos concluir:")
        solucion_md.append("* a ver")

        solucion_latex = r"\textbf{Discusión y resolución por Gauss:} Escalonando la matriz ampliada tenemos\\"
        solucion_latex += r"$A^*= {} \thicksim {}$. \\  De los valores de la última fila podemos concluir:".format(latex(AA),latex(AAs)).replace('[','(').replace(']',')')
        solucion_latex += r"\begin{itemize}"
        pprint(AAs)
                
        pprint("det(A)={}".format(A.det()))
        pprint(AAs.row(-1)[-2:])

        for i in (solve(AAs.row(-1)[-2])) :
            pprint(i)
            if AAs.row(-1)[-1].subs(k,i) == 0 :
                pprint("Si {} = {} -->  0z=0 --> S.C.I".format(k,i))
                solucion_md += r"* Si ${} = {} \to$ $${}$$ La última fila es $0z=0 \to $ S.C.I".format(k,i,latex(AAs.subs(k,i))).replace('[','(').replace(']',')')
                solucion_latex += r"\item Si ${} = {} \to$ $${}$$ La última fila es $0z=0 \to $ S.C.I".format(k,i,latex(AAs.subs(k,i))).replace('[','(').replace(']',')')
                pprint([eq.subs(k,i) for eq in sist])
                sol = list(zip([x,y,z],linsolve([eq.subs(k,i) for eq in sist],[x,y,z]).args[0],[r.subs(k,i) for r in [AAs.row(j) for j in range(AA.shape[0])]]))
                pprint(sol)
                for s in reversed(sol) :
                        pprint("{} --> {} = {}".format(s[2],s[0],s[1].subs(z,"\lambda")))
                        if resol :
                            solucion_latex += r"\begin{itemize}"
                            solucion_md += r"* ${} \to {} = {}$".format(latex(s[2]),latex(s[0]),latex(s[1]).replace('z',"\lambda")).replace('[','(').replace(']',')')
                            solucion_latex += r"\item ${} \to {} = {}$".format(latex(s[2]),latex(s[0]),latex(s[1]).replace('z',"\lambda")).replace('[','(').replace(']',')')
                            solucion_latex += r"\end{itemize}"
            else :
                pprint("Si {} = {} --> 0z={} -->S.I".format(k,i, AAs.row(-1)[-1].subs(k,i)))
                solucion_latex += r"\item Si ${} = {} \to$ $${}$$ La última fila es $0z={} \to $ S.I.".format(k,i,latex(AAs.subs(k,i)),AA.LUdecomposition()[1].applyfunc(simplify).row(-1)[-1].subs(k,i)).replace('[','(').replace(']',')')

        if solve(AAs.row(-1)[-2]) :
            pprint("si {} <> {}  --> S.C.D.".format(k, solve(AAs.row(-1)[-2])))
            solucion_latex += r"\item si ${}\neq {}  \to $ S.C.D.".format(k,solve(AAs.row(-1)[-2]))
        else :
            pprint("S.C.D.".format(k, solve(AAs.row(-1)[-2])))
            solucion_latex += r"\item S.C.D.".format(k,solve(AAs.row(-1)[-2]))


        pprint(list(linsolve(sist,[x,y,z]).args[0].args))
        sol = list(zip([x,y,z],linsolve(sist,[x,y,z]).args[0],[AAs.row(j) for j in range(AA.shape[0])]))
        pprint(sol)
        if resol :
            for s in reversed(sol) :
                pprint("{} --> {} = {}".format(s[2],s[0],s[1]))
                solucion_latex += r"\begin{itemize}"
                solucion_latex += r"\item ${} \to {} = {}$".format(latex(s[2]),s[0],latex(s[1])).replace('[','(').replace(']',')')
                solucion_latex += r"\end{itemize}"

        solucion_latex += r"\end{itemize}  "

        # Por rangos y determinantes

        pprint("Por rangos y determinantes:")
        solucion_latex += r"\textbf{Por rangos y determinantes:} \\"


        #Rango de A:


        solucion_latex += r"$\left|A\right|={}={} ".format(latex(A).replace("[","|").replace("]","|"),latex(A.det())) 
        if solve(A.det()) :
            solucion_latex += r"\to \left|A\right|=0 \quad si \quad {} = {}$".format(k,latex(solve(A.det())))
            solucion_latex += r"\begin{itemize}"
            for i in solve(A.det()):
                A2 = A.subs(k,i)
                AA2 = AA.subs(k,i)
                pprint(A2)
                pprint(A2.rank())
                pprint(AA2.rank())
                if A2.rank() < AA2.rank() :
                    pprint("Si {} = {} --> S.I.".format(k,i))
                    solucion_latex += r"\item Si ${}={} \to rg(A)={} \land rg(A^*)={} \to $ S.I.".format(k,i,A2.rank(),AA2.rank())
                else :
                    pprint("Si {} = {} --> S.C.I --> solo se puede resolver por Gauss, ver más arriba".format(k,i))
                    solucion_latex += r"\item Si ${}={} \to rg(A)={} \land rg(A^*)={} \to $ S.C.I. $\to$ solo se puede resolver por Gauss, (ver más arriba)".format(k,i,A2.rank(),AA2.rank())

            pprint("Si {} <> {} --> Rango(A)=Rango(A)={} --> S.C.D.".format(k,solve(A.det()),A.rank()))
            solucion_latex += r"\item Si ${} \neq{} \to rg(A)={} \land rg(A^*)={} \to $ S.C.D.  \\ ".format(k, solve(A.det()),A.rank(),AA.rank())
            if resol :
                pprint("Por Cramer:")
                sol=[]
                solucion_latex += r" \\ Por Cramer: \begin{itemize}"
                for i, var in enumerate([x,y,z]):
                    #print("columna"+latex(i))
                    AA.col_swap(i,3)
                    pprint("Delta_i, A.det, solucion_latex_i : ")
                    sol.append([var,AA[:,:-1],simplify(AA[:,:-1].det()),simplify(A.det()),simplify(AA[:,:-1].det()/A.det())])
                    pprint(sol[i])
                    #print(r"$x_"+latex(i)+r"=\frac{"+latex(AA[:,:-1])+r"}{"+latex(A.det())+r"}=\frac{"+latex(AA[:,:-1].det())+r"}{"+latex(A.det())+r"}="+latex(AA[:,:-1].det()/A.det())+"$")
                    solucion_latex += r"\item $"+latex(sol[i][0])+r"=\frac{"+latex(sol[i][1]).replace('[','|').replace(']','|')+r"}{"+latex(sol[i][3])+r"}=\frac{"+latex(sol[i][2])+r"}{"+latex(sol[i][3])+r"}="+latex(sol[i][4])+r"$"
                    AA.col_swap(i,3)
                solucion_latex += r"\end{itemize}"

        else:
            solucion_latex += r" \neq 0 $"
            solucion_latex += r"\begin{itemize}"
            solucion_latex += r" \item $rg(A)={} \land rg(A^*)={} \to $ S.C.D.   \\".format(A.rank(),AA.rank())
            if resol :
                pprint("Por Cramer:")
                sol=[]
                solucion_latex += r" \\ Por Cramer: \begin{itemize}"
                for i, var in enumerate([x,y,z]):
                    #print("columna"+latex(i))
                    AA.col_swap(i,3)
                    pprint("Delta_i, A.det, solucion_latex_i : ")
                    sol.append([var,AA[:,:-1],simplify(AA[:,:-1].det()),simplify(A.det()),simplify(AA[:,:-1].det()/A.det())])
                    pprint(sol[i])
                    #print(r"$x_"+latex(i)+r"=\frac{"+latex(AA[:,:-1])+r"}{"+latex(A.det())+r"}=\frac{"+latex(AA[:,:-1].det())+r"}{"+latex(A.det())+r"}="+latex(AA[:,:-1].det()/A.det())+"$")
                    solucion_latex += r"\item $"+latex(sol[i][0])+r"=\frac{"+latex(sol[i][1]).replace('[','|').replace(']','|')+r"}{"+latex(sol[i][3])+r"}=\frac{"+latex(sol[i][2])+r"}{"+latex(sol[i][3])+r"}="+latex(sol[i][4])+r"$"
                    AA.col_swap(i,3)
                solucion_latex += r"\end{itemize}"
        solucion_latex += r"\end{itemize}"
    d['solucion_latex']=solucion_latex
    d['solucion_markdown']=solucion_md
    return(d) 
