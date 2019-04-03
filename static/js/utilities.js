function replaceSpec(Texte){
    var TabSpec = {"à":"a","á":"a","â":"a","ã":"a","ä":"a","å":"a","ò":"o","ó":"o","ô":"o","õ":"o","ö":"o","ø":"o","è":"e","é":"e","ê":"e","ë":"e","ç":"c","ì":"i","í":"i","î":"i","ï":"i","ù":"u","ú":"u","û":"u","ü":"u","ÿ":"y","ñ":"n","-":" ","_":" "}; 
      var reg=/[àáäâèéêëçìíîïòóôõöøùúûüÿñ_-]/gi; 
      return Texte.replace(reg,function(){ return TabSpec[arguments[0].toLowerCase()];}).toLowerCase();
  }
  
function replaceByGroup(choice){
    if (choice == "La France Insoumise / Parti communiste")
        nbGroup = 1;
    else if (choice == "Europe Écologie / Génération.s")
        nbGroup = 2;
    else if (choice == "Parti socialiste / Parti radical")
        nbGroup = 3;
    else if (choice == "UDI / Modem / En Marche")
        nbGroup = 4;
    else if (choice == "Les Républicains")
        nbGroup = 5;
    else if (choice == "Rassemblement national / Les Patriotes")
        nbGroup =  6;
    else
        nbGroup = 7;
    return nbGroup
}

  function calculateMostAdapted(answers) {
    var mostImportantScore = [-1, -1]
    var same_gender = []
    var same_firstname = []
    var similar_firstname = []
    var same_circo = []
    var same_birthdate = []
    var similar_birthdate = [10000]
    //var birthdate = []
    var same_party = []
  
    for(var i = 0; i < liste_dep.length; i++) {
      var result = 1
      // On s'occupe du genre 
      if (liste_dep[i].gender == answers[0].substring(0,1).toUpperCase()) {
        same_gender.push(liste_dep[i].name);
        result = result + 1200;
      }
      // On s'occupe du prénom
      if (replaceSpec(liste_dep[i].first_name).indexOf(replaceSpec(answers[1])) !== -1) {
        if (replaceSpec(liste_dep[i].first_name) == replaceSpec(answers[1])){
          same_firstname.push(liste_dep[i].name)
          result = result + 200
        }
        else {
          similar_firstname.push(liste_dep[i].name)
          result = result + 100
        }  
      }
      // On s'occupe de la circonscription
      if (liste_dep[i].circo == answers[2]) {
        same_circo.push(liste_dep[i].name);
        result = result + 1200;
      }
      // On s'occupe de l'année de naissance
      if (Number(liste_dep[i].date_birth.slice(-4)) == Number(answers[3])) {
        same_birthdate.push(liste_dep[i].name);
        result = result + 1000;
      }
      else {        // birthdate.push([liste_dep[i].name, difference, Number(liste_dep[i].date_birth.slice(-4))]);
        difference = Math.abs(Number(answers[3]) - Number(liste_dep[i].date_birth.slice(-4)))
        if (difference < similar_birthdate[0])
            similar_birthdate = [difference, liste_dep[i].name, liste_dep[i].date_birth, liste_dep[i].gender]
        // birthdate.push([liste_dep[i].name, difference, Number(liste_dep[i].date_birth.slice(-4))]);
        result = result + 1000/difference;
      }
      // On s'occupe des affinités politiques
      if (replaceByGroup(answers[4]) == liste_dep[i].national_party_grp) {
        same_party.push(liste_dep[i].name);
        result = result + 10000;
      }
      else if (Math.abs(replaceByGroup(answers[4]) - liste_dep[i].national_party_grp) == 1) {
        result = result + 6000;
      }
      if (result > mostImportantScore[1])
        mostImportantScore = [liste_dep[i].num, result]
    }
    tab = [mostImportantScore[0], same_gender, same_firstname, same_circo, same_party, same_birthdate, similar_birthdate]
    return(tab)
  }