import collections
import re

import pandas as pd
import requests
import streamlit as st


BASE_URL = "http://backend:8000"


def pretty_money(money):
    return ','.join(re.findall(r'\d{1,3}',
                               str(money)[::-1]))[::-1] + ' Ft'

greeting = st.header("Welcome to the Cost Breakdown")

start_date = st.sidebar.date_input("Start Date (incl.)", format="YYYY-MM-DD")
end_date = st.sidebar.date_input("End Date (incl.)", format="YYYY-MM-DD")

# Get categorized transactions in the range
resp = requests.get(f"{BASE_URL}/categorized_transactions_window/?start_date={start_date}&end_date={end_date}")
print(f"HEY JOE, resp: {resp}")
if resp.status_code != 200:
    categorized_transactions = []
else:
    categorized_transactions = resp.json().get('data', [])
for tx in categorized_transactions:
    if not tx.get("category"):
        tx["category"] = {"name": "misc"}
        tx["pattern"] = {"pattern: ""N/A"}

# Get all categories
resp = requests.get(f"{BASE_URL}/categories/")
if resp.status_code != 200:
    print(f"HEY JOE, GOT {resp.status_code}, {resp.reason}")
categories = [item.get("name") for item in resp.json()] + ["misc"]

show_transactions = st.sidebar.checkbox('Show Transactions')
show_total_cost = st.sidebar.checkbox('Show Total cost')
show_categories = st.sidebar.checkbox('Show Categories')
inspect_category = st.sidebar.checkbox('Show Details')


if show_transactions:
    st.header(f"Categorized Transactions within {start_date} and {end_date}:")
    for tx in categorized_transactions:
        st.write(tx)

if show_total_cost:
    st.write(f"TOTAL COST: {pretty_money(sum([tx.get('transaction', {}).get('amount', 0) for tx in categorized_transactions]))}")


if show_categories:
    cat_url = f"{BASE_URL}/cost_stats/?start_date={start_date}&end_date={end_date}"
    collector = requests.get(cat_url).json()
    df = pd.DataFrame.from_dict({k: [abs(v)] for k, v in collector.items()}, orient='index', columns=["Amount(HUF)"])

    st.write(df)

if inspect_category:
    inspect_cat = st.sidebar.selectbox('Inspect Category', categories)
    if inspect_cat:
        group_events =  st.sidebar.checkbox('Group Events')
        st.header(f'Inspect category {inspect_cat}')

        if group_events:
            collector = collections.defaultdict(int)
            for item in categorized_transactions:
                if item["category"]["name"] != inspect_cat or not item["pattern"]:
                    continue
                collector[item["pattern"].get("pattern", "N/A")] += item["transaction"].get("amount", 0)
            df = pd.DataFrame.from_dict({k:[abs(v)] for k,v in collector.items()}, orient='index', columns=["Amount(HUF)"])
        else:
            collector = [
                (
                    item.get("transaction", {}).get("merchant", "N/A"), 
                    abs(item.get("transaction", {}).get("amount")),
                    item.get("transaction", {}).get("date")
                )
                        for item in categorized_transactions if item["category"]["name"] == inspect_cat]

            df = pd.DataFrame(collector, columns=["Transaction", "Amount(HUF)", "Date"])

    st.write(df)
        
