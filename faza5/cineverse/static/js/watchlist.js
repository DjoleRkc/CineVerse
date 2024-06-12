/*Autor:Đorđe Pajić*/

/**
 * Updates the watchlist by fetching data from the server and rendering it on the page.
 */
function updateWatchlist() {
$.ajax({
    url: "fetchWatchlist",
    type: "GET",
    dataType: "json",
    success: function (data) {
        $('#watchlist-items').empty();
        data.watchlist.forEach(function (item) {
                var filmURL = `/pregledFilma/${item.naziv}`;
                $('#watchlist-items').append(`
                    <li class="p-3 my-2 rounded">
                        <div>
                            <a href="${filmURL}">
                                <img src="${item.slika}" class="slika">
                            </a>
                            <br>
                            ${item.naziv}
                            <br>
                            <button class="button btn-danger rounded ukloniBtn" data-idfil="${item.idfil}">Ukloni</button>
                            
                        </div>
                    </li>
                    <li class="p-3 my-2 rounded"></li>
                `);
            });

    $(".ukloniBtn").click(function () {

        const idfil = $(this).data("idfil");

        var btn = $(this);

        $.ajax({
            url: "ukloniIzWatchliste",
            type: "POST",
            data: JSON.stringify({idfil}),
            contentType: "application/json",
            success: function(response) {
                if(response.ok) {
                    btn.parent().parent().remove();
                }
                else{
                    console.error(response.error)
                }
            }
    })


})
    },
    error: function (xhr, status, error) {
        console.error("Error fetching watchlist data:", error);
    }
});
}

/**
 * Updates the graded movies by fetching data from the server and rendering it on the page.
 */
function updateGrades() {
    $.ajax({
        url: "fetchGrades",
        type: "GET",
        dataType: "json",
        success: function (data) {
            $('#graded-items').empty();
            data.gradedItems.forEach(function (item) {
                var filmURL = `/pregledFilma/${item.naziv}`;
                $('#graded-items').append(`
                    <li class="p-3 my-2 rounded">
                        <div>
                            <a href="${filmURL}">
                                <img src="${item.slika}" class="slika">
                            </a>
                            <br>
                            ${item.naziv}
                            <br>
                            ${item.ocena}/5 ★
                        </div>
                    </li>
                    <li class="p-3 my-2 rounded"></li>
                `);
            });
        },
        error: function (xhr, status, error) {
            console.error("Error fetching graded items data:", error);
        }
    });
}

updateWatchlist()
updateGrades()

// Regularly updates watchlist and graded items every 10 seconds
setInterval(function () {
    updateWatchlist();
    updateGrades();
}, 10000);





