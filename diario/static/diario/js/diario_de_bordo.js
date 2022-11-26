var menuAtivo;
function ativaBotaoParticipante(idParticipante) {
  // desativa todos os botões
  document.querySelectorAll(".participantes button").forEach((button) => {
    button.style.backgroundColor = "whitesmoke";
    button.style.color = "black";
    button.style.font_weight = "600";
  });
  //mostra botao respostas
  let buttonAnswer = document.querySelector('[data-menu="respostas"]');
  buttonAnswer.style.display = "block";
  //esconde botao presencas
  let buttonPresences = document.querySelector('[data-menu="presencas"]');
  buttonPresences.style.display = "none";
  // desativa o botao do grupo
  document.querySelectorAll(".grupo button").forEach((button) => {
    button.style.backgroundColor = "white";
    button.style.color = "black";
    button.style.font_weight = "600";
  });
  // obtém e ativa o botão do participante
  let buttonAtivo = document.querySelector(`[data-participante="${idParticipante}"]`);
  buttonAtivo.style.backgroundColor = "#0d6efd";
  buttonAtivo.style.color = "white";
  buttonAtivo.style.font_weight = "600";
}
//Grupo
function ativaBotaoGrupo(idGrupo) {
  // desativa todos os botões
  document.querySelectorAll(".participantes button").forEach((button) => {
    button.style.backgroundColor = "white";
    button.style.color = "black";
    button.style.font_weight = "600";
  });
  // obtém e ativa o botão do grupo
  let buttonAtivo = document.querySelector(`[data-idGrupo="${idGrupo}"]`);
  buttonAtivo.style.backgroundColor = "#0d6efd";
  buttonAtivo.style.color = "white";
  buttonAtivo.style.font_weight = "600";
  let buttonPresences = document.querySelector('[data-menu="presencas"]');
  buttonPresences.style.display = "block";
  //esconde botao respostas
  let buttonAnswer = document.querySelector('[data-menu="respostas"]');
  buttonAnswer.style.display = "none";
}
//Fim grupo
function ativaMenu() {
  // põe botões de menu a branco + esconde respetiva info
  document.querySelectorAll(".menu").forEach((m) => {
    m.style.backgroundColor = "white";
    m.style.color = "black";
    m.font_weight = "normal";
    document.querySelector(`#${m.dataset.menu}`).style.display = "none";
  });
  menuAtivo.style.color = "white";
  menuAtivo.style.font_weight = "bold";
  menuAtivo.style.backgroundColor = "#0d6efd";
  document.querySelector(`#${menuAtivo.dataset.menu}`).style.display = "block";
}

// function descarregaInfoParticipante(id) {
//   /* vai buscar a informação do participante id */
//   fetch("/diario_participante/" + id)
//     .then((response) => response.text())
//     .then((text) => (document.querySelector(".info").innerHTML = text))
//     .then(() => ativaMenu());
// }

function descarregaInfoParticipante(idSG, idParticipante) {
  console.log("entrou")
  /* vai buscar a informação do participante id */
  fetch('/diario_participante/' + idSG + '/' + idParticipante)
      .then(response => response.text())
      .then(text => document.querySelector('.info').innerHTML = text)
      .then(() => ativaMenu());
}

//Grupo
function descarregaInfoGrupo(idSessaoGrupo) {
  /* vai buscar a informação do grupo id */
  fetch("/diario_grupo/" + idSessaoGrupo)
    .then((response) => response.text())
    .then((text) => {document.querySelector(".info").innerHTML = text;
    //console.log(text)
  })
    .then(() => ativaMenu());
  }

/***************************************************************************/
/********** DOMContentLoaded ***********************************************/
/***************************************************************************/
document.addEventListener("DOMContentLoaded", function () {
  menuAtivo = document.querySelector("[data-menu='notas']");
  document.querySelector("[data-menu='respostas']").style.display = "none";
  // onclick num participante
  document
    .querySelectorAll(".participantes button")
    .forEach((botaoParticipante) => {
      botaoParticipante.onclick = () => {
        ativaBotaoParticipante(botaoParticipante.dataset.participante);
        descarregaInfoParticipante(botaoParticipante.dataset.sessaogrupo, botaoParticipante.dataset.participante);
      };
    });
  //Grupo
  // onclick num grupo
  document.querySelectorAll(".grupo button").forEach((botaoGrupo) => {
    botaoGrupo.onclick = () => {
      ativaBotaoGrupo(botaoGrupo.dataset.idgrupo);
      descarregaInfoGrupo(botaoGrupo.dataset.idgrupo);
    };
  });
  // onclick num botão de menu
  document.querySelectorAll(".menu").forEach((menu) => {
    menu.onclick = () => {
      menuAtivo = menu;
      ativaMenu();
    };
  });
});
/* vai buscar ao formulario com id formId
os dados e envia para servidor,
e espera por info atualizada do participante */
function sendFormParticipante(idSG, idPart, formId) {
  console.log("sendFormParticipante");
  let data = new FormData(document.getElementById(formId));
  fetch(`/diario_participante/${idSG}/${idPart}`, {method: "POST", body: data})
      .then(response => response.text())
      .then(text => {
          document.querySelector('.info').innerHTML = text;
          ativaMenu();
          ativaBotaoParticipante(idPart);
      });
}

function sendForm(idSG, idPart, formId) {
  let data = new FormData(document.getElementById(formId));
  fetch(`/diario_grupo/${idSG}/${idPart}`, { method: "POST", body: data })
    .then((response) => response.text())
    .then((text) => {
      document.querySelector(".info").innerHTML = text;
      ativaMenu();
      ativaBotaoGrupo(idgrupo);
    });
  return false;
}

function mostraDiarioBordo() {
  var htmlShow = document.getElementById("direita");

  if (htmlShow.style.display == "none") {
    htmlShow.style.display = "block";
  } else {
    htmlShow.style.display = "none";
  }
}



function atualizaPresencas(id) {
  let data = new FormData();
  var ele = document.getElementsByTagName('input');
  for(i = 0; i < ele.length; i++) {  
      if(ele[i].type=="radio") {
        if(ele[i].checked){
          data.append('nome', ele[i].name);
          data.append('valor', ele[i].value);
        }
      }
  }
  csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  data.append('csrfmiddlewaretoken',csrfmiddlewaretoken);
  
  fetch('/atualizaPresencasDiario/'+id, {
      method: "POST",
      body: data
      })
      .then(response => response);
}