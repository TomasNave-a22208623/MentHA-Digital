

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
    data.append('fumador', document.getElementById('fumador').value);
    data.append('pressao_arterial', document.getElementById('pressao_arterial').value);
    data.append('colestrol_total', document.getElementById('colestrol_total').value);
    data.append('comentario', document.getElementById('comentario').value);
    console.log(document.getElementById('comentario').value);
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