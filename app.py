from flask import Flask, render_template, request
import pandas as pd
# import your_model  # Importez votre modèle ici

app = Flask(__name__)

@app.route('/for', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = pd.read_csv("analyse_donnees/DB/donn_int_bk.csv")
        culture = request.form['culture']
        prediction = data.predict(culture)
        culture = float(request.form['culture'])
        return render_template('result.html', prediction=prediction)
    return render_template('form.html')

@app.route('/resultat')
def resultat():
    if request.method == 'POST':
        data = pd.read_csv("analyse_donnees/DB/donn_int_bk.csv")
        
        prediction = data.predict(culture)
    return render_template('resultat.html')
  
if __name__ == '__main__':
    app.run(debug=True)