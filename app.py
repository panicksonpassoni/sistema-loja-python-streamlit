from tinydb import TinyDB, where
import streamlit as st

db = TinyDB("loja.jason")

estoque = db.table("estoque")
vendas = db.table("vendas")

st.set_page_config(page_title="sistema loja", page_icon="🏪")
st.title("🏪 Sistema de loja")

aba_estoque, aba_cadastro, aba_vender, aba_vendas = st.tabs(
   ["Estoque", "Cadastrar", "Vender", "Vendas"]
)

with aba_estoque:
    st.header("Estoque atual")

    produtos = estoque.all()

    if len(produtos) == 0:
        st.info("Estoque vazio, cadastre um produto na aba ao lado!")
    else:
        st.table(produtos)
        st.metric("Total de produtos", len(produtos))

with aba_cadastro:
    st.header("Cadastrar produto")
    nome  = st.text_input("Nome", key="cad_nome")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.5, key="cad_preco")
    qtd   = st.number_input("Quantidade", min_value=0, step=1, key="cad_qtd")

    if st.button("Cadastrar", type="primary"):
        if nome.strip() == "":
            st.error("Digite o nome!")
        else:
            estoque.insert({
                "nome": nome, "preco": float(preco), "qtd": int(qtd)
            })
            st.success(f"✅ '{nome}' cadastrado!")



with aba_vender:
    st.header("Registrar venda")
    produtos = estoque.all()

    if len(produtos) == 0:
        st.info("Sem produtos para vender")

    else:
        st.header("Registrar venda")
        produtos = estoque.all()
        if len(produtos) == 0:
            st.info("Sem produtos pra vender.")
        else:
            nomes = [p["nome"] for p in produtos if p["qtd"] > 0]
            if len(nomes) == 0:
                st.warning("Tudo zerado!")
            else:
                escolhido = st.selectbox("Produto", nomes, key="v_prod")
                qtd_v = st.number_input("Qtd", min_value=1, step=1, key="v_qtd")
                cliente = st.text_input("Cliente", key="v_cli")

                produto = estoque.get(where("nome") == escolhido)
                total = produto["preco"] * qtd_v
                st.info(f"💰 Total: R$ {total:.2f}")

                if st.button("Confirmar venda", type="primary"):
                    vendas.insert({
                        "produto": escolhido, "qtd": int(qtd_v),
                        "total": total, "cliente": cliente
                    })
                    estoque.update(
                        {"qtd": produto["qtd"] - int(qtd_v)},
                        where("nome") == escolhido
                    )
                    st.success("✅ Venda registrada!")
                    st.balloons()



with aba_vendas:
    st.header("Histórico de vendas")
    lista = vendas.all()

    if len(lista) == 0:
        st.info("Sem vendas ainda.")
    else:
        st.table(lista)
        

