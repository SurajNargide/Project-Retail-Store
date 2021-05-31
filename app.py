from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/index', methods=['POST','GET'])
def index():
    data = pd.read_csv(r"static/Retail-Ecommerce.csv", encoding='unicode_escape')
    clv = pd.read_csv(r"static/clv.csv")
    sale = pd.read_csv(r"static/salepermonth.csv")
    x = int(request.form['id'])
    r = pd.DataFrame(clv['Time'])
    r = pd.concat([clv['Monetary'], r], axis=1)
    r = pd.concat([clv['Frequent'], r], axis=1)
    r = pd.concat([clv['Recent'], r], axis=1)
    r = pd.concat([clv['CustomerID'], r], axis=1)
    r = (r.loc[r['CustomerID'] == x])
    r = r.drop('CustomerID', axis=1)
    r_col = r.columns
    r_val = r.values
    score = pd.DataFrame(clv['RFM_score'])
    score = pd.concat([clv['CustomerID'], score], axis=1)
    score = (score.loc[score['CustomerID'] == x])
    score = score.drop('CustomerID', axis=1)
    score_col = score.columns
    score_val = score.values
    total = pd.DataFrame(clv['RFM_Total'])
    total = pd.concat([clv['CustomerID'], total], axis=1)
    total = (total.loc[total['CustomerID'] == x])
    total = total.drop('CustomerID', axis=1)
    total_col = total.columns
    total_val = total.values
    qurt = pd.DataFrame(clv['t_score'])
    qurt = pd.concat([clv['m_score'], qurt], axis=1)
    qurt = pd.concat([clv['f_score'], qurt], axis=1)
    qurt = pd.concat([clv['r_score'], qurt], axis=1)
    qurt = pd.concat([clv['CustomerID'], qurt], axis=1)
    qurt = (qurt.loc[qurt['CustomerID'] == x])
    qurt = qurt.drop('CustomerID', axis=1)
    qurt_col = qurt.columns
    qurt_val = qurt.values
    purchase = (data.loc[data['CustomerID'] == x])
    purchase = pd.DataFrame(purchase)
    purchase_col = purchase.columns
    purchase_value = purchase.values

    # Graph
    g = (sale.loc[sale['CustomerID'] == x])
    g = g.set_index('CustomerID')
    g = g.drop('Unnamed: 0', axis=1)
    month = g.columns
    value = g.iloc[0]

    y = (clv.loc[clv['CustomerID'] == x])
    y = y['Cluster']
    y = y.values
    y = np.array(y)
    if y < 3:
        y = 0
    else:
        y = 1

    return render_template("index.html", x = r, purchase=purchase, id = x, headings = purchase_col, data = purchase_value,
                           headings_r =r_col , data_r =r_val, score_head = score_col, score_data = score_val, total_head = total_col, total_data = total_val,
                           qurt_head = qurt_col, qurt_data = qurt_val, y = y )


if __name__ == '__main__':
    app.run(debug=True)
