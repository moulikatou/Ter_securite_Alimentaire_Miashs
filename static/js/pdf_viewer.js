function comeon(some) {
    console.log(some);
    return "yup";
}

function createViewer() {
    /*
        * cree le lecteur de pdf
     */ 
    this.div = d3.select("#content").append("div")
        .attr("id", "view");
    
    //var height = window.innerHeight;
    // height -= d3.select("#top-menu").node().getBoundingClientRect().height;
    // height -= d3.select("#title").node().getBoundingClientRect().height;
    this.viewer = this.div.append("object")
        .attr("id", "PDFObject")
        .attr("type", "application/pdf")
        .attr("width", "100%")
        .attr("height", "500px");
        
}

function displayPDF(filename, title) {
    /*
        * charge le pdf passer en argument, en plus de changer le titre afficher sur la page
     */
    // console.log(filename, title);
    d3.select("#PDFObject").attr("title", filename);
    d3.select("#title").text(title);
}

function createSelector(path, files, titles) {
    // rajoute la div contenant les different input submit
   // this.div = d3.select("#maincontent").append("div")
   //     .attr("id", "select");
    // this.div = document.getElementById("maincontent").append("div");
    // this.div.setAttribute("id", "select");

    // la table pour organiser les boutons
   // this.table = this.div.append("table");
   // for (var i = 0; i < files.length; i++) {
   //     var filename = files[i], title = titles;

        // genere chaque bouton, filename=<le nom du fichier a charger>
        // title=<le titre du fichier a afficher>
    //    var tr = this.table.append("tr")
    //    tr.append("label")
    //        .attr("for", filename)
    //    .append("input")
    //        .attr("id", "button-v")
    //        .attr("name", filename)
    //        .attr("type", "submit")
    //        .attr("value", title)
    //        .on("click", function() {
    //            displayPDF(path + '/' + this.getAttribute("name"), this.getAttribute("value"));
    //        });
   // }
   console.log("je suis là")
}

