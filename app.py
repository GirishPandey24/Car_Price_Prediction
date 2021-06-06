from flask import Flask,render_template,request
import pickle
import jsonify
import sklearn
import numpy as np
from sklearn.preprocessing import StandardScaler


app=Flask(__name__)

rf_random=pickle.load(open('car.pkl','rb'))





@app.route("/")
def home():
    return render_template('index.html')



standard_to=StandardScaler()
@app.route('/predict',methods=['POST','GET'])
def predict():
    
    if request.method=='POST':
        
        result_data = []

        dict1 = { 'km_driven':0, 'no_year':0,
        'fuel_Diesel':0, 'fuel_Electric':0,
       'fuel_LPG':0, 'fuel_Petrol':0, 'seller_type_Individual':0,
       'seller_type_Trustmark Dealer':0, 'transmission_Manual':0,
       'owner_Fourth & Above Owner':0, 'owner_Second Owner':0,
       'owner_Test Drive Car':0, 'owner_Third Owner':0}
        
        
        data = [float(x) for x in request.form.values()]

        dict1['km_driven']=data[0]
        year=2020-data[1]
        dict1['no_year']=year
        
        
        if data[2] == 0:####data[2] 2 bcoz it occurs at index 2 ,0 bcoz in html diesel value is 0
            dict1["fuel_Diesel"]=1
        elif data[2] == 1:####data[2] 2 bcoz it occurs at index 2 ,0 bcoz in html electric value is 1
            dict1['fuel_Electric']=1
        elif data[2]==3:
            dict1['fuel_LPG']=1
        elif data[2]==4:
            dict1['fuel_Petrol']=1
        else:
            dict1["fuel_Diesel"]=0
            dict1['fuel_Electric']=0
            dict1['fuel_LPG']=0
            dict1['fuel_Petrol']=0

        if data[3]==1:
            dict1['seller_type_Individual']=1
        elif data[3]==2:
            dict1['seller_type_Trustmark Dealer']=1
        else:
            dict1['seller_type_Individual']=0
            dict1['seller_type_Trustmark Dealer']=0

        if data[4]==0:
            dict1['transmission_Manual']=1
        else:
            dict1['transmission_Manual']=0
        
        if data[5]==0:
            dict1['owner_Fourth & Above Owner']=1
        elif data[5]==1:
            dict1['owner_Second Owner']=1
        elif data[5]==2:
            dict1['owner_Test Drive Car']=1
        elif data[5]==3:
            dict1['owner_Third Owner']=1
        else:
            dict1['owner_Fourth & Above Owner']=0
            dict1['owner_Second Owner']=0
            dict1['owner_Test Drive Car']=0
            dict1['owner_Third Owner']=0
            
        print("==================",dict1)
        for value in dict1.values():
            result_data.append(value)
        print("==========================",data)
        print("=======================",result_data)
            
        
        result=rf_random.predict([result_data])
        output=round(result[0],2)
        #return "The age is {} and the Salary is {}".format(age,salary)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)
