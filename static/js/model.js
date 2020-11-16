function redirect(url) {
    document.location.href = url;
}


/*function redirectLinkPage(){
    document.getElementById('a')
        .getAttribute('id')
        .on("click",function() {
            redirect("'"+this.getAttribute("id")+"'")
        })
}*/



/*function createTopMenu(categories) {
    // ajoute une table dans la div "top-menu"
    var table = d3.select("content").append("table");
    var tr = table.append("tr"); // la table consiste en 1 lignes et de plusieurs colonnes

    for (var i = 0; i < categories.length; i++) {
        var title = categories[i]["title"], url = categories[i]["url"];

        // genere chaque colonne de la table, title=<le nom de la categorie>
        // url=<l'adresse de redirection>
        var th = table.append("th");
        th.append("label")
            .attr("for", title)
        .append("input")
            .attr("id", "button-h")
            .attr("name", title)
            .attr("type", "submit")
            .attr("value", title)
            .attr("class", url)
            .on("click", function() {
                redirect(this.getAttribute("class"));
            });
    }*/
}