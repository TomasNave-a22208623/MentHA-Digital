console.log('olateste')
// console.log($(document).on("click", ".btn-submit-risk"))
console.log('olateste2')
$(document).on("click", ".btn-submit-risk", async () => {
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
    try {
        const response = await fetch(href, {
            method: "POST",
            body: data,
            headers: { 'X-CSRFToken': csrf_token },
        });
        if (response.ok) {
            hideButton(); // Chama a função para ocultar o botão
        }
    } catch (error) {
        console.error("Error:", error);
    }
});
// document.getElementById('data_atual').value = new Date().toISOString();
// function hideButton() {
//     // Oculta o botão de envio
//     var button = document.getElementById('btn-submit-risk')[0];
//     button.style.display = "none";
// }
console.log('chegou aqui');

document.getElementById('pdfButton').addEventListener('click',  ()=> {
    var doc = new jsPDF("p", "mm", [300, 300]);
    console.log('Clicado-risk');
    var makePDF = document.querySelector("#generatePdf");
    // fromHTML Method
    doc.fromHTML(makePDF);
    doc.save("Risco.pdf");
    console.log("teste risk")
});
