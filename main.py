import os
from flask import Flask , render_template, request, Markup
from flask_bootstrap import Bootstrap

#initialisation de l'application flask

app = Flask(__name__)

#creation instance bootstrap et initialisation
def create_app(obj):
     bootstrap = Bootstrap()
     bootstrap.init_app(app)


# top menu categories, their title associated with the redirection url
categories = []

def  addCategorie(obj,elt):
    return obj.append(elt)

addCategorie(categories,{"title" : "Home", "url" : "/","class":"fas fa-home"})
addCategorie(categories,{"title" : "Report", "url" : "/rendu","class":"fas fa-folder-open"})
addCategorie(categories,{"title" : "Dashboard", "url" : "/","class":"fas fa-chart-bar"})
addCategorie(categories,{"title" : "Ressources", "url" : "/ressources","class":"fas fa-globe"})
addCategorie(categories,{"title" : "About Our Team", "url" : "/","class":"fas fa-users"})

#page d'accueil
@app.route("/")
def index():
    return render_template('index.html', data=categories)


#parsage des fichiers pdf contenus dans le dossier static/pdfs  et envoi des données vers la page rendu

@app.route("/rendu")
def rendu():
    nbreFeuilleR=0
    nbreRenduPer=0
    try:
        data = {}
        for _,_,files in os.walk('static/pdfs'):
            data["titlesF"] = []
            data["paths"] = []
            data["titlesR"] = []
            for f in files:
                f = f.split('.')[0]
                if f == "feuille_de_route":
                    nbreFeuilleR += 1
                    data["titlesF"].append("Feuille de Route")
                else:
                    f = f.split('-')
                    if f[0] == "rendu_periodique":
                        nbreRenduPer += 1
                        data["titlesR"].append("Rendu Periodique du " + f[1].replace('_', '/'))
                        f = '-'.join(f)
                data["paths"].append(f + ".pdf")

        data["paths"] = Markup('["' + '","'.join(data["paths"]) + '"]')
        data["titlesF"] = Markup(' , '.join(data["titlesF"]) )
        data["titlesR"] = Markup(' , '.join(data["titlesR"]) )
        data["nbreFeuille"] = nbreFeuilleR
        data["nbreRendu"] = nbreRenduPer
        print(data)


        return render_template('pdf_viewer.html', data=categories, sample=data)
    except Exception as err:
        print(err)
        return str(err)



@app.route("/ressources")
def ressources():

    return render_template('ressources.html', data=categories)

if __name__ == "__main__":
    create_app(app)
    app.run(debug=True)

