

console.log('olateste')
// console.log($(document).on("click", ".btn-submit-risk"))
console.log('olateste2')
$(document).on("click", ".btn-submit-risk", async () => {
    document.getElementById('btn-report').style.display = "block";
    var idsSelecionados;
    var csrf_token = Cookies.get('csrftoken');
    var href = document.getElementsByClassName('btn-submit-risk')[0].getAttribute('data-href'); //var href = document.getElementsByClassName('btn-submit-risk')[0].getAttribute('data-href');
    data = new FormData();
    data.append('idade', document.getElementById('idade').value);
    data.append('sexo', document.getElementById('sexo').value);
    data.append('altura', document.getElementById('altura').value);
    data.append('peso', document.getElementById('peso').value);
    data.append('fumador', document.getElementById('fumador').value);
    data.append('pressao_arterial', document.getElementById('pressao_arterial').value);
    data.append('colestrol_total', document.getElementById('colestrol_total').value);
    data.append('colestrol_hdl', document.getElementById('colestrol_hdl').value);
    data.append('colestrol_nao_hdl', document.getElementById('colestrol_nao_hdl').value);
    data.append('hemoglobina_gliciada', document.getElementById('hemoglobina_gliciada').value);
    data.append('diabetes', document.getElementById('diabetes').value);
    data.append('anos_diabetes', document.getElementById('anos_diabetes').value);
    data.append('enfarte', document.getElementById('enfarte').value);
    data.append('avc', document.getElementById('avc').value);
    data.append('doenca_pernas', document.getElementById('doenca_pernas').value);
    data.append('doenca_rins', document.getElementById('doenca_rins').value);
    data.append('hipercolestrol', document.getElementById('hipercolestrol').value);
    data.append('comentario', document.getElementById('comentario').value);
    console.log(document.getElementById('comentario').value);
    console.log(document.getElementById('diabetes').value);
    console.log(href);
    // try {
        const response = await fetch(href, {
            method: "POST",
            body: data,
            headers: { 'X-CSRFToken': csrf_token },
            processData: false,  // tell jQuery not to process the data
            contentType: false   // tell jQuery not to set contentType
            
        })
        .then((response) => {
            console.log(response) 
        });
    // } catch (error) {
    //     console.error("Error:", error);
    // }
});
// document.getElementById('data_atual').value = new Date().toISOString();
// function hideButton() {
//     // Oculta o botão de envio
//     var button = document.getElementById('btn-submit-risk')[0];
//     button.style.display = "none";
// }
console.log('chegou aqui');

// $(document).on("click", ".btn-submit-risk",  ()=> {
//     event.preventDefault();
//     var csrf_token = Cookies.get('csrftoken');
//     var href = document.getElementsByClassName('btn-submit-risk')[0].getAttribute('data-href'); //var href = document.getElementsByClassName('btn-submit-risk')[0].getAttribute('data-href');
//     data = new FormData();
//     data.append('idade', document.getElementById('idade').value);
//     data.append('sexo', document.getElementById('sexo').value);
//     data.append('fumador', document.getElementById('fumador').value);
//     data.append('pressao_arterial', document.getElementById('pressao_arterial').value);
//     data.append('colestrol_total', document.getElementById('colestrol_total').value);
//     data.append('comentario', document.getElementById('comentario').value);
//     console.log(document.getElementById('comentario').value);
//     console.log(href);

//     $.ajax({
//         method: 'POST',
//         url: href,
//         data: data,
//         headers: { 'X-CSRFToken': csrf_token },
//         async: false,
//         success: function (data) {
//             console.log("Success!")
//             $('.page-content').html(data);
//             return false;
//         },
//         error: function () {
//             console.log("Error!");
//             alert("Pagina não disponível.");
//         }
//     })
// });