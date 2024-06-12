// autor: Lana Jovanovic

$(document).ready(function(){
    $(".odbijPredlog").click(function(){
        $(this).closest('.list-group-item').slideUp('slow', function(){
            $(".predloziForm", this).find('[name="akcija"]').val('odbij').submit()
            $(this).remove()
        })
    })

    $(".prihvatiPredlog").click(function(){
        $(this).closest('.list-group-item').slideUp('slow', function(){
            $(".predloziForm", this).find('[name="akcija"]').val('prihvati').end().submit()
            $(this).remove()
        })
    })
})