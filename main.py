import os
import flask

app = flask.Flask(__name__)

# top menu categories, their title associated with the redirection url
categories = [{"title" : "Accueil", "url" : "/"}, {"title" : "Rendu", "url" : "/rendu"}, {"title" : "Ressources", "url" : "/ressources"}]

@app.route("/")
def index():
    return flask.render_template('index.html', data=categories)

@app.route("/rendu")
def rendu():
    data = {}
    for _,_,files in os.walk('static/pdfs'):
        data["titles"] = []
        data["paths"] = []
        for f in files:
            f = f.split('.')[0]
            if f == "feuille_de_route":
                data["titles"].append("Feuille de Route")
            else:
                f = f.split('-')
                if f[0] == "rendu_periodique":
                    data["titles"].append("Rendu Periodique du " + f[1].replace('_', '/'))
                    f = '-'.join(f)
            data["paths"].append(f + ".pdf")

    data["paths"] = flask.Markup('["' + '","'.join(data["paths"]) + '"]')
    data["titles"] = flask.Markup('["' + '","'.join(data["titles"]) + '"]')
    data["categories"] = flask.Markup(str(categories))
    print(data)
    return flask.render_template('pdf_viewer.html', data=data)

@app.route("/ressources")
def ressources():
    data = {}
    data["categories"] = categories
    return flask.render_template('ressources.html', data=data)

if __name__ == "__main__":
    app.run(port=5000)
