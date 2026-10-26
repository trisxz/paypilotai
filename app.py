
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="PayPilot AI",
    page_icon="💳",
    layout="wide"
)

st.title("💳 PayPilot AI")
st.caption("Smart invoice management for freelancers")

# Demo data for the first version
if "invoices" not in st.session_state:
    st.session_state.invoices = [
        {
            "client": "Alex Morgan",
            "service": "Logo design",
            "amount": 3000.00,
            "status": "Pending",
            "due_date": "2026-10-30",
        },
        {
            "client": "Jamie Lee",
            "service": "Website design",
            "amount": 8500.00,
            "status": "Paid",
            "due_date": "2026-10-25",
        },
    ]

invoices = st.session_state.invoices

# Dashboard metrics
total = sum(item["amount"] for item in invoices)
pending = sum(
    item["amount"] for item in invoices
    if item["status"] == "Pending"
)
paid = sum(
    item["amount"] for item in invoices
    if item["status"] == "Paid"
)

col1, col2, col3 = st.columns(3)

col1.metric("Total invoiced", f"₹{total:,.2f}")
col2.metric("Awaiting payment", f"₹{pending:,.2f}")
col3.metric("Payments received", f"₹{paid:,.2f}")

st.divider()

# Create invoice
st.subheader("Create an invoice")

with st.form("invoice_form"):
    client = st.text_input("Client name")
    service = st.text_input("Service description")
    amount = st.number_input(
        "Amount (INR)",
        min_value=1.0,
        value=1000.0,
        step=100.0,
    )
    due_date = st.date_input("Due date", value=date.today())

    submitted = st.form_submit_button("Create invoice")

    if submitted:
        if not client.strip() or not service.strip():
            st.error("Please enter both client and service.")
        else:
            st.session_state.invoices.append({
                "client": client.strip(),
                "service": service.strip(),
                "amount": amount,
                "status": "Draft",
                "due_date": due_date.isoformat(),
            })
            st.success("Invoice draft created!")
            st.rerun()

st.divider()

# Invoice list
st.subheader("Your invoices")

if st.session_state.invoices:
    st.dataframe(
        st.session_state.invoices,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No invoices yet. Create your first invoice above.")

st.caption(
    "Prototype only — no real payments have been processed."
)

