// autor : Nikola Ostojić

/**
 * Sorts movies based on the selected criteria.
 */
function sortMovies() {
    /** @type {string} */
    var sortBy = document.getElementById("myDropdown").value;

    /** @type {HTMLElement} */
    var moviesContainer = document.getElementById("cards-holder");

    /** @type {HTMLCollection} */
    var movies = moviesContainer.children;

    /** @type {Array} */
    var moviesArray = Array.from(movies);

    if (sortBy === "IMDB") {
        moviesArray.sort(function(a, b) {
            /** @type {number} */
            var imdbRatingA = parseFloat(a.dataset.imdb);

            /** @type {number} */
            var imdbRatingB = parseFloat(b.dataset.imdb);   
            return imdbRatingB - imdbRatingA;
        });
    } else if (sortBy === "Korisnika") {
        moviesArray.sort(function(a, b) {
            /** @type {number} */
            var korisnikA = parseFloat(a.dataset.korisnikocena);

            /** @type {number} */
            var korisnikB = parseFloat(b.dataset.korisnikocena);
            return korisnikB - korisnikA;
        });
    }

    moviesContainer.innerHTML = "";

    moviesArray.forEach(function(movie) {

        moviesContainer.appendChild(movie);
    });
}

$(document).ready(function(){

    /**
     * Handles the click event on elements with the class "oceniDugme".
     * Clears the previous rating and sets the movie name for rating.
     */
    $(".oceniDugme").click(function(){
        $('input[name="rating"]').prop('checked', false);
        nazivFilma = $(this).data("naziv-filma");
        target = $(this).attr("id");
        $("#oceniFilm").find('.modal-title').text('Oceni: "' + nazivFilma + '"')

    });

    /**
     * Handles the click event on elements with the class "potvrdiOcenu".
     * Retrieves the rating value and sends it to the server to rate the movie.
     * Updates the user rating displayed on the card.
     */
    $(".potvrdiOcenu").click(function(){
        ocena=0;
        for (let i = 1; i < 6; i++) {
            if($("#star"+i).is(':checked')) ocena=i;
        }


        $.post("oceniFilm",{
                'nazivFilma': nazivFilma,
                'ocena':ocena
            }).done(function(response) {
                
                $("#ocena-" + target).html(`Ocena korisnika: ${response.novaOcena.toFixed(1)} ★`);
                $("#CARD-" + target).attr("data-korisnikocena", response.novaOcena.toFixed(1));
            })
    });
    //================================================================

    
    $(".dugmeSrce").click(function() {
        // Get the movie ID from the clicked button
        var filID = $(this).attr("data-idFilma");
        var button = $(this);  // Capture the clicked button
    
        console.log("Button clicked, filID:", filID);
    
        $.post("dodajUWatchList", { 'idFilma': filID })
        .done(function(response) {
            console.log("Response received:", response);
            button.prop('disabled', true);  // Disable the button
        })
        .fail(function(xhr, status, error) {
            console.error("Request failed:", status, error);
        });
    });
    
    
    
    
});