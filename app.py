
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="BOM Comparator Tool", layout="wide")

# ============================================================
# Language selector with real flag images
# ============================================================

def render_language_selector(current_lang):
    selected_pt = "selected-flag" if current_lang == "pt" else ""
    selected_en = "selected-flag" if current_lang == "en" else ""
    selected_cn = "selected-flag" if current_lang == "cn" else ""

    st.markdown("""
<style>
.language-title {
    font-size: 14px;
    font-weight: 700;
    color: #e5e7eb;
    margin-bottom: 8px;
}
.flag-display-card {
    width: 74px;
    height: 52px;
    border-radius: 9px;
    border: 1px solid #334155;
    background: rgba(15, 23, 42, 0.92);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 6px;
    box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.08);
}
.flag-display-card.selected-flag {
    border: 2px solid #0ea5e9;
    box-shadow: 0 0 16px rgba(14, 165, 233, 0.58);
}
.flag-svg {
    width: 54px;
    height: 36px;
    border-radius: 2px;
    display: block;
}
.selected-lang {
    border: 1px solid #0ea5e9;
    border-radius: 8px;
    padding: 6px 10px;
    color: #38bdf8;
    display: inline-block;
    margin-top: 4px;
    margin-bottom: 10px;
    font-size: 12px;
    font-weight: 700;
    background: rgba(14, 165, 233, 0.12);
}
div[data-testid="stHorizontalBlock"] button {
    min-height: 34px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: rgba(15, 23, 42, 0.92);
    color: #f8fafc;
    font-size: 12px;
    font-weight: 800;
    transition: 0.15s ease-in-out;
}
div[data-testid="stHorizontalBlock"] button:hover {
    border-color: #38bdf8;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.35);
    transform: translateY(-1px);
}
</style>
<div class="language-title">🌐 Idioma / Language / 语言</div>
""", unsafe_allow_html=True)

    lang_cols = st.columns([0.55, 0.55, 0.55, 6])

    with lang_cols[0]:
        st.markdown(f"""
<div class="flag-display-card {selected_pt}">
<svg class="flag-svg" viewBox="0 0 90 60" xmlns="http://www.w3.org/2000/svg">
<rect width="90" height="60" fill="#009b3a"/>
<path d="M45 6 L84 30 L45 54 L6 30 Z" fill="#ffdf00"/>
<circle cx="45" cy="30" r="13" fill="#002776"/>
<path d="M32 27 C40 24, 52 24, 59 31" stroke="#fff" stroke-width="3" fill="none"/>
</svg>
</div>
""", unsafe_allow_html=True)
        if st.button("PT", key="lang_pt", help="Português", use_container_width=True):
            st.session_state.lang = "pt"
            st.rerun()

    with lang_cols[1]:
        st.markdown(f"""
<div class="flag-display-card {selected_en}">
<svg class="flag-svg" viewBox="0 0 90 60" xmlns="http://www.w3.org/2000/svg">
<rect width="90" height="60" fill="#b22234"/>
<g fill="#fff">
<rect y="4.62" width="90" height="4.62"/>
<rect y="13.85" width="90" height="4.62"/>
<rect y="23.08" width="90" height="4.62"/>
<rect y="32.31" width="90" height="4.62"/>
<rect y="41.54" width="90" height="4.62"/>
<rect y="50.77" width="90" height="4.62"/>
</g>
<rect width="38" height="32.3" fill="#3c3b6e"/>
<g fill="#fff">
<circle cx="6" cy="5" r="1.3"/><circle cx="13" cy="5" r="1.3"/><circle cx="20" cy="5" r="1.3"/><circle cx="27" cy="5" r="1.3"/><circle cx="34" cy="5" r="1.3"/>
<circle cx="9.5" cy="10" r="1.3"/><circle cx="16.5" cy="10" r="1.3"/><circle cx="23.5" cy="10" r="1.3"/><circle cx="30.5" cy="10" r="1.3"/>
<circle cx="6" cy="15" r="1.3"/><circle cx="13" cy="15" r="1.3"/><circle cx="20" cy="15" r="1.3"/><circle cx="27" cy="15" r="1.3"/><circle cx="34" cy="15" r="1.3"/>
<circle cx="9.5" cy="20" r="1.3"/><circle cx="16.5" cy="20" r="1.3"/><circle cx="23.5" cy="20" r="1.3"/><circle cx="30.5" cy="20" r="1.3"/>
<circle cx="6" cy="25" r="1.3"/><circle cx="13" cy="25" r="1.3"/><circle cx="20" cy="25" r="1.3"/><circle cx="27" cy="25" r="1.3"/><circle cx="34" cy="25" r="1.3"/>
</g>
</svg>
</div>
""", unsafe_allow_html=True)
        if st.button("EN", key="lang_en", help="English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()

    with lang_cols[2]:
        st.markdown(f"""
<div class="flag-display-card {selected_cn}">
<svg class="flag-svg" viewBox="0 0 90 60" xmlns="http://www.w3.org/2000/svg">
<rect width="90" height="60" fill="#de2910"/>
<polygon points="18,8 20.9,16.5 30,16.5 22.6,21.8 25.5,30 18,24.9 10.5,30 13.4,21.8 6,16.5 15.1,16.5" fill="#ffde00"/>
<polygon points="37,7 38.5,11 42.8,11.1 39.3,13.5 40.7,17.6 37,15.2 33.4,17.6 34.7,13.5 31.3,11.1 35.5,11" fill="#ffde00"/>
<polygon points="49,16 50.2,19.5 54,19.5 50.9,21.7 52.1,25.2 49,23.1 45.9,25.2 47.1,21.7 44,19.5 47.8,19.5" fill="#ffde00"/>
<polygon points="49,31 50.2,34.5 54,34.5 50.9,36.7 52.1,40.2 49,38.1 45.9,40.2 47.1,36.7 44,34.5 47.8,34.5" fill="#ffde00"/>
<polygon points="37,42 38.2,45.5 42,45.5 38.9,47.7 40.1,51.2 37,49.1 33.9,51.2 35.1,47.7 32,45.5 35.8,45.5" fill="#ffde00"/>
</svg>
</div>
""", unsafe_allow_html=True)
        if st.button("CN", key="lang_cn", help="中文", use_container_width=True):
            st.session_state.lang = "cn"
            st.rerun()

    label = {
        "pt": "Português selecionado",
        "en": "English selected",
        "cn": "中文已选择"
    }.get(current_lang, "English selected")

    st.markdown(f'<div class="selected-lang">{label}</div>', unsafe_allow_html=True)



# ============================================================
# Global BOM Comparator v1.4 - International Edition
# Languages: Portuguese, English, Chinese
# ============================================================

TEXT = {
    "pt": {
        "language": "Idioma",
        "app_title": "BOM Comparator Tool",
        "app_subtitle": "Compare arquivos BOM por Ref. e Part Number, incluindo PN divergente, itens faltantes, itens extras e duplicidades.",
        "area": "Quality Specialist",
        "version": "Versão 1.5.16",
        "tool_type": "Developed by Matheus Augusto de Lima Basilio",
        "how_to_use": "Como usar",
        "step1": "1. Carregue a Tabela 1 e a Tabela 2",
        "step2": "2. Verifique se as colunas selecionadas automaticamente estão corretas",
        "step3": "3. Clique em Comparar",
        "step4": "4. Revise os resultados e baixe o relatório em Excel",
        "note": "Tabela 1: uma Ref. por linha | Tabela 2: múltiplas Ref. podem estar na mesma célula, separadas por vírgula",
        "upload_files": "① Carregar arquivos",
        "table1": "Tabela 1",
        "table2": "Tabela 2",
        "table1_caption": "Formato: uma Ref. por linha + Part Number",
        "table2_caption": "Formato: múltiplas Ref. podem estar separadas por vírgula",
        "upload_table1": "Carregar Tabela 1",
        "upload_table2": "Carregar Tabela 2",
        "select_columns": "② Selecionar colunas",
        "ref_col_t1": "Coluna Ref. da Tabela 1",
        "pn_col_t1": "Coluna Part Number da Tabela 1",
        "ref_col_t2": "Coluna Ref. da Tabela 2",
        "pn_col_t2": "Coluna Part Number da Tabela 2",
        "auto_col_note": "O sistema sugere as colunas automaticamente, mas você ainda pode alterar manualmente.",
        "preview_files": "Visualizar arquivos carregados",
        "compare": "Comparar",
        "summary": "③ Resumo Executivo",
        "total_items": "Total de Itens",
        "match": "Match",
        "match_rate": "Match Rate",
        "missing": "Faltando na Tabela 2",
        "extra": "Extra na Tabela 2",
        "pn_mismatch": "PN Divergente",
        "duplicate_ref": "Ref. Duplicada",
        "critical_dup": "Duplicidade Crítica",
        "total_issues": "Total de Problemas",
        "result_ok": "Resultado: As duas BOMs estão totalmente equivalentes. Nenhum problema encontrado.",
        "result_critical": "Resultado: Foi encontrada Ref. duplicada crítica com PN diferente. Verifique primeiro os itens Critical Duplicate.",
        "result_mismatch": "Resultado: Foi encontrado PN divergente. Verifique primeiro os itens PN Mismatch.",
        "result_duplicate": "Resultado: Foram encontradas referências duplicadas. Verifique os itens Duplicate Ref.",
        "result_missing_extra": "Resultado: Foram encontrados itens faltantes ou extras. Verifique as diferenças.",
        "issue_center": "Central de Problemas",
        "duplicate_check": "Verificação de Ref. Duplicada",
        "comparison_result": "④ Resultado da Comparação",
        "download_excel": "📥 Baixar Relatório Excel",
        "processing_error": "Erro ao processar os arquivos",
        "upload_warning": "Carregue os dois arquivos para iniciar a comparação.",
        "footer": "BOM Comparator Tool | Version 1.5.16<br><br>Developed by Matheus Augusto de Lima Basilio<br>Quality Specialist | Matheus.Augusto@jovimobile.com<br>© 2026 Matheus Augusto de Lima Basilio",
        "filters": "Filtros e Busca",
        "result_filter": "Filtrar resultado",
        "issue_filter": "Filtrar problemas por severidade",
        "search": "Pesquisar Ref. ou Part Number",
        "all": "Todos",
        "all_issues": "Todas",
        "no_result": "Nenhum resultado encontrado com os filtros aplicados.",
        "issue_filters": "🚨 Filtros da Central de Problemas",
        "comparison_filters": "🔍 Filtros da Comparação",
        "issue_filter_note": "ℹ️ Este filtro afeta apenas a Central de Problemas.",
        "comparison_filter_note": "ℹ️ Estes filtros afetam o Resultado da Comparação e a busca nas tabelas exibidas.",
        "drag_drop": "📁 Arraste o arquivo aqui ou clique para selecionar",
        "supported_files": "Formatos aceitos: XLSX, XLS e CSV"
    },
    "en": {
        "language": "Language",
        "app_title": "BOM Comparator Tool",
        "app_subtitle": "Compare BOM files by Ref. and Part Number, including PN mismatch, missing items, extra items and duplicates.",
        "area": "Quality Specialist",
        "version": "Version 1.5.16",
        "tool_type": "Developed by Matheus Augusto de Lima Basilio",
        "how_to_use": "How to Use",
        "step1": "1. Upload Table 1 and Table 2",
        "step2": "2. Check if the automatically selected columns are correct",
        "step3": "3. Click Compare",
        "step4": "4. Review the results and download the Excel report",
        "note": "Table 1: one Ref. per row | Table 2: multiple Ref. may be in the same cell, separated by commas",
        "upload_files": "① Upload Files",
        "table1": "Table 1",
        "table2": "Table 2",
        "table1_caption": "Format: one Ref. per row + Part Number",
        "table2_caption": "Format: multiple Ref. may be separated by commas",
        "upload_table1": "Upload Table 1",
        "upload_table2": "Upload Table 2",
        "select_columns": "② Select Columns",
        "ref_col_t1": "Table 1 Ref. Column",
        "pn_col_t1": "Table 1 Part Number Column",
        "ref_col_t2": "Table 2 Ref. Column",
        "pn_col_t2": "Table 2 Part Number Column",
        "auto_col_note": "The system suggests columns automatically, but you can still change them manually.",
        "preview_files": "Preview Uploaded Files",
        "compare": "Compare",
        "summary": "③ Executive Summary",
        "total_items": "Total Items",
        "match": "Match",
        "match_rate": "Match Rate",
        "missing": "Missing in Table 2",
        "extra": "Extra in Table 2",
        "pn_mismatch": "PN Mismatch",
        "duplicate_ref": "Duplicate Ref.",
        "critical_dup": "Critical Dup.",
        "total_issues": "Total Issues",
        "result_ok": "Result: Both BOMs are fully matched. No issues found.",
        "result_critical": "Result: Critical duplicate Ref. with different PN found. Please review Critical Duplicate first.",
        "result_mismatch": "Result: PN mismatch found. Please review PN Mismatch first.",
        "result_duplicate": "Result: Duplicate Ref. found. Please review Duplicate Ref.",
        "result_missing_extra": "Result: Missing or extra items found. Please review differences.",
        "issue_center": "Issue Center",
        "duplicate_check": "Duplicate Ref. Check",
        "comparison_result": "④ Comparison Result",
        "download_excel": "📥 Download Excel Report",
        "processing_error": "Error processing files",
        "upload_warning": "Please upload both files to start the comparison.",
        "footer": "BOM Comparator Tool | Version 1.5.16<br><br>Developed by Matheus Augusto de Lima Basilio<br>Quality Specialist | Matheus.Augusto@jovimobile.com<br>© 2026 Matheus Augusto de Lima Basilio",
        "filters": "Filters and Search",
        "result_filter": "Filter result",
        "issue_filter": "Filter issues by severity",
        "search": "Search Ref. or Part Number",
        "all": "All",
        "all_issues": "All",
        "no_result": "No results found with the applied filters.",
        "issue_filters": "🚨 Issue Center Filters",
        "comparison_filters": "🔍 Comparison Filters",
        "issue_filter_note": "ℹ️ This filter affects only the Issue Center.",
        "comparison_filter_note": "ℹ️ These filters affect the Comparison Result and search across displayed tables.",
        "drag_drop": "📁 Drag and drop the file here or click to browse",
        "supported_files": "Supported formats: XLSX, XLS and CSV"
    },
    "cn": {
        "language": "语言",
        "app_title": "BOM Comparator Tool",
        "app_subtitle": "通过位号和料号对比BOM文件，包括料号不一致、缺失项目、多余项目和重复位号。",
        "area": "Quality Specialist",
        "version": "版本 1.5.16",
        "tool_type": "Developed by Matheus Augusto de Lima Basilio",
        "how_to_use": "使用说明",
        "step1": "1. 上传表格1和表格2",
        "step2": "2. 检查系统自动选择的列是否正确",
        "step3": "3. 点击开始比较",
        "step4": "4. 查看结果并下载Excel报告",
        "note": "表格1：每行一个位号 | 表格2：多个位号可在同一个单元格中，用逗号分隔",
        "upload_files": "① 上传文件",
        "table1": "表格1",
        "table2": "表格2",
        "table1_caption": "格式：每行一个位号 + 料号",
        "table2_caption": "格式：多个位号可用逗号分隔",
        "upload_table1": "上传表格1",
        "upload_table2": "上传表格2",
        "select_columns": "② 选择列",
        "ref_col_t1": "表格1位号列",
        "pn_col_t1": "表格1料号列",
        "ref_col_t2": "表格2位号列",
        "pn_col_t2": "表格2料号列",
        "auto_col_note": "系统会自动建议列名，但如果选择不正确，用户仍然可以手动更改。",
        "preview_files": "查看上传文件",
        "compare": "开始比较",
        "summary": "③ 汇总",
        "total_items": "总项目数",
        "match": "匹配",
        "match_rate": "匹配率",
        "missing": "表格2缺少",
        "extra": "表格2多余",
        "pn_mismatch": "料号不一致",
        "duplicate_ref": "重复位号",
        "critical_dup": "严重重复",
        "total_issues": "问题总数",
        "result_ok": "结果：两个BOM完全匹配，未发现问题。",
        "result_critical": "结果：发现严重重复位号且料号不同，请优先检查Critical Duplicate项目。",
        "result_mismatch": "结果：发现料号不一致，请优先检查PN Mismatch项目。",
        "result_duplicate": "结果：发现重复位号，请检查Duplicate Ref.项目。",
        "result_missing_extra": "结果：发现缺失或多余项目，请检查差异。",
        "issue_center": "问题中心",
        "duplicate_check": "重复位号检查",
        "comparison_result": "④ 比较结果",
        "download_excel": "📥 下载Excel报告",
        "processing_error": "处理文件时发生错误",
        "upload_warning": "请上传两个文件以开始比较。",
        "footer": "BOM Comparator Tool | Version 1.5.16<br><br>Developed by Matheus Augusto de Lima Basilio<br>Quality Specialist | Matheus.Augusto@jovimobile.com<br>© 2026 Matheus Augusto de Lima Basilio",
        "filters": "筛选和搜索",
        "result_filter": "筛选结果",
        "issue_filter": "按严重等级筛选问题",
        "search": "搜索位号或料号",
        "all": "全部",
        "all_issues": "全部",
        "no_result": "未找到符合筛选条件的结果。",
        "issue_filters": "🚨 问题中心筛选",
        "comparison_filters": "🔍 比较结果筛选",
        "issue_filter_note": "ℹ️ 此筛选仅影响问题中心。",
        "comparison_filter_note": "ℹ️ 这些筛选影响比较结果，并可在显示的表格中搜索。",
        "drag_drop": "📁 将文件拖到这里或点击选择文件",
        "supported_files": "支持格式：XLSX、XLS 和 CSV"
    }
}


# Translation for table headers and displayed statuses
TABLE_TEXT = {
    "pt": {
        "ref": "Ref.",
        "pn": "Part Number",
        "pn_t1": "PN Tabela 1",
        "pn_t2": "PN Tabela 2",
        "status": "Status",
        "table": "Tabela",
        "qty": "Qtd.",
        "pn_count": "Qtd. PN",
        "pn_list": "Lista de Part Numbers",
        "issue": "Problema",
        "issue_type": "Tipo de Problema",
        "details": "Detalhes",
        "severity": "Severidade",
        "match": "Match",
        "missing": "Faltando na Tabela 2",
        "extra": "Extra na Tabela 2",
        "mismatch": "PN Divergente",
        "duplicate": "Ref. Duplicada",
        "critical_duplicate": "Duplicidade Crítica - PN Diferente",
        "high": "Alta",
        "medium": "Média",
        "critical": "Crítica",
        "table1": "Tabela 1",
        "table2": "Tabela 2",
        "table1_vs_table2": "Tabela 1 vs Tabela 2"
    },
    "en": {
        "ref": "Ref.",
        "pn": "Part Number",
        "pn_t1": "PN Table 1",
        "pn_t2": "PN Table 2",
        "status": "Status",
        "table": "Table",
        "qty": "Qty",
        "pn_count": "PN Count",
        "pn_list": "Part Number List",
        "issue": "Issue",
        "issue_type": "Issue Type",
        "details": "Details",
        "severity": "Severity",
        "match": "Match",
        "missing": "Missing in Table 2",
        "extra": "Extra in Table 2",
        "mismatch": "PN Mismatch",
        "duplicate": "Duplicate Ref.",
        "critical_duplicate": "Critical Duplicate Ref. - Different PN",
        "high": "High",
        "medium": "Medium",
        "critical": "Critical",
        "table1": "Table 1",
        "table2": "Table 2",
        "table1_vs_table2": "Table 1 vs Table 2"
    },
    "cn": {
        "ref": "位号",
        "pn": "料号",
        "pn_t1": "表格1料号",
        "pn_t2": "表格2料号",
        "status": "状态",
        "table": "表格",
        "qty": "数量",
        "pn_count": "料号数量",
        "pn_list": "料号列表",
        "issue": "问题",
        "issue_type": "问题类型",
        "details": "详细信息",
        "severity": "严重等级",
        "match": "匹配",
        "missing": "表格2缺少",
        "extra": "表格2多余",
        "mismatch": "料号不一致",
        "duplicate": "重复位号",
        "critical_duplicate": "严重重复位号-不同料号",
        "high": "高",
        "medium": "中",
        "critical": "严重",
        "table1": "表格1",
        "table2": "表格2",
        "table1_vs_table2": "表格1 vs 表格2"
    }
}

STATUS_MAP = {
    "匹配 (Match)": "match",
    "匹配": "match",
    "存在于表格1，但不存在于表格2 (Only in Table 1)": "missing",
    "表格2缺少项目": "missing",
    "存在于表格2，但不存在于表格1 (Only in Table 2)": "extra",
    "表格2多余项目": "extra",
    "料号不一致 (PN Mismatch)": "mismatch",
    "料号不一致": "mismatch",
    "重复位号 (Duplicate Ref.)": "duplicate",
    "重复位号": "duplicate",
    "严重重复位号-不同料号 (Critical Duplicate Ref. - Different PN)": "critical_duplicate",
    "严重重复位号-不同料号": "critical_duplicate"
}

ISSUE_TYPE_MAP = {
    "PN Mismatch": "mismatch",
    "Missing in Table 2": "missing",
    "Extra in Table 2": "extra",
    "Duplicate Ref.": "duplicate",
    "Critical Duplicate Ref. - Different PN": "critical_duplicate"
}

SEVERITY_MAP = {
    "High": "high",
    "Medium": "medium",
    "Critical": "critical"
}

TABLE_MAP = {
    "Table 1": "table1",
    "Table 2": "table2",
    "Table 1 vs Table 2": "table1_vs_table2"
}


def traduzir_status(valor, lang):
    chave = STATUS_MAP.get(str(valor))
    return TABLE_TEXT[lang].get(chave, valor) if chave else valor


def traduzir_issue_type(valor, lang):
    chave = ISSUE_TYPE_MAP.get(str(valor))
    return TABLE_TEXT[lang].get(chave, valor) if chave else valor


def traduzir_severity(valor, lang):
    chave = SEVERITY_MAP.get(str(valor))
    return TABLE_TEXT[lang].get(chave, valor) if chave else valor


def traduzir_tabela(valor, lang):
    chave = TABLE_MAP.get(str(valor))
    return TABLE_TEXT[lang].get(chave, valor) if chave else valor


def traduzir_details(valor, lang):
    texto = str(valor)

    if texto.startswith("Qty="):
        texto = texto.replace("Qty=", {
            "pt": "Qtd.=",
            "en": "Qty=",
            "cn": "数量="
        }[lang])
        texto = texto.replace("PN List=", {
            "pt": "Lista de PN=",
            "en": "PN List=",
            "cn": "料号列表="
        }[lang])

    texto = texto.replace("Exists in Table 1, but not in Table 2", {
        "pt": "Existe na Tabela 1, mas não existe na Tabela 2",
        "en": "Exists in Table 1, but not in Table 2",
        "cn": "存在于表格1，但不存在于表格2"
    }[lang])

    texto = texto.replace("Exists in Table 2, but not in Table 1", {
        "pt": "Existe na Tabela 2, mas não existe na Tabela 1",
        "en": "Exists in Table 2, but not in Table 1",
        "cn": "存在于表格2，但不存在于表格1"
    }[lang])

    return texto


def traduzir_resultado_df(df, lang):
    out = df.copy()
    labels = TABLE_TEXT[lang]

    if "Status" in out.columns:
        out["Status"] = out["Status"].apply(lambda x: traduzir_status(x, lang))

    out = out.rename(columns={
        "位号 (Ref.)": labels["ref"],
        "PN_Tabela1": labels["pn_t1"],
        "PN_Tabela2": labels["pn_t2"],
        "Status": labels["status"]
    })

    return out


def traduzir_duplicate_df(df, lang):
    out = df.copy()
    labels = TABLE_TEXT[lang]

    if out.empty:
        return out.rename(columns={
            "Table": labels["table"],
            "位号 (Ref.)": labels["ref"],
            "Qty": labels["qty"],
            "PN Count": labels["pn_count"],
            "料号列表 (Part Number List)": labels["pn_list"],
            "Issue": labels["issue"]
        })

    if "Table" in out.columns:
        out["Table"] = out["Table"].apply(lambda x: traduzir_tabela(x, lang))

    if "Issue" in out.columns:
        out["Issue"] = out["Issue"].apply(lambda x: traduzir_status(x, lang))

    out = out.rename(columns={
        "Table": labels["table"],
        "位号 (Ref.)": labels["ref"],
        "Qty": labels["qty"],
        "PN Count": labels["pn_count"],
        "料号列表 (Part Number List)": labels["pn_list"],
        "Issue": labels["issue"]
    })

    return out


def traduzir_issues_df(df, lang):
    out = df.copy()
    labels = TABLE_TEXT[lang]

    if out.empty:
        return out.rename(columns={
            "Issue Type": labels["issue_type"],
            "Table": labels["table"],
            "位号 (Ref.)": labels["ref"],
            "PN Table 1": labels["pn_t1"],
            "PN Table 2": labels["pn_t2"],
            "Details": labels["details"],
            "Severity": labels["severity"]
        })

    if "Issue Type" in out.columns:
        out["Issue Type"] = out["Issue Type"].apply(lambda x: traduzir_issue_type(x, lang))

    if "问题类型" in out.columns:
        out["问题类型"] = out["问题类型"].apply(lambda x: traduzir_status(x, lang))

    if "Table" in out.columns:
        out["Table"] = out["Table"].apply(lambda x: traduzir_tabela(x, lang))

    if "Severity" in out.columns:
        out["Severity"] = out["Severity"].apply(lambda x: traduzir_severity(x, lang))

    if "Details" in out.columns:
        out["Details"] = out["Details"].apply(lambda x: traduzir_details(x, lang))

    out = out.rename(columns={
        "Issue Type": labels["issue_type"],
        "问题类型": labels["issue"],
        "Table": labels["table"],
        "位号 (Ref.)": labels["ref"],
        "PN Table 1": labels["pn_t1"],
        "PN Table 2": labels["pn_t2"],
        "Details": labels["details"],
        "Severity": labels["severity"]
    })

    return out


def traduzir_normalizada_df(df, lang):
    return df.copy().rename(columns={
        "位号 (Ref.)": TABLE_TEXT[lang]["ref"],
        "料号 (Part Number)": TABLE_TEXT[lang]["pn"]
    })


def aplicar_busca_resultado(df, termo):
    if not termo:
        return df

    termo = str(termo).strip().lower()
    if termo == "":
        return df

    cols = ["位号 (Ref.)", "PN_Tabela1", "PN_Tabela2", "Status"]
    mask = False

    for col in cols:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.lower().str.contains(termo, na=False)

    return df[mask]


if "lang" not in st.session_state:
    st.session_state.lang = "en"

# ----------------------------
# Language selector with real flag cards
# ----------------------------
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
.upload-card {
    padding: 16px 16px 8px 16px;
    border-radius: 12px 12px 0 0;
    border: 1px dashed #38bdf8;
    border-bottom: none;
    background: rgba(15, 23, 42, 0.55);
    margin-bottom: 0;
}
.upload-title {
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
}
.upload-hint {
    font-size: 13px;
    color: #93c5fd;
    margin-bottom: 2px;
}
.upload-format {
    font-size: 12px;
    color: #94a3b8;
}
div[data-testid="stFileUploader"] {
    margin-top: 0 !important;
}
div[data-testid="stFileUploader"] section {
    border-radius: 0 0 12px 12px !important;
    border: 1px dashed #38bdf8 !important;
    border-top: none !important;
    background: rgba(31, 41, 55, 0.70) !important;
    padding-top: 12px !important;
}
div[data-testid="stFileUploader"] label {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

render_language_selector(st.session_state.lang)

t = TEXT[st.session_state.lang]

# ============================================================
# Login Screen
# ============================================================

VALID_USER = "quality"
VALID_PASSWORD = "jovi123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .login-container {
        max-width: 430px;
        margin: 70px auto 0 auto;
        padding: 34px 34px 28px 34px;
        border-radius: 18px;
        border: 1px solid #334155;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(17, 24, 39, 0.96));
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
    }
    .login-title {
        font-size: 30px;
        font-weight: 850;
        color: #f8fafc;
        text-align: center;
        margin-bottom: 8px;
    }
    .login-subtitle {
        font-size: 14px;
        color: #93c5fd;
        text-align: center;
        margin-bottom: 24px;
    }
    .login-footer {
        font-size: 12px;
        color: #64748b;
        text-align: center;
        margin-top: 18px;
    }
    </style>
    <div class="login-container">
        <div class="login-title">BOM Comparator Tool</div>
        <div class="login-subtitle">Restricted Access | Jovi Quality Department</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Usuário / User")
        password = st.text_input("Senha / Password", type="password")
        login_clicked = st.form_submit_button("Entrar / Login", use_container_width=True)

        if login_clicked:
            if username == VALID_USER and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos. / Invalid username or password.")

    st.markdown("""
    <div class="login-footer">
        Developed by Matheus Augusto de Lima Basilio<br>
        Quality Specialist | Jovi Quality Department
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# Logout control
logout_col1, logout_col2 = st.columns([8, 1])
with logout_col2:
    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()


# ----------------------------
# Header
# ----------------------------
st.markdown(f"""
<div class="main-header">
    <div>
        <div class="main-title">{t["app_title"]}</div>
        <div class="main-subtitle">{t["app_subtitle"]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="section-card">
    <div class="section-title">{t["how_to_use"]}</div>
    <div class="section-text">
        {t["step1"]}<br>
        {t["step2"]}<br>
        {t["step3"]}<br>
        {t["step4"]}
    </div>
    <br>
    <div class="small-note">{t["note"]}</div>
</div>
""", unsafe_allow_html=True)

st.subheader(t["upload_files"])

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="upload-card">
        <div class="upload-title">{t['table1']}</div>
        <div class="upload-hint">{t['drag_drop']}</div>
        <div class="upload-format">{t['table1_caption']} | {t['supported_files']}</div>
    </div>
    """, unsafe_allow_html=True)

    arquivo1 = st.file_uploader(
        t["upload_table1"],
        type=["xlsx", "xls", "csv"],
        key="t1",
        label_visibility="collapsed"
    )

with col2:
    st.markdown(f"""
    <div class="upload-card">
        <div class="upload-title">{t['table2']}</div>
        <div class="upload-hint">{t['drag_drop']}</div>
        <div class="upload-format">{t['table2_caption']} | {t['supported_files']}</div>
    </div>
    """, unsafe_allow_html=True)

    arquivo2 = st.file_uploader(
        t["upload_table2"],
        type=["xlsx", "xls", "csv"],
        key="t2",
        label_visibility="collapsed"
    )


def primeira_linha_eh_comentario(arquivo):
    """
    Detects whether the first row of Table 2 is a comment/note row.
    If the file is already clean and starts with the real headers, it will not skip anything.
    """
    try:
        if arquivo.name.lower().endswith(".csv"):
            preview = pd.read_csv(arquivo, dtype=str, header=None, nrows=1)
            arquivo.seek(0)
        else:
            preview = pd.read_excel(arquivo, dtype=str, header=None, nrows=1)
            arquivo.seek(0)

        if preview.empty:
            return False

        first_row_text = " ".join(
            preview.iloc[0].fillna("").astype(str).tolist()
        ).lower()

        comment_keywords = [
            "note:",
            "note：",
            "the red background",
            "unverified material",
            "red background color",
            "备注",
            "说明"
        ]

        header_keywords = [
            "bit number",
            "child material code",
            "ref",
            "part number",
            "料号",
            "位号"
        ]

        # If it clearly contains real headers, do not skip.
        if any(keyword in first_row_text for keyword in header_keywords):
            return False

        # If it contains comment/note text, skip first row.
        if any(keyword in first_row_text for keyword in comment_keywords):
            return True

        return False

    except Exception:
        try:
            arquivo.seek(0)
        except Exception:
            pass
        return False


def ler_arquivo(arquivo, skip_first_row=False):
    skiprows = 1 if skip_first_row else 0

    if arquivo.name.lower().endswith(".csv"):
        df = pd.read_csv(arquivo, dtype=str, skiprows=skiprows)
        arquivo.seek(0)
        return df

    df = pd.read_excel(arquivo, dtype=str, skiprows=skiprows)
    arquivo.seek(0)
    return df


def limpar_nome_coluna(c):
    return str(c).replace("\n", " ").strip()


def normalizar_colunas(df):
    df = df.copy()
    df.columns = [limpar_nome_coluna(c) for c in df.columns]
    return df


def encontrar_coluna_padrao(colunas, tipo):
    colunas_lista = list(colunas)

    if tipo == "ref":
        candidatos = [
            "bit number",
            "ref", "ref.", "reference", "reference designator",
            "designator", "ref des", "refdes", "location",
            "位号", "位置", "器件位号"
        ]
    else:
        candidatos = [
            "child material code",
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


def gerar_excel(resultado, tabela1_normalizada, tabela2_normalizada, dup_tabela1, dup_tabela2, issues_df, lang):
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
        traduzir_issues_df(issues_df, lang).to_excel(writer, index=False, sheet_name="Issues")
        traduzir_resultado_df(match_df, lang).to_excel(writer, index=False, sheet_name="Match")
        traduzir_resultado_df(missing_df, lang).to_excel(writer, index=False, sheet_name="Missing")
        traduzir_resultado_df(extra_df, lang).to_excel(writer, index=False, sheet_name="Extra")
        traduzir_resultado_df(mismatch_df, lang).to_excel(writer, index=False, sheet_name="PN_Mismatch")
        traduzir_duplicate_df(dup_tabela1, lang).to_excel(writer, index=False, sheet_name="Duplicate_Ref_T1")
        traduzir_duplicate_df(dup_tabela2, lang).to_excel(writer, index=False, sheet_name="Duplicate_Ref_T2")
        traduzir_resultado_df(resultado, lang).to_excel(writer, index=False, sheet_name="All_Results")
        traduzir_normalizada_df(tabela1_normalizada, lang).to_excel(writer, index=False, sheet_name="Table1_Normalized")
        traduzir_normalizada_df(tabela2_normalizada, lang).to_excel(writer, index=False, sheet_name="Table2_Normalized")

        workbook = writer.book

        for sheet_name in workbook.sheetnames:
            ws = workbook[sheet_name]

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

            ws.freeze_panes = "A2"

            if ws.max_row > 1 and ws.max_column > 1:
                ws.auto_filter.ref = ws.dimensions

    output.seek(0)
    return output


if arquivo1 and arquivo2:
    try:
        df1 = normalizar_colunas(ler_arquivo(arquivo1))

        skip_first_row_t2 = primeira_linha_eh_comentario(arquivo2)
        df2 = normalizar_colunas(ler_arquivo(arquivo2, skip_first_row=skip_first_row_t2))

        file_signature = (
            getattr(arquivo1, "name", ""),
            getattr(arquivo1, "size", None),
            getattr(arquivo2, "name", ""),
            getattr(arquivo2, "size", None)
        )

        if st.session_state.get("file_signature") != file_signature:
            st.session_state["file_signature"] = file_signature
            st.session_state["comparison_done"] = False

        st.subheader(t["select_columns"])

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"**{t['table1']}**")
            col_ref_t1 = st.selectbox(
                t["ref_col_t1"],
                df1.columns,
                index=encontrar_coluna_padrao(df1.columns, "ref"),
                key="ref_t1"
            )
            col_pn_t1 = st.selectbox(
                t["pn_col_t1"],
                df1.columns,
                index=encontrar_coluna_padrao(df1.columns, "pn"),
                key="pn_t1"
            )

        with c2:
            st.markdown(f"**{t['table2']}**")
            col_ref_t2 = st.selectbox(
                t["ref_col_t2"],
                df2.columns,
                index=encontrar_coluna_padrao(df2.columns, "ref"),
                key="ref_t2"
            )
            col_pn_t2 = st.selectbox(
                t["pn_col_t2"],
                df2.columns,
                index=encontrar_coluna_padrao(df2.columns, "pn"),
                key="pn_t2"
            )

        st.caption(t["auto_col_note"])

        with st.expander(t["preview_files"]):
            st.write(t["table1"])
            st.dataframe(df1.head(20), use_container_width=True)
            st.write(t["table2"])
            st.dataframe(df2.head(20), use_container_width=True)

        st.divider()

        compare_clicked = st.button(t["compare"], type="primary", use_container_width=True)

        if compare_clicked:
            tabela1 = preparar_tabela1(df1, col_ref_t1, col_pn_t1)
            tabela2 = preparar_tabela2(df2, col_ref_t2, col_pn_t2)

            dup_tabela1 = detectar_ref_duplicada(tabela1, "Table 1")
            dup_tabela2 = detectar_ref_duplicada(tabela2, "Table 2")

            resultado = comparar(tabela1, tabela2)
            issues_df = criar_issue_center(resultado, dup_tabela1, dup_tabela2)

            st.session_state["comparison_done"] = True
            st.session_state["tabela1_result"] = tabela1
            st.session_state["tabela2_result"] = tabela2
            st.session_state["dup_tabela1_result"] = dup_tabela1
            st.session_state["dup_tabela2_result"] = dup_tabela2
            st.session_state["resultado_result"] = resultado
            st.session_state["issues_result"] = issues_df

        if st.session_state.get("comparison_done", False):
            tabela1 = st.session_state["tabela1_result"]
            tabela2 = st.session_state["tabela2_result"]
            dup_tabela1 = st.session_state["dup_tabela1_result"]
            dup_tabela2 = st.session_state["dup_tabela2_result"]
            resultado = st.session_state["resultado_result"]
            issues_df = st.session_state["issues_result"]

            st.subheader(t["summary"])

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
                    <div class="metric-title">{t["total_items"]}</div>
                    <div class="metric-value">{total_count}</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-title">{t["match"]}</div>
                    <div class="metric-value">{match_count}</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-title">{t["match_rate"]}</div>
                    <div class="metric-value">{match_rate:.2f}%</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">{t["missing"]}</div>
                    <div class="metric-value">{missing_count}</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">{t["extra"]}</div>
                    <div class="metric-value">{extra_count}</div>
                </div>
                <div class="metric-card red">
                    <div class="metric-title">{t["pn_mismatch"]}</div>
                    <div class="metric-value">{mismatch_count}</div>
                </div>
                <div class="metric-card yellow">
                    <div class="metric-title">{t["duplicate_ref"]}</div>
                    <div class="metric-value">{duplicate_count}</div>
                </div>
                <div class="metric-card red">
                    <div class="metric-title">{t["critical_dup"]}</div>
                    <div class="metric-value">{critical_duplicate_count}</div>
                </div>
                <div class="metric-card purple">
                    <div class="metric-title">{t["total_issues"]}</div>
                    <div class="metric-value">{total_issues_count}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if total_issues_count == 0:
                st.success(t["result_ok"])
            elif critical_duplicate_count > 0:
                st.error(t["result_critical"])
            elif mismatch_count > 0:
                st.error(t["result_mismatch"])
            elif duplicate_count > 0:
                st.warning(t["result_duplicate"])
            else:
                st.warning(t["result_missing_extra"])

            # ============================================================
            # Issue Center Filters
            # ============================================================
            issues_filtradas = issues_df.copy()

            if total_issues_count > 0:
                st.subheader(t["issue_filters"])
                issue_col1, issue_col2 = st.columns([2, 5])

                issue_filter_options = [
                    t["all_issues"],
                    TABLE_TEXT[st.session_state.lang]["critical"],
                    TABLE_TEXT[st.session_state.lang]["high"],
                    TABLE_TEXT[st.session_state.lang]["medium"]
                ]

                with issue_col1:
                    issue_filter_label = st.selectbox(
                        t["issue_filter"],
                        issue_filter_options,
                        key="issue_filter"
                    )

                with issue_col2:
                    st.caption(t["issue_filter_note"])

                if issue_filter_label != t["all_issues"] and not issues_filtradas.empty:
                    severity_key = None
                    for key in ["critical", "high", "medium"]:
                        if issue_filter_label == TABLE_TEXT[st.session_state.lang][key]:
                            severity_key = key

                    if severity_key:
                        internal_severities = [k for k, v in SEVERITY_MAP.items() if v == severity_key]
                        issues_filtradas = issues_filtradas[issues_filtradas["Severity"].isin(internal_severities)]

                st.subheader(t["issue_center"])

                if issues_filtradas.empty:
                    st.info(t["no_result"])
                else:
                    st.dataframe(traduzir_issues_df(issues_filtradas, st.session_state.lang), use_container_width=True)

            # ============================================================
            # Comparison Filters
            # ============================================================
            st.subheader(t["comparison_filters"])

            comp_col1, comp_col2, comp_col3 = st.columns([2, 3, 3])

            result_filter_options = [
                t["all"],
                TABLE_TEXT[st.session_state.lang]["match"],
                TABLE_TEXT[st.session_state.lang]["mismatch"],
                TABLE_TEXT[st.session_state.lang]["missing"],
                TABLE_TEXT[st.session_state.lang]["extra"]
            ]

            with comp_col1:
                result_filter_label = st.selectbox(
                    t["result_filter"],
                    result_filter_options,
                    key="result_filter"
                )

            with comp_col2:
                search_text = st.text_input(
                    t["search"],
                    key="search_text"
                )

            with comp_col3:
                st.caption(t["comparison_filter_note"])

            resultado_filtrado = resultado.copy()

            if result_filter_label != t["all"]:
                status_key = None
                for key in ["match", "mismatch", "missing", "extra"]:
                    if result_filter_label == TABLE_TEXT[st.session_state.lang][key]:
                        status_key = key

                if status_key:
                    internal_statuses = [k for k, v in STATUS_MAP.items() if v == status_key]
                    resultado_filtrado = resultado_filtrado[resultado_filtrado["Status"].isin(internal_statuses)]

            resultado_filtrado = aplicar_busca_resultado(resultado_filtrado, search_text)

            if duplicate_count > 0:
                st.subheader(t["duplicate_check"])
                duplicate_all = pd.concat([dup_tabela1, dup_tabela2], ignore_index=True)

                if search_text:
                    termo = str(search_text).strip().lower()
                    duplicate_all = duplicate_all[
                        duplicate_all.astype(str).apply(
                            lambda row: row.str.lower().str.contains(termo, na=False).any(),
                            axis=1
                        )
                    ]

                if duplicate_all.empty:
                    st.info(t["no_result"])
                else:
                    st.dataframe(traduzir_duplicate_df(duplicate_all, st.session_state.lang), use_container_width=True)

            st.subheader(t["comparison_result"])

            if resultado_filtrado.empty:
                st.info(t["no_result"])
            else:
                st.dataframe(traduzir_resultado_df(resultado_filtrado, st.session_state.lang), use_container_width=True)

            excel = gerar_excel(resultado, tabela1, tabela2, dup_tabela1, dup_tabela2, issues_df, st.session_state.lang)
            st.download_button(
                label=t["download_excel"],
                data=excel,
                file_name="bom_comparison_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"{t['processing_error']}: {e}")
else:
    st.warning(t["upload_warning"])

st.markdown(f"""<hr style="margin-top:28px;margin-bottom:10px;border:0;border-top:1px solid #334155;">
<div style="display:flex;align-items:center;justify-content:space-between;color:#94a3b8;font-size:12px;">
<div style="width:25%;"></div>
<div style="width:50%;text-align:center;line-height:1.7;">{t["footer"]}</div>
<div style="width:25%;text-align:left;padding-left:28px;border-left:1px solid #334155;line-height:1.8;color:#38bdf8;font-size:14px;font-weight:700;">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">
<path d="M3 21h18"/>
<path d="M5 21V7l8-4v18"/>
<path d="M19 21V11l-6-3"/>
<path d="M9 9h1"/>
<path d="M9 13h1"/>
<path d="M9 17h1"/>
<path d="M14 13h1"/>
<path d="M14 17h1"/>
</svg>
<span>Jovi Quality Department</span>
</div>
<div style="display:flex;align-items:center;gap:8px;">
<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">
<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
<circle cx="12" cy="7" r="4"/>
</svg>
<span>Manager: 曾毅</span>
</div>
</div>
</div>""", unsafe_allow_html=True)
