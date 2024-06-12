/*Autor: Đorđe Pajić, Nikola Ostojić*/

/** @type {string} */
var nazivFilma;

/** @type {number} */
var ocena

$(document).ready(function(){

    /**
     * Handles the click event on elements with the class "oceniDugme".
     * Sets the movie name for rating and updates the modal title accordingly.
     */
    $(".oceniDugme").click(function(){
        $('input[name="rating"]').prop('checked', false);
        nazivFilma = $(this).data("naziv-filma");
        target = $(this).attr("id");
        $("#oceniFilm").find('.modal-title').text('Oceni: "' + nazivFilma + '"')

    })

    /**
     * Handles the click event on elements with the class "potvrdiOcenu".
     * Retrieves the rating value and sends it to the server to rate the movie.
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
            })
    });

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
})
