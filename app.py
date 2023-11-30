from flask import Flask, render_template,request 
from text_summary import summarizer
app = Flask(__name__)

# def index():
#    return render_template('index.html') 

@app.route('/')
@app.route('/summarize',methods=['POST','GET'])
def summarize():
   if request.method== 'POST':
      data = request.form.get('data')
      res=summarizer(data)
      return render_template('index.html',summary=res[0], doc= res[1])
   return render_template('index.html')
if __name__ == "__main__":
   app.run(debug=True)