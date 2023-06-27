function toggleChevron() {
    element = document.getElementById("sidebar-icon");

    if (element.classList.contains('fa-chevron-left')) {
        element.classList.remove('fa-chevron-left');
        element.classList.add('fa-chevron-right');
    } else {
        element.classList.add('fa-chevron-left');
        element.classList.remove('fa-chevron-right');
    }
}

function toggleVideoconf() {
    element = document.getElementById("videoconf");
    content = document.getElementById("content");

    if (element.style.height == "0px") {
        console.log("Abre Videoconf")
        element.style.height = "100px";
        content.style.gap = "25px";
    } else {
        console.log("Fecha Videoconf")
        element.style.height = "0px";
        content.style.gap = "0px";
    }
}


function moveSidebar(){
    element = document.getElementById("sidebar");
    content = document.getElementById("content");

    //esconder sidebar
    if (element.style.width === "250px") {
        element.style.width = "82px";
        content.style.marginLeft = "87px";

        document.querySelectorAll('.sidebar-text').forEach(function(e) {
            e.style.display = "none";
        });


        document.getElementById('logo').innerText = "M";

        
    //mostrar sidebar
    } else {
        element.style.width = "250px";
        content.style.marginLeft = "250px";

        document.querySelectorAll('.sidebar-text').forEach(function(e) {
            e.style.display = "inline-block";
        });

        document.getElementById('logo').innerText = "MENTHA DIGITAL";
    }

    
}
window.addEventListener("DOMContentLoaded", (event) => {
    document.getElementById("videoconf").style.height = "0px";
});


$(document).on("click", ".sidebar-toggle-btn", function () {
    toggleChevron();
    moveSidebar();
});

$(document).on("click", ".videoconf-button", function () {
    toggleVideoconf();
});