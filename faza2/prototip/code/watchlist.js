/*Autor:Đorđe Pajić*/

document.addEventListener("DOMContentLoaded", function(){
    const watchListData = [
        {
            title: "Dina: Drugi Deo",
            image: "../images/DINA_223.jpg",
            link: "./pregledFilma.html"
        },
        {
            title: "Bob Marli: One Love",
            image: "../images/One_Love_223x324px_cnplxx_SRB.jpg"
        },
        {
            title: "KUNG FU PANDA 4",
            image: "../images/kung_fu_223.jpg"
        }
    ];

    const watchList = document.getElementById("watchlist");
    const watchListButton = document.getElementById("watchlist-button");
    const watchListContainer = document.querySelector('.watchlist-container');
    watchListContainer.classList.add('d-none');

    function toggleWatchlist() {
        watchListContainer.classList.toggle('d-none');
        if (!watchListContainer.classList.contains('d-none')) {
            renderWatchList();
        } else {
            watchList.innerHTML = ""; // Clear watchlist when hiding
        }
    }

    function renderWatchList(){
        watchList.innerHTML = "";

        watchListData.forEach(movie => {
            const li = document.createElement("li");
            li.classList.add("list-group-item", "d-flex", "align-items-center");

            const img = document.createElement("img");
            img.classList.add("me-3");
            img.src = movie.image;
            img.alt = movie.title;

            img.addEventListener("click", function(){
                window.location.href = movie.link;
            });

            const title = document.createElement("span");
            title.classList.add("flex-grow-1");
            title.textContent = movie.title;

            const removeButton = document.createElement("button");
            removeButton.classList.add("btn", "btn-danger");
            removeButton.textContent = "Ukloni";

            removeButton.addEventListener("click", function(){
                const index = watchListData.indexOf(movie);
                if(index > -1){
                    watchListData.splice(index, 1);
                    renderWatchList();
                }
            });

            li.appendChild(img);
            li.appendChild(title);
            li.appendChild(removeButton);

            watchList.appendChild(li);
        });
    }

    watchListButton.addEventListener("click", function(){
        toggleWatchlist();
    });
});
