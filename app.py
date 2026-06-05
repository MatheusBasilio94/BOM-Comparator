
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="BOM Comparison Tool", layout="wide")

st.title("BOM表对比工具 (BOM Comparison Tool)")
st.write("上传表格1和表格2以比较 位号 (Ref.) 和 料号 (Part Number).")

st.info("""
格式说明 (Format)

- 表格1 (Table 1): 每行一个位号 (One Ref. per row)
- 表格2 (Table 2): 多个位号在同一个单元格中，用逗号分隔 (Multiple Ref. in one cell separated by commas)

字段 (Fields):
- 位号 (Ref.)
- 料号 (Part Number)
""")

col1, col2 = st.columns(2)

with col1:
    arquivo1 = st.file_uploader(
        "上传表格1 (Upload Table 1)",
        type=["xlsx", "xls", "csv"],
        key="t1"
    )

with col2:
    arquivo2 = st.file_uploader(
        "上传表格2 (Upload Table 2)",
        type=["xlsx", "xls", "csv"],
        key="t2"
    )


def ler_arquivo(arquivo):
    if arquivo.name.lower().endswith(".csv"):
        return pd.read_csv(arquivo, dtype=str)
    return pd.read_excel(arquivo, dtype=str)


def limpar_nome_coluna(c):
    return str(c).replace("\n", " ").strip()


def normalizar_colunas(df):
    df = df.copy()
    df.columns = [limpar_nome_coluna(c) for c in df.columns]
    return df


def preparar_tabela1(df, col_ref, col_pn):
    saida = df[[col_ref, col_pn]].copy()
    saida.columns = ["位号 (Ref.)", "料号 (Part Number)"]
    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].astype(str).str.strip()
    saida["料号 (Part Number)"] = saida["料号 (Part Number)"].astype(str).str.strip()
    saida = saida[(saida["位号 (Ref.)"] != "") & (saida["位号 (Ref.)"].str.lower() != "nan")]
    saida = saida[(saida["料号 (Part Number)"] != "") & (saida["料号 (Part Number)"].str.lower() != "nan")]
    return saida.drop_duplicates()


def preparar_tabela2(df, col_ref, col_pn):
    saida = df[[col_ref, col_pn]].copy()
    saida.columns = ["位号 (Ref.)", "料号 (Part Number)"]

    # 多个位号用逗号分隔，并转换为多行
    # Split multiple Ref. separated by comma and transform into rows
    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].astype(str).str.split(",")
    saida = saida.explode("位号 (Ref.)")

    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].astype(str).str.strip()
    saida["料号 (Part Number)"] = saida["料号 (Part Number)"].astype(str).str.strip()
    saida = saida[(saida["位号 (Ref.)"] != "") & (saida["位号 (Ref.)"].str.lower() != "nan")]
    saida = saida[(saida["料号 (Part Number)"] != "") & (saida["料号 (Part Number)"].str.lower() != "nan")]
    return saida.drop_duplicates()


def comparar(t1, t2):
    t1 = t1.copy()
    t2 = t2.copy()

    t1["Key"] = t1["位号 (Ref.)"] + "|" + t1["料号 (Part Number)"]
    t2["Key"] = t2["位号 (Ref.)"] + "|" + t2["料号 (Part Number)"]

    chaves1 = set(t1["Key"])
    chaves2 = set(t2["Key"])

    ok = t1[t1["Key"].isin(chaves2)].copy()
    ok["Status"] = "匹配 (Match)"

    falta_t2 = t1[~t1["Key"].isin(chaves2)].copy()
    falta_t2["Status"] = "存在于表格1，但不存在于表格2 (Only in Table 1)"

    extra_t2 = t2[~t2["Key"].isin(chaves1)].copy()
    extra_t2["Status"] = "存在于表格2，但不存在于表格1 (Only in Table 2)"

    resultado = pd.concat([ok, falta_t2, extra_t2], ignore_index=True)
    resultado = resultado[["位号 (Ref.)", "料号 (Part Number)", "Status"]].sort_values(
        ["Status", "料号 (Part Number)", "位号 (Ref.)"]
    )
    return resultado


def gerar_excel(resultado, tabela1_normalizada, tabela2_normalizada):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        resultado.to_excel(writer, index=False, sheet_name="Comparison_Result")
        tabela1_normalizada.to_excel(writer, index=False, sheet_name="Table1_Normalized")
        tabela2_normalizada.to_excel(writer, index=False, sheet_name="Table2_Normalized")
    output.seek(0)
    return output


if arquivo1 and arquivo2:
    try:
        df1 = normalizar_colunas(ler_arquivo(arquivo1))
        df2 = normalizar_colunas(ler_arquivo(arquivo2))

        st.subheader("选择列 (Select Columns)")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**表格1 (Table 1)**")
            col_ref_t1 = st.selectbox("表格1位号列 (Ref. Column)", df1.columns, key="ref_t1")
            col_pn_t1 = st.selectbox("表格1料号列 (Part Number Column)", df1.columns, key="pn_t1")

        with c2:
            st.markdown("**表格2 (Table 2)**")
            col_ref_t2 = st.selectbox("表格2位号列 (Ref. Column)", df2.columns, key="ref_t2")
            col_pn_t2 = st.selectbox("表格2料号列 (Part Number Column)", df2.columns, key="pn_t2")

        with st.expander("查看上传文件 (Preview Uploaded Files)"):
            st.write("表格1 (Table 1)")
            st.dataframe(df1.head(20), use_container_width=True)
            st.write("表格2 (Table 2)")
            st.dataframe(df2.head(20), use_container_width=True)

        if st.button("开始比较 (Compare)", type="primary"):
            tabela1 = preparar_tabela1(df1, col_ref_t1, col_pn_t1)
            tabela2 = preparar_tabela2(df2, col_ref_t2, col_pn_t2)

            resultado = comparar(tabela1, tabela2)

            st.subheader("汇总 (Summary)")
            c1, c2, c3 = st.columns(3)
            c1.metric("匹配 (Match)", (resultado["Status"] == "匹配 (Match)").sum())
            c2.metric(
                "表格2缺少项目 (Missing in Table 2)",
                (resultado["Status"] == "存在于表格1，但不存在于表格2 (Only in Table 1)").sum()
            )
            c3.metric(
                "表格2多余项目 (Extra in Table 2)",
                (resultado["Status"] == "存在于表格2，但不存在于表格1 (Only in Table 2)").sum()
            )

            st.subheader("比较结果 (Comparison Result)")
            st.dataframe(resultado, use_container_width=True)

            excel = gerar_excel(resultado, tabela1, tabela2)
            st.download_button(
                label="下载Excel结果 (Download Excel Result)",
                data=excel,
                file_name="bom_comparison_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"处理文件时发生错误 (Error processing files): {e}")
else:
    st.warning("请上传两个文件以开始比较 (Please upload both files to start the comparison).")
