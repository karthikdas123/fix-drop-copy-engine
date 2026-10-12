import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Electronic Trading Risk | Drop-Copy Reconciliation",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Real-Time FIX Drop-Copy Reconciliation Desk")
st.markdown("Middle-Office Trade Control & Gateway Desynchronization Monitoring Dashboard")

# Mock Data Generation
oms_data = [
    {"ClOrdID": "ORD-1001", "Symbol": "AAPL", "Side": "BUY",  "Qty": 500, "Price": 180.50, "Status": "FILLED"},
    {"ClOrdID": "ORD-1002", "Symbol": "MSFT", "Side": "SELL", "Qty": 200, "Price": 415.00, "Status": "FILLED"},
    {"ClOrdID": "ORD-1003", "Symbol": "NVDA", "Side": "BUY",  "Qty": 1000,"Price": 875.25, "Status": "PARTIAL"},
    {"ClOrdID": "ORD-1004", "Symbol": "AMZN", "Side": "BUY",  "Qty": 300, "Price": 178.00, "Status": "NEW"},
]
oms_df = pd.DataFrame(oms_data)

dropcopy_data = [
    {"ClOrdID": "ORD-1001", "ExecID": "EX-9001", "Symbol": "AAPL", "Side": "BUY",  "LastQty": 500, "LastPx": 180.50, "ExecType": "Fill"},
    {"ClOrdID": "ORD-1002", "ExecID": "EX-9002", "Symbol": "MSFT", "Side": "SELL", "LastQty": 200, "LastPx": 415.50, "ExecType": "Fill"},
    {"ClOrdID": "ORD-1003", "ExecID": "EX-9003", "Symbol": "NVDA", "Side": "BUY",  "LastQty": 1000,"LastPx": 875.25, "ExecType": "Fill"},
    {"ClOrdID": "ORD-9999", "ExecID": "EX-9999", "Symbol": "GOOGL","Side": "BUY",  "LastQty": 150, "LastPx": 140.20, "ExecType": "Fill"},
]
dc_df = pd.DataFrame(dropcopy_data)

# Reconciliation Engine Logic
merged = pd.merge(oms_df, dc_df, on="ClOrdID", how="outer", suffixes=("_OMS", "_EXCH"))
reconciliation_results = []

for _, row in merged.iterrows():
    cl_ord_id = row["ClOrdID"]
    
    if pd.isna(row.get("Symbol_OMS")):
        reconciliation_results.append({
            "ClOrdID": cl_ord_id,
            "Symbol": row.get("Symbol_EXCH"),
            "Category": "ORPHAN ORDER",
            "Severity": "HIGH",
            "Details": f"Exchange executed ExecID {row.get('ExecID')} but no order found in internal OMS blotter."
        })
    elif pd.isna(row.get("ExecID")):
        reconciliation_results.append({
            "ClOrdID": cl_ord_id,
            "Symbol": row.get("Symbol_OMS"),
            "Category": "EXECUTION DROP",
            "Severity": "CRITICAL",
            "Details": "OMS shows order active/submitted, but no exchange drop-copy fill confirmation received."
        })
    else:
        price_diff = abs(row["Price"] - row["LastPx"])
        if price_diff > 0.01:
            reconciliation_results.append({
                "ClOrdID": cl_ord_id,
                "Symbol": row["Symbol_OMS"],
                "Category": "PRICE TRADE BREAK",
                "Severity": "MEDIUM",
                "Details": f"Price Mismatch! OMS: {row['Price']} vs Exchange: {row['LastPx']}"
            })
        else:
            reconciliation_results.append({
                "ClOrdID": cl_ord_id,
                "Symbol": row["Symbol_OMS"],
                "Category": "MATCHED",
                "Severity": "NONE",
                "Details": "Trade verified successfully."
            })

results_df = pd.DataFrame(reconciliation_results)

# Top Metrics Bar
total_trades = len(results_df)
matched_count = len(results_df[results_df["Category"] == "MATCHED"])
breaks_count = len(results_df[results_df["Category"] != "MATCHED"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Records Processed", total_trades)
col2.metric("Matched Trades", matched_count)
col3.metric("Active Exceptions", breaks_count)

st.divider()

# Exception Filter
severity_filter = st.selectbox("Filter by Exception Severity", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "NONE"])
if severity_filter != "ALL":
    filtered_results = results_df[results_df["Severity"] == severity_filter]
else:
    filtered_results = results_df

st.subheader("📋 Reconciliation Audit Report")
st.dataframe(filtered_results)

# Raw Data Inspection Tabs
st.subheader("🔍 Gateway Feed Inspection")
tab1, tab2 = st.tabs(["Internal OMS Blotter", "Exchange Drop-Copy Feed"])

with tab1:
    st.dataframe(oms_df)

with tab2:
    st.dataframe(dc_df)