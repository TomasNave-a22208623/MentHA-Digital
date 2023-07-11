$(document).on("click", ".btn-submit-risk", async () => {
    //event.preventDefault();
    var idsSelecionados;
    var csrf_token = Cookies.get('csrftoken');
    var href = document.getElementById("risk-submit").getAttribute('data-href'); //var href = document.getElementsByClassName('btn-submit-risk')[0].getAttribute('data-href');
    temErros = false;
    data = new FormData();

    if ((document.getElementById('idade').value < 55) || (document.getElementById('idade').value > 89)) {
        temErros = true;
    } else {
        data.append('idade', document.getElementById('idade').value);
    }

    data.append('sexo', document.getElementById('sexo').value);
    data.append('altura', document.getElementById('altura').value);
    data.append('peso', document.getElementById('peso').value);
    data.append('fumador', document.getElementById('fumador').value);

    if ((document.getElementById('pressao_arterial').value < 100) || (document.getElementById('pressao_arterial').value > 179)) {
        temErros = true;
    } else {
        data.append('pressao_arterial', document.getElementById('pressao_arterial').value);
    }

    if ((document.getElementById('colestrol_total').value < 160) || (document.getElementById('colestrol_total').value > 240)) {
        temErros = true;
    } else {
        data.append('colestrol_total', document.getElementById('colestrol_total').value);
    }

    if ((document.getElementById('colestrol_hdl').value < 80) || (document.getElementById('colestrol_hdl').value > 160)) {
        temErros = true;
    } else {
        data.append('colestrol_hdl', document.getElementById('colestrol_hdl').value);
    }

    if ((document.getElementById('colestrol_nao_hdl').value < 80) || (document.getElementById('colestrol_nao_hdl').value > 160)) {
        temErros = true;
    } else {
        data.append('colestrol_nao_hdl', document.getElementById('colestrol_nao_hdl').value);
    }

    hemoglobina_gliciada = document.getElementById('hemoglobina_gliciada').value;
    hemoglobina_gliciada = parseFloat(hemoglobina_gliciada);

    if ((hemoglobina_gliciada < 3.0) || (hemoglobina_gliciada > 6.9)) {
        temErros = true;
        alert("O valor da hemoglobina glicida deve estar entre 3.0 e 6.9");
    } else {
        data.append('hemoglobina_gliciada', document.getElementById('hemoglobina_gliciada').value);
    }

    data.append('diabetes', document.getElementById('diabetes').value);
    data.append('anos_diabetes', document.getElementById('anos_diabetes').value);
    data.append('enfarte', document.getElementById('enfarte').value);
    data.append('avc', document.getElementById('avc').value);
    data.append('doenca_pernas', document.getElementById('doenca_pernas').value);
    data.append('doenca_rins', document.getElementById('doenca_rins').value);
    data.append('hipercolestrol', document.getElementById('hipercolestrol').value);
    data.append('comentario', document.getElementById('comentario').value);
    // try {
    if (!temErros) {
        event.preventDefault();
        $.ajax({
            method: 'POST',
            url: href,
            data: data,
            mimeType: "multipart/form-data",
            headers: {'X-CSRFToken': csrf_token},
            contentType: false,
            processData: false,
            async: false,
            success: function (data) {
                console.log("Success!")
                $('.container-fluid').html(data);
                return false;
            },
            error: function () {
                console.log("Error!");
                alert("Pagina não disponível.");
            }
        })
    }
    // } catch (error) {
    //     console.error("Error:", error);
    // }$('.page-content').html(data);
});
//teste
// document.getElementById('data_atual').value = new Date().toISOString();
// function hideButton() {
//     // Oculta o botão de envio
//     var button = document.getElementById('btn-submit-risk')[0];
//     button.style.display = "none";
// }



// $(document).on("click", ".btn-submit-risk", function () {
//     event.preventDefault();
//     var href = $(this).attr("data-href");
//     const csrf_token = Cookies.get('csrftoken');
//     // var post_data = $("#appointment-form").serialize();
//     var post_data = $("#risk_form").serialize();
    
//     $.ajax({
//         method: 'POST',
//         url: href,
//         data: post_data,
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