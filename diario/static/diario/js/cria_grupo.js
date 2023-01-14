

function atualiza_filtros(){
  const programa = document.getElementById('programa').value;
  if (programa) {    
    switch(programa){
      case 'CARE':
        document.querySelector('.filtro_care').style.display = "block";
        document.querySelector('.filtro_cog').style.display = "none";
        break;
      case 'COG':
        document.querySelector('.filtro_care').style.display = "none";
        document.querySelector('.filtro_cog').style.display = "block";
        break;
    }
  }
}

function atualiza_candidatos(){
  console.log("cc")
  form_data = new FormData();
  form_data.append("programa", document.getElementById('programa').value);
  if (document.getElementById('programa').value == "CARE"){
    form_data.append("localizacao", document.getElementById('Localizações_care').value);
    form_data.append("diagnostico", document.getElementById('Diagnósticos_care').value);
    form_data.append("escolaridade", document.getElementById('Escolaridades_care').value);
    form_data.append("referenciacao", document.getElementById('Referenciações_care').value);
  }
  else if (document.getElementById('programa').value == "COG"){
    form_data.append("localizacao", document.getElementById('Localizações_cog').value);
    form_data.append("diagnostico", document.getElementById('Diagnósticos_cog').value);
    form_data.append("escolaridade", document.getElementById('Escolaridades_cog').value);
    form_data.append("referenciacao", document.getElementById('Referenciações_cog').value);
    form_data.append("gds", document.getElementById('GDS_cog').value);
  }

  csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form_data.append('csrfmiddlewaretoken',csrfmiddlewaretoken);

  fetch('/diario/obter_candidatos', {
    method: "POST",
    body: form_data,
    })
    .then(response => response.text())
    .then(text => document.querySelector('.container-candidatos').innerHTML = text)
}
