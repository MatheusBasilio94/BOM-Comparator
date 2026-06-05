
# BOM表对比工具 (BOM Comparison Tool)

This is a bilingual Chinese + English version of the BOM comparison tool.

## How to run

Open Command Prompt in this folder and run:

python -m pip install -r requirements.txt

Then run:

python -m streamlit run app.py

## Main fields

- 位号 (Ref.)
- 料号 (Part Number)

## Result status

- 匹配 (Match)
- 存在于表格1，但不存在于表格2 (Only in Table 1)
- 存在于表格2，但不存在于表格1 (Only in Table 2)
