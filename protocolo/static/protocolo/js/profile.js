console.log('está aqui');
document.getElementById('btn-abrir').addEventListener('click', () => {
    div = document.getElementById('card-profile');
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
});
console.log('está aqui2');
document.getElementById('btn-fechar').addEventListener('click', () => {
    div = document.getElementById('card-profile-risk');
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
});
