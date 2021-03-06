from flask import Flask, request, abort, render_template
import json
import pandas as pd
import pickle
import Project.Config.predict
from Project.Config.predict import getDtScore,getKnnScore,getRfcScore,getNbScore,getAnnScore

app = Flask(__name__)
dt_model=pickle.load(open('./Project/Config/models/dt_model.pkl','rb'))
mlp_model=pickle.load(open('./Project/Config/models/mlp_model.pkl','rb'))
knn_model=pickle.load(open('./Project/Config/models/knn_model.pkl','rb'))
nb_model=pickle.load(open('./Project/Config/models/nb_model.pkl','rb'))
rfc_model=pickle.load(open('./Project/Config/models/rfc_model.pkl','rb'))

dt_score = getDtScore()
knn_score = getKnnScore()
rfc_score = getRfcScore()
nb_score = getNbScore()
mlp_score = getAnnScore()

f = open("./Project/Config/log.txt", "a")
@app.route('/')
def home():
    print(dt_score)
    return render_template('landing.html')



@app.route('/predict',methods=['POST'])
def predict():
    stay_in = 0
    leave = 0
    pred = ""
    customer_id = request.form['id']
    customer_surname = request.form['lastname']
    customer_age = request.form['age']
    customer_gender = request.form['gender']
    customer_geography = request.form['geography']
    customer_score = request.form['score']
    customer_balance = request.form['balance']
    customer_credit_card = request.form['credit_card']
    customer_tenure = request.form['tenure']
    customer_active = request.form['active']
    customer_product = request.form['product']
    customer_salary = request.form['salary']
    features=[float(customer_score),
                float(customer_geography),
                float(customer_gender),
                float(customer_age),
                float(customer_tenure),
                float(customer_balance),
                float(customer_product),
                float(customer_credit_card),
                float(customer_active),
                float(customer_salary)]
    predict_data_dt = dt_model.predict([features])
    predict_data_mlp = mlp_model.predict([features])
    predict_data_knn = knn_model.predict([features])
    predict_data_nb = nb_model.predict([features])
    predict_data_rfc = rfc_model.predict([features])
    predict_list = [predict_data_dt,predict_data_mlp,predict_data_knn,predict_data_nb,predict_data_rfc]
    complete_data = features
    complete_data = [customer_id,
                        customer_surname,
                        float(customer_score),
                        float(customer_geography),
                        float(customer_gender),
                        float(customer_age),
                        float(customer_tenure),
                        float(customer_balance),
                        float(customer_product),
                        float(customer_credit_card),
                        float(customer_active),
                        float(customer_salary)]
    if complete_data[4] == 0 : complete_data[4] = "Male"
    else: complete_data[4] = "Female"
    if complete_data[3] == 0 : complete_data[3] = "France"
    elif complete_data[3] == 1 : complete_data[3] = "Germany"
    elif complete_data[3] == 2 : complete_data[3] = "Spain"
    if complete_data[10] == 0 : complete_data[10] = "No"
    else: complete_data[10] = "Yes"
    if complete_data[9] == 0 : complete_data[9] = "No"
    else: complete_data[9] = "Yes"
    for x in predict_list:
        if x == [0]:
            stay_in += 1
        elif x == [1]:
            leave +=1
        else:
            raise EOFError
    if stay_in > leave :
        pred = "stat"
        complete_data.append("stay")
    else :
        pred = "leave"
        complete_data.append("leave")
    f = open("./Project/Config/log.txt", "a")
    f.write(",".join( repr(e) for e in complete_data ).replace("'", ''))
    f.write("\n")
    f.close()
    return render_template('result.html',
                                pred=pred,
                                dtpre = predict_data_dt,
                                mlppre = predict_data_mlp,
                                knnpre= predict_data_knn,
                                nbpre = predict_data_nb,
                                rfcpre= predict_data_rfc,
                                dt_score = dt_score,
                                rfc_score = rfc_score,
                                mlp_score = mlp_score,
                                knn_score = knn_score,
                                nb_score = nb_score,
                                gender = complete_data[4])
    


@app.route('/history',methods=['POST','GET'])
def history():
    # f = open("./Project/Config/history.txt", "r")
    # a = f.read()
    # f.close()
    a = pd.read_csv('./Project/Config/log.txt', sep=',', error_bad_lines=False)
    a = a.to_html(index = False)
    print(a)
    return render_template('history.html',hist=a)

