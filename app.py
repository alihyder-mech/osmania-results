from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, unicodedata
from random import randint
app = Flask(__name__)
API_ENDPOINT = "https://www.osmania.ac.in/res07/20211271.jsp"
grades = { 
    0:"F",
    5:"E",
    6:"D",
    7:"C",
    8:"B",
    9:"A",
    10:"S"
}
def get_data(htno):
    data  = {

            "mbstatus":"SEARCH",
            "htno": htno,
            "Submit.x" : "32",
            "Submit.y" : "10"
        }
    r = requests.post(url = API_ENDPOINT, data = data)
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('font')
    tags = tags[3:len(tags)-11]
    data_t=[]
    for tag in tags:
        data_t.append(unicodedata.normalize("NFKD",tag.contents[0]).strip())

    i = 0
    personal_data= {}
    while i< 12:
        personal_data[data_t[i]]=data_t[i+1]
        i+=2
    i = 18
    grade_data = []
    while i<len(data_t):
        grade_data.append([data_t[i],data_t[i+1],data_t[i+2]])
        i+=5
    i = 0
    while i< len(grade_data):
        try:
            int(grade_data[i][0][:2])
            i+=1
        except:
            grade_data.pop(i)
    
    for i in range(len(grade_data)):
        points = randint(5,10)
        grade_data[i].append(points)
        grade_data[i].append(grades[points])
    gpa = 0
    cred = 0 
    for sub in grade_data:
        holder = sub[2]
        if ( sub[2] == '='):
            holder ='0'
        

        gpa += float(holder)*sub[3]
        cred +=  float(holder)
    sgpa =round(gpa/cred, 2)
    

    personal_data['grade_data'] = grade_data
    personal_data["Result"] = str(sgpa)
    return personal_data
    


@app.route("/", methods=['GET', "POST"])
def hello_world():
    if request.method == "POST":
        htno = request.form.get('htno')
        personal_data =  get_data(htno)
        return render_template('result.html', personal_data = personal_data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
