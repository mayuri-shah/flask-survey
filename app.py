from flask import Flask, request, render_template, redirect, flash, jsonify,session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import Survey, Question, surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#session["RESPONSE"] = []
s1 = surveys["satisfaction"]
s2 = surveys["personality"]
res = []

@app.route('/')
def start():
    return render_template('home.html',survey1 = s1,survey2 = s2)

@app.route('/queAns/<int:num>',methods=["POST"])
def start_submit(num):
    session["RESPONSE"] = []
    
    return redirect(f"/questions/{num}/0")

@app.route('/answer/<int:num>',methods=["POST"])
def submit_ans(num):
    ans = request.form.get('answer')
    res = session["RESPONSE"]
    res.append(ans)
    session["RESPONSE"]=res
    return redirect(f"/questions/{num}/{len(res)}")
    
@app.route("/questions/<int:num>/<int:queid>")
def submit_que(num,queid):
    ques = s1.questions if num == 1 else s2.questions
    res = session.get("RESPONSE")
    
    if queid < len(ques):
            question = ques[queid]
                
    if len(res) == len(ques):
           return redirect('/complete')

    if (len(res) != queid):
        flash(f"out of range {queid}")
        return redirect(f"/questions/{num}/{len(res)}")
        
    
    return render_template('questions.html',question=question,queid = queid ,num=num)

@app.route('/complete')
def complete_survey():
    return "Thank you"