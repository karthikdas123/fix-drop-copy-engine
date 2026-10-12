# ⚡ Real-Time FIX Drop-Copy Reconciliation Desk

A Python and Streamlit-based middle-office trade control and risk application designed to simulate real-time exchange drop-copy feeds (FIX protocol format) against internal Order Management System (OMS) blotters.

## 🚀 Overview
In institutional electronic trading, monitoring execution integrity and preventing state desynchronization is critical. This tool automates the reconciliation workflow between internal trading records and exchange matching engine ground truths, instantly flagging operational trade breaks, execution drops, and orphan orders.

## 🛠️ Core Features
* **Automated Exception Detection:** Flags and categorizes trade discrepancies into institutional risk levels:
  * **Critical:** Execution drops (orders active in OMS with no exchange fill confirmation).
  * **High:** Orphan orders (untracked executions arriving from the exchange with no OMS record).
  * **Medium:** Price/quantity trade breaks (mismatches between internal logs and execution prices).
* **Interactive Streamlit Dashboard:** Provides real-time desk metrics, severity filtering, and side-by-side feed inspections.

## 💻 Tech Stack
* **Language:** Python
* **Data Processing:** Pandas
* **UI Framework:** Streamlit

## ⚙️ How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/karthikdas123/fix-drop-copy-engine.git](https://github.com/karthikdas123/fix-drop-copy-engine.git)
   cd fix-drop-copy-engine

   Install dependencies:

pip install streamlit pandas

Run the dashboard:

streamlit run app.py