
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="BOM Comparison Tool", layout="wide")

st.markdown("""
<style>
.main-header {
    padding: 22px;
    border-radius: 14px;
    background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
    color: white;
    margin-bottom: 20px;
}
.main-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 6px;
}
.main-subtitle {
    font-size: 16px;
    color: #cbd5e1;
}
.section-card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #334155;
    background-color: #111827;
    margin-bottom: 18px;
}
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}
.section-text {
    color: #d1d5db;
    font-size: 14px;
}
.small-note {
    color: #94a3b8;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
        <div>
            <div class="main-title">Global BOM Comparator</div>
            <div class="main-subtitle">
                BOM表对比工具 (BOM Comparison Tool)<br>
                Compare BOM files by 位号 (Ref.) and 料号 (Part Number), including PN mismatch, missing items and extra items.
            </div>
        </div>
        <div style="text-align: right; min-width: 190px;">
            <div style="font-size: 14px; color: #cbd5e1; font-weight: 700;">SMT Quality & NPI</div>
            <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Version 1.3</div>
            <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Internal BOM Validation Tool</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="section-title">使用说明 (How to Use)</div>
    <div class="section-text">
        1. 上传表格1和表格2 (Upload Table 1 and Table 2)<br>
        2. 检查系统自动选择的列是否正确 (Check the automatically selected columns)<br>
        3. 点击开始比较 (Click Compare)<br>
        4. 查看结果并下载Excel报告 (Review results and download the Excel report)
    </div>
    <br>
    <div class="small-note">
        表格1 (Table 1): 每行一个位号 (One Ref. per row) | 
        表格2 (Table 2): 多个位号可在同一个单元格中，用逗号分隔 (Multiple Ref. in one cell separated by commas)
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("① 上传文件 (Upload Files)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**表格1 (Table 1)**")
    st.caption("Format: one Ref. per row + Part Number")
    arquivo1 = st.file_uploader(
        "上传表格1 (Upload Table 1)",
        type=["xlsx", "xls", "csv"],
        key="t1"
    )

with col2:
    st.markdown("**表格2 (Table 2)**")
    st.caption("Format: multiple Ref. may be separated by commas")
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


def encontrar_coluna_padrao(colunas, tipo):
    """
    Try to automatically identify the Ref. and Part Number columns.
    尝试自动识别位号列和料号列。
    """
    colunas_lista = list(colunas)

    if tipo == "ref":
        candidatos = [
            "ref", "ref.", "reference", "reference designator",
            "designator", "ref des", "refdes", "location",
            "位号", "位置", "器件位号"
        ]
    else:
        candidatos = [
            "part number", "part numbe", "partnumber", "part no",
            "part no.", "pn", "p/n", "material", "material number",
            "item number", "料号", "物料号", "物料编码", "物料代码"
        ]

    def limpar_texto(txt):
        return (
            str(txt)
            .lower()
            .replace(" ", "")
            .replace(".", "")
            .replace("_", "")
            .replace("-", "")
            .replace("/", "")
            .strip()
        )

    candidatos_limpos = [limpar_texto(c) for c in candidatos]

    for coluna in colunas_lista:
        coluna_limpa = limpar_texto(coluna)
        if coluna_limpa in candidatos_limpos:
            return colunas_lista.index(coluna)

    for coluna in colunas_lista:
        coluna_limpa = limpar_texto(coluna)
        for candidato in candidatos_limpos:
            if candidato in coluna_limpa or coluna_limpa in candidato:
                return colunas_lista.index(coluna)

    return 0


def limpar_tabela(saida):
    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].replace(
        ["", " ", "None", "none", "NONE", "nan", "NaN", "NAN", "<NA>"],
        pd.NA
    )

    saida = saida.dropna(subset=["位号 (Ref.)"])

    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].astype(str).str.strip()
    saida["料号 (Part Number)"] = saida["料号 (Part Number)"].astype(str).str.strip()

    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].replace(
        ["", " ", "None", "none", "NONE", "nan", "NaN", "NAN", "<NA>"],
        pd.NA
    )

    saida["料号 (Part Number)"] = saida["料号 (Part Number)"].replace(
        ["", " ", "None", "none", "NONE", "nan", "NaN", "NAN", "<NA>"],
        pd.NA
    )

    saida = saida.dropna(subset=["位号 (Ref.)", "料号 (Part Number)"])

    return saida


def preparar_tabela1(df, col_ref, col_pn):
    saida = df[[col_ref, col_pn]].copy()
    saida.columns = ["位号 (Ref.)", "料号 (Part Number)"]
    return limpar_tabela(saida)


def preparar_tabela2(df, col_ref, col_pn):
    saida = df[[col_ref, col_pn]].copy()
    saida.columns = ["位号 (Ref.)", "料号 (Part Number)"]

    saida["位号 (Ref.)"] = saida["位号 (Ref.)"].astype(str).str.split(",")
    saida = saida.explode("位号 (Ref.)")

    return limpar_tabela(saida)



def detectar_ref_duplicada(df, nome_tabela):
    """
    Detect duplicated Ref. within each normalized table.
    检测每个表格中的重复位号。
    """
    duplicados = df[df.duplicated(subset=["位号 (Ref.)"], keep=False)].copy()

    if duplicados.empty:
        return pd.DataFrame(columns=[
            "Table",
            "位号 (Ref.)",
            "Qty",
            "PN Count",
            "料号列表 (Part Number List)",
            "Issue"
        ])

    resumo = (
        duplicados
        .groupby("位号 (Ref.)")
        .agg(
            Qty=("位号 (Ref.)", "count"),
            **{
                "PN Count": ("料号 (Part Number)", lambda x: len(set(x.astype(str)))),
                "料号列表 (Part Number List)": ("料号 (Part Number)", lambda x: ", ".join(sorted(set(x.astype(str)))))
            }
        )
        .reset_index()
    )

    resumo.insert(0, "Table", nome_tabela)

    resumo["Issue"] = resumo["PN Count"].apply(
        lambda x: "严重重复位号-不同料号 (Critical Duplicate Ref. - Different PN)"
        if x > 1
        else "重复位号 (Duplicate Ref.)"
    )

    return resumo


def comparar(t1, t2):
    t1 = t1.copy().drop_duplicates()
    t2 = t2.copy().drop_duplicates()

    t1 = t1.rename(columns={"料号 (Part Number)": "PN_Tabela1"})
    t2 = t2.rename(columns={"料号 (Part Number)": "PN_Tabela2"})

    combinado = pd.merge(
        t1,
        t2,
        on="位号 (Ref.)",
        how="outer",
        indicator=True
    )

    def definir_status(row):
        if row["_merge"] == "left_only":
            return "存在于表格1，但不存在于表格2 (Only in Table 1)"
        elif row["_merge"] == "right_only":
            return "存在于表格2，但不存在于表格1 (Only in Table 2)"
        elif row["PN_Tabela1"] == row["PN_Tabela2"]:
            return "匹配 (Match)"
        else:
            return "料号不一致 (PN Mismatch)"

    combinado["Status"] = combinado.apply(definir_status, axis=1)

    resultado = combinado[[
        "位号 (Ref.)",
        "PN_Tabela1",
        "PN_Tabela2",
        "Status"
    ]].copy()

    resultado = resultado.sort_values(["Status", "位号 (Ref.)"])

    return resultado



def criar_issue_center(resultado, dup_tabela1, dup_tabela2):
    """
    Create a centralized issue list consolidating all BOM problems.
    创建问题中心，整合所有BOM问题。
    """
    issues = []

    missing_status = "存在于表格1，但不存在于表格2 (Only in Table 1)"
    extra_status = "存在于表格2，但不存在于表格1 (Only in Table 2)"
    mismatch_status = "料号不一致 (PN Mismatch)"

    for _, row in resultado.iterrows():
        if row["Status"] == mismatch_status:
            issues.append({
                "Issue Type": "PN Mismatch",
                "问题类型": "料号不一致",
                "Table": "Table 1 vs Table 2",
                "位号 (Ref.)": row["位号 (Ref.)"],
                "PN Table 1": row["PN_Tabela1"],
                "PN Table 2": row["PN_Tabela2"],
                "Details": f'{row["PN_Tabela1"]} → {row["PN_Tabela2"]}',
                "Severity": "High"
            })

        elif row["Status"] == missing_status:
            issues.append({
                "Issue Type": "Missing in Table 2",
                "问题类型": "表格2缺少项目",
                "Table": "Table 1",
                "位号 (Ref.)": row["位号 (Ref.)"],
                "PN Table 1": row["PN_Tabela1"],
                "PN Table 2": "",
                "Details": "Exists in Table 1, but not in Table 2",
                "Severity": "Medium"
            })

        elif row["Status"] == extra_status:
            issues.append({
                "Issue Type": "Extra in Table 2",
                "问题类型": "表格2多余项目",
                "Table": "Table 2",
                "位号 (Ref.)": row["位号 (Ref.)"],
                "PN Table 1": "",
                "PN Table 2": row["PN_Tabela2"],
                "Details": "Exists in Table 2, but not in Table 1",
                "Severity": "Medium"
            })

    duplicate_all = pd.concat([dup_tabela1, dup_tabela2], ignore_index=True)

    for _, row in duplicate_all.iterrows():
        issue_type = (
            "Critical Duplicate Ref. - Different PN"
            if row["Issue"] == "严重重复位号-不同料号 (Critical Duplicate Ref. - Different PN)"
            else "Duplicate Ref."
        )
        severity = "Critical" if issue_type.startswith("Critical") else "Medium"

        issues.append({
            "Issue Type": issue_type,
            "问题类型": row["Issue"],
            "Table": row["Table"],
            "位号 (Ref.)": row["位号 (Ref.)"],
            "PN Table 1": "",
            "PN Table 2": "",
            "Details": f'Qty={row["Qty"]}; PN List={row["料号列表 (Part Number List)"]}',
            "Severity": severity
        })

    return pd.DataFrame(issues, columns=[
        "Issue Type",
        "问题类型",
        "Table",
        "位号 (Ref.)",
        "PN Table 1",
        "PN Table 2",
        "Details",
        "Severity"
    ])


def gerar_excel(resultado, tabela1_normalizada, tabela2_normalizada, dup_tabela1, dup_tabela2, issues_df):
    output = BytesIO()

    match_status = "匹配 (Match)"
    missing_status = "存在于表格1，但不存在于表格2 (Only in Table 1)"
    extra_status = "存在于表格2，但不存在于表格1 (Only in Table 2)"
    mismatch_status = "料号不一致 (PN Mismatch)"

    match_df = resultado[resultado["Status"] == match_status].copy()
    missing_df = resultado[resultado["Status"] == missing_status].copy()
    extra_df = resultado[resultado["Status"] == extra_status].copy()
    mismatch_df = resultado[resultado["Status"] == mismatch_status].copy()

    total_count = len(resultado)
    match_count = len(match_df)
    missing_count = len(missing_df)
    extra_count = len(extra_df)
    mismatch_count = len(mismatch_df)
    duplicate_t1_count = len(dup_tabela1)
    duplicate_t2_count = len(dup_tabela2)
    duplicate_total_count = duplicate_t1_count + duplicate_t2_count
    total_issues_count = len(issues_df)
    critical_issues_count = (issues_df["Severity"] == "Critical").sum() if not issues_df.empty else 0
    high_issues_count = (issues_df["Severity"] == "High").sum() if not issues_df.empty else 0
    match_rate = (match_count / total_count * 100) if total_count > 0 else 0

    summary_df = pd.DataFrame({
        "Item": [
            "Total Items",
            "Match",
            "Match Rate",
            "Missing in Table 2",
            "Extra in Table 2",
            "PN Mismatch",
            "Duplicate Ref. Table 1",
            "Duplicate Ref. Table 2",
            "Duplicate Ref. Total",
            "Total Issues",
            "Critical Issues",
            "High Issues"
        ],
        "项目": [
            "总项目数",
            "匹配",
            "匹配率",
            "表格2缺少项目",
            "表格2多余项目",
            "料号不一致",
            "表格1重复位号",
            "表格2重复位号",
            "重复位号总数",
            "问题总数",
            "严重问题",
            "高风险问题"
        ],
        "Qty / Value": [
            total_count,
            match_count,
            f"{match_rate:.2f}%",
            missing_count,
            extra_count,
            mismatch_count,
            duplicate_t1_count,
            duplicate_t2_count,
            duplicate_total_count,
            total_issues_count,
            critical_issues_count,
            high_issues_count
        ]
    })

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_df.to_excel(writer, index=False, sheet_name="Summary")
        issues_df.to_excel(writer, index=False, sheet_name="Issues")
        match_df.to_excel(writer, index=False, sheet_name="Match")
        missing_df.to_excel(writer, index=False, sheet_name="Missing")
        extra_df.to_excel(writer, index=False, sheet_name="Extra")
        mismatch_df.to_excel(writer, index=False, sheet_name="PN_Mismatch")
        dup_tabela1.to_excel(writer, index=False, sheet_name="Duplicate_Ref_T1")
        dup_tabela2.to_excel(writer, index=False, sheet_name="Duplicate_Ref_T2")
        resultado.to_excel(writer, index=False, sheet_name="All_Results")
        tabela1_normalizada.to_excel(writer, index=False, sheet_name="Table1_Normalized")
        tabela2_normalizada.to_excel(writer, index=False, sheet_name="Table2_Normalized")

        workbook = writer.book

        for sheet_name in workbook.sheetnames:
            ws = workbook[sheet_name]

            # Ajustar largura das colunas automaticamente
            for column_cells in ws.columns:
                max_length = 0
                column_letter = column_cells[0].column_letter

                for cell in column_cells:
                    try:
                        value_length = len(str(cell.value)) if cell.value is not None else 0
                        if value_length > max_length:
                            max_length = value_length
                    except Exception:
                        pass

                ws.column_dimensions[column_letter].width = min(max_length + 3, 45)

            # Congelar cabeçalho
            ws.freeze_panes = "A2"

            # Aplicar filtro no cabeçalho
            if ws.max_row > 1 and ws.max_column > 1:
                ws.auto_filter.ref = ws.dimensions

    output.seek(0)
    return output


if arquivo1 and arquivo2:
    try:
        df1 = normalizar_colunas(ler_arquivo(arquivo1))
        df2 = normalizar_colunas(ler_arquivo(arquivo2))

        st.subheader("② 选择列 (Select Columns)")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**表格1 (Table 1)**")
            col_ref_t1 = st.selectbox(
                "表格1位号列 (Ref. Column)",
                df1.columns,
                index=encontrar_coluna_padrao(df1.columns, "ref"),
                key="ref_t1"
            )
            col_pn_t1 = st.selectbox(
                "表格1料号列 (Part Number Column)",
                df1.columns,
                index=encontrar_coluna_padrao(df1.columns, "pn"),
                key="pn_t1"
            )

        with c2:
            st.markdown("**表格2 (Table 2)**")
            col_ref_t2 = st.selectbox(
                "表格2位号列 (Ref. Column)",
                df2.columns,
                index=encontrar_coluna_padrao(df2.columns, "ref"),
                key="ref_t2"
            )
            col_pn_t2 = st.selectbox(
                "表格2料号列 (Part Number Column)",
                df2.columns,
                index=encontrar_coluna_padrao(df2.columns, "pn"),
                key="pn_t2"
            )

        st.caption("系统会自动建议列名，但如果选择不正确，用户仍然可以手动更改。 (The system suggests columns automatically, but you can still change them manually.)")

        with st.expander("查看上传文件 (Preview Uploaded Files)"):
            st.write("表格1 (Table 1)")
            st.dataframe(df1.head(20), use_container_width=True)
            st.write("表格2 (Table 2)")
            st.dataframe(df2.head(20), use_container_width=True)

        st.divider()

        if st.button("开始比较 (Compare)", type="primary", use_container_width=True):
            tabela1 = preparar_tabela1(df1, col_ref_t1, col_pn_t1)
            tabela2 = preparar_tabela2(df2, col_ref_t2, col_pn_t2)

            dup_tabela1 = detectar_ref_duplicada(tabela1, "Table 1")
            dup_tabela2 = detectar_ref_duplicada(tabela2, "Table 2")

            resultado = comparar(tabela1, tabela2)
            issues_df = criar_issue_center(resultado, dup_tabela1, dup_tabela2)

            st.subheader("③ 汇总 (Executive Summary)")

            match_count = (resultado["Status"] == "匹配 (Match)").sum()
            missing_count = (resultado["Status"] == "存在于表格1，但不存在于表格2 (Only in Table 1)").sum()
            extra_count = (resultado["Status"] == "存在于表格2，但不存在于表格1 (Only in Table 2)").sum()
            mismatch_count = (resultado["Status"] == "料号不一致 (PN Mismatch)").sum()
            duplicate_count = len(dup_tabela1) + len(dup_tabela2)
            total_issues_count = len(issues_df)
            critical_duplicate_count = (
                (issues_df["Issue Type"] == "Critical Duplicate Ref. - Different PN").sum()
                if not issues_df.empty else 0
            )
            total_count = len(resultado)
            match_rate = (match_count / total_count * 100) if total_count > 0 else 0

            st.markdown(f"""
            <style>
            .metric-card {{
                padding: 18px;
                border-radius: 12px;
                background-color: #1f2937;
                border: 1px solid #374151;
                text-align: center;
                margin-bottom: 10px;
            }}
            .metric-title {{
                font-size: 14px;
                color: #d1d5db;
                margin-bottom: 8px;
                font-weight: 600;
            }}
            .metric-value {{
                font-size: 30px;
                color: white;
                font-weight: 700;
            }}
            .green {{ border-left: 6px solid #22c55e; }}
            .blue {{ border-left: 6px solid #3b82f6; }}
            .yellow {{ border-left: 6px solid #facc15; }}
            .red {{ border-left: 6px solid #ef4444; }}
            .purple {{ border-left: 6px solid #a855f7; }}
            </style>

            <div style="display: grid; grid-template-columns: repeat(9, 1fr); gap: 12px;">
                <div class="metric-card blue">
                    <div class="metric-title">总项目数 (Total Items)</div>
                    <div class="metric-value">{total_count}</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-title">匹配 (Match)</div>
                    <div class="metric-value">{match_count}</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-title">匹配率 (Match Rate)</div>
                    <div class="metric-value">{match_rate:.2f}%</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">表格2缺少 (Missing)</div>
                    <div class="metric-value">{missing_count}</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">表格2多余 (Extra)</div>
                    <div class="metric-value">{extra_count}</div>
                </div>
                <div class="metric-card red">
                    <div class="metric-title">料号不一致 (PN Mismatch)</div>
                    <div class="metric-value">{mismatch_count}</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">重复位号 (Duplicate Ref.)</div>
                    <div class="metric-value">{duplicate_count}</div>
                </div>
                <div class="metric-card red">
                    <div class="metric-title">严重重复 (Critical Dup.)</div>
                    <div class="metric-value">{critical_duplicate_count}</div>
                </div>
                <div class="metric-card purple">
                    <div class="metric-title">问题总数 (Total Issues)</div>
                    <div class="metric-value">{total_issues_count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if total_issues_count == 0:
                st.success("结果: 两个BOM完全匹配，未发现问题 (Result: Both BOMs are fully matched. No issues found).")
            elif critical_duplicate_count > 0:
                st.error("结果: 发现严重重复位号且料号不同，请优先检查Critical Duplicate项目 (Result: Critical duplicate Ref. with different PN found. Please review first).")
            elif mismatch_count > 0:
                st.error("结果: 发现料号不一致，请优先检查PN Mismatch项目 (Result: PN mismatch found. Please review first).")
            elif duplicate_count > 0:
                st.warning("结果: 发现重复位号，请检查Duplicate Ref.项目 (Result: Duplicate Ref. found. Please review).")
            else:
                st.warning("结果: 发现缺失或多余项目，请检查差异 (Result: Missing or extra items found. Please review differences).")

            if total_issues_count > 0:
                st.subheader("问题中心 (Issue Center)")
                st.dataframe(issues_df, use_container_width=True)

            if duplicate_count > 0:
                st.subheader("重复位号检查 (Duplicate Ref. Check)")
                duplicate_all = pd.concat([dup_tabela1, dup_tabela2], ignore_index=True)
                st.dataframe(duplicate_all, use_container_width=True)

            st.subheader("④ 比较结果 (Comparison Result)")
            st.dataframe(resultado, use_container_width=True)

            excel = gerar_excel(resultado, tabela1, tabela2, dup_tabela1, dup_tabela2, issues_df)
            st.download_button(
                label="📥 下载Excel报告 (Download Excel Report)",
                data=excel,
                file_name="bom_comparison_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"处理文件时发生错误 (Error processing files): {e}")
else:
    st.warning("请上传两个文件以开始比较 (Please upload both files to start the comparison).")

st.markdown("""
<hr style="margin-top: 28px; margin-bottom: 10px; border: 0; border-top: 1px solid #334155;">
<div style="text-align: center; color: #94a3b8; font-size: 12px;">
    Global BOM Comparator | Version 1.3 | SMT Quality & NPI | 位号 (Ref.) + 料号 (Part Number)
</div>
""", unsafe_allow_html=True)

