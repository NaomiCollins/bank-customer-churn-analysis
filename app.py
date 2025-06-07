from flask import Flask, render_template, request, jsonify
import pickle
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open(r'C:\pythoncustchurnprednewd\Customer_Churn_Prediction.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        credit_score = int(request.form['CreditScore'])
        age = int(request.form['Age'])
        tenure = int(request.form['Tenure'])
        balance = float(request.form['Balance'])
        num_of_products = int(request.form['NumOfProducts'])
        has_cr_card = int(request.form['HasCrCard'])
        is_active_member = int(request.form['IsActiveMember'])
        estimated_salary = float(request.form['EstimatedSalary'])
        geography_germany = request.form['Geography_Germany']

        if geography_germany == 'Germany':
            geography_germany = 1
            geography_spain = 0
            geography_france = 0

        elif geography_germany == 'Spain':
            geography_germany = 0
            geography_spain = 1
            geography_france = 0

        else:
            geography_germany = 0
            geography_spain = 0
            geography_france = 1

        gender_male = request.form['Gender_Male']

        if gender_male == 'Male':
            gender_male = 1
            gender_female = 0
        else:
            gender_male = 0
            gender_female = 1

        # Additional features
        complain = int(request.form['Complain'])
        satisfaction_score = int(request.form['SatisfactionScore'])
        card_type = request.form['CardType']
        point_earned = int(request.form['PointEarned'])

        # Convert card_type to numerical values
        card_type_mapping = {'Silver': 0, 'Gold': 1, 'Platinum': 2, 'Diamond': 3}
        card_type_numeric = card_type_mapping.get(card_type, 0)  # Default to 0 if not found

        prediction = model.predict([
            [credit_score, age, tenure, balance, num_of_products, has_cr_card, is_active_member,
             estimated_salary, geography_germany, geography_spain, gender_male,
             complain, satisfaction_score, card_type_numeric, point_earned]
        ])

        if prediction == 1:
            return render_template('index.html', prediction_text="The Customer will leave the bank", show_button=True)
        else:
            return render_template('index.html', prediction_text="The Customer will not leave the bank",
                                   show_button=False)
# Add the recommendation route
@app.route('/recommendation', methods=['GET'])
def recommendation():
    recommendations = [
        "1. Proactively reach out to Identified high-risk customers with personalized incentives, discounts, or alternative solutions to encourage them to stay.",
        "2. Offer personalized financial counseling for customers facing credit score challenges, provide guidance to improve their financial situation and strengthen their relationship with the bank.",
        "3. Design targeted offers for customers with a history of complaints or low satisfaction scores.",
        "4. Implement exit surveys for customers who have decided to leave, gather valuable insights into their reasons for churn and use this feedback to make immediate improvements and future retention strategies."
    ]
    return render_template('reccomend.html', recommendations=recommendations)



if __name__ == "__main__":
     app.debug=True
     app.run()