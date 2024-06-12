/* Autor: Đorđe Pajić*/

/**
 * Executes the specified function when the DOM content is fully loaded.
 * Sets up event listeners for date selection, fetching projections, and handling reservation button clicks.
 * Displays success modal upon successful reservation.
 * @param {function} showSuccessMessage - Function to show the success modal.
 */
$(document).ready(async function(){
    /** @type {jQuery} */
    var datumSelektor = $( ".datumSelektor" );

    /** @type {Date} */
    var danas = new Date()

    /** @type {string} */
    var datumId = $(".datumSelektor").attr("id").substr(0,5);

    /** @type {number} */
    var yearToday = danas.getFullYear();

    /** @type {string[]} */
    var datumi = []

    for ( var i = 0; i < 3; i++ )
 {
        /** @type {Date} */
        var optDate = new Date()
        optDate.setDate(danas.getDate()+i)
        /** @type {string} */
        var formatiranDatum =  optDate.getDate().toString().padStart(2, '0') + '.' + (optDate.getMonth() + 1).toString().padStart(2, '0');

        /** @type {jQuery} */
        var option = $('<option>').val("option"+i).attr("id", i.toString()).text(formatiranDatum);

        if (formatiranDatum === datumId) {
            option.prop('selected', true);
        }


        if (i === 0){

            datumi[i] = formatiranDatum + '.' + yearToday;

        }
        else{

            var monthBefore = parseInt(datumi[i-1][3] + datumi[i-1][4]);
            var monthNow = parseInt(formatiranDatum[3] + formatiranDatum[4]);

            if (monthNow < monthBefore){
                yearToday += 1;
            }
            datumi[i] = formatiranDatum + '.' + yearToday;
        }
        


        datumSelektor.append(option);
    }

    /**
     * Handles change events on the date selector.
     * Fetches projections based on the selected date and updates the view.
     */
    $(".datumSelektor").change(function(){
        /** @type {number} */
        var index = parseInt($(this).val()[6]);
        fetch(`projekcije?datum=${datumi[index]}`)
        .then(response => response.text())
        .then(html => {

            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => console.error('Error:', error));
    });
    

    /**
     * Handles click events on reservation buttons.
     * Retrieves projection data based on the selected date and film, and populates the dropdown menu.
     */
    $(".rezervisiDugme").click(function(){
        $(".projekcije").empty();
         /** @type {string} */
         let datum = $(".datumSelektor option:selected").text()

         /** @type {string} */
         let idfil = $(this).data("idfilma");

         /** @type {jQuery} */
         let $dropdownMeni = $(this).next(".dropdown").find(".projekcije");

         $.get('dohvatiProjekcije?idfilma='+idfil+"&datum="+datum,function(response){
            $dropdownMeni.empty()
             $.each(response.data, function (index, projekcija) {
                $dropdownMeni.append(
                    $('<li>').append(
                        $('<a>')
                            .attr('href', 'rezervisiKartu?film=' + idfil + '&vreme=' + encodeURIComponent(projekcija.vreme) + '&sala=' + encodeURIComponent(projekcija.sala) + '&idpro=' + encodeURIComponent(projekcija.idpro))
                            .text(projekcija.vreme + ' - Sala: ' + projekcija.sala)
                    )
                );
                
             })
         })

    })

    $(".promeniDugme").click(function(){
        $(".promeni-projekciju").empty();
         /** @type {string} */
         let datum = $(".datumSelektor option:selected").text()

         /** @type {string} */
         let idfil = $(this).data("idfilma");

         /** @type {jQuery} */
         let $dropdownMeni = $(this).next(".dropdown").find(".promeni-projekciju");

         $.get('dohvatiProjekcije?idfilma='+idfil+"&datum="+datum,function(response){
            $dropdownMeni.empty()
             $.each(response.data, function (index, projekcija) {
                $dropdownMeni.append(
                    $('<li>').append(
                        $('<a>')
                            .attr('href', 'promeniProjekciju?film=' + idfil + '&vreme=' + encodeURIComponent(projekcija.vreme) + '&sala=' + encodeURIComponent(projekcija.sala) + '&idpro=' + encodeURIComponent(projekcija.idpro))
                            .text(projekcija.vreme + ' - Sala: ' + projekcija.sala)
                    )
                );

             })
         })

    })

    $(".obrisiDugme").click(function(){
        $(".obrisi-projekciju").empty();
         /** @type {string} */
         let datum = $(".datumSelektor option:selected").text()

         /** @type {string} */
         let idfil = $(this).data("idfilma");

         /** @type {jQuery} */
         let $dropdownMeni = $(this).next(".dropdown").find(".obrisi-projekciju");

         $.get('dohvatiProjekcije?idfilma='+idfil+"&datum="+datum,function(response){
            $dropdownMeni.empty()
             $.each(response.data, function (index, projekcija) {
                $dropdownMeni.append(
                    $('<li>').append(
                        $('<a>')
                            .attr('href', 'obrisiProjekciju?film=' + idfil + '&vreme=' + encodeURIComponent(projekcija.vreme) + '&sala=' + encodeURIComponent(projekcija.sala) + '&idpro=' + encodeURIComponent(projekcija.idpro))
                            .text(projekcija.vreme + ' - Sala: ' + projekcija.sala)
                    )
                );

             })
         })

    })

    /**
     * Closes the dropdown menu when clicking outside of it.
     */
    $(document).on("click", function(event) {
        if (!$(event.target).closest('.dropdown').length) {
            $(".projekcije").empty();
        }
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


function showSuccessMessage() {
    var myModal = new bootstrap.Modal(document.getElementById('successModal'));
    myModal.show();
}