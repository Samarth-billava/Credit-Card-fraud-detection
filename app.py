from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(x) for x in request.form.values()]
        prediction = model.predict([np.array(data)])
        result = "Fraudulent Transaction 🚨" if prediction[0] == 1 else "Legitimate Transaction ✅"

        if prediction[0] == 1:
            message_html = '''
                <div style="text-align:center; padding:30px; color:white; background: linear-gradient(135deg, #ff0844, #ffb199); height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                    <h1 style="font-size:40px;">🚨 ALERT! FRAUD DETECTED! 🚨</h1>
                    <p style="font-size:22px;">Immediate action is required. Verify your transactions now!</p>
                    <a href="/" style="padding:12px 25px; background-color:#ff0844; color:white; text-decoration:none; border-radius:8px; font-size:18px; box-shadow:0px 0px 15px rgba(255, 0, 0, 0.6);"> Go Back</a>
                </div>
            '''
        else:
            message_html = '''
                <div style="text-align:center; padding:30px; color:white; background: linear-gradient(135deg, #00c6ff, #0072ff); height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                    <h1 style="font-size:40px;">✅ Safe Transaction Confirmed! 🎉</h1>
                    <p style="font-size:22px;">Your transaction looks secure. Keep your financial safety strong! </p>
                    <a href="/" style="padding:12px 25px; background-color:#00ff7f; color:#000; text-decoration:none; border-radius:8px; font-size:18px; box-shadow:0px 0px 15px rgba(0, 255, 127, 0.6);"> Check Another</a>
                </div>
            '''

        return message_html
    except Exception as e:
        return f"""
            <div style='text-align:center; color:white; background: linear-gradient(135deg, #ff512f, #dd2476); height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;'>
                <h2 style='font-size:36px;'>⚠️ Error Occurred ⚠️</h2>
                <p style='font-size:20px;'>{str(e)}</p>
                <a href="/" style="padding:12px 25px; background-color:#ff512f; color:white; text-decoration:none; border-radius:8px; font-size:18px;">🔙 Try Again</a>
            </div>
        """

if __name__ == "__main__":
    app.run(debug=True)
