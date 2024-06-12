// autor: Lana Jovanovic

$(document).ready(function(){
     /**
     * Handles the functionality for accepting user requests.
     * @param {Event} event - The click event.
     */
    $(".prihvatiDugme").click(function(){
        /**
         * The closest list-group-item element.
         * @type {jQuery}
         */
        $(this).closest('.list-group-item').slideUp('slow', function(){
            /**
             * The userForm element within the list-group-item.
             * @type {jQuery}
             */
            $(".userForm", this).find('[name="action"]').val('prihvati').end().submit()
            $(this).remove()
        })
    })
    /**
     * The jQuery element representing a user list item.
     * @type {jQuery}
     */
    var userListItem;

    /**
     * Handles the functionality for rejecting user requests.
     * @param {Event} event - The click event.
     */
    $(".odbijDugme").click(function() {
        /**
         * The closest list-group-item element.
         * @type {jQuery}
         */
        userListItem = $(this).closest('.list-group-item')
        $("#confirmDeleteModal").modal("show")
    })


    /**
     * Handles the functionality for confirming rejection of user requests.
     * @param {Event} event - The click event.
     */
    $(".prihvatiModalDugme").click(function() {
        userListItem.slideUp('slow', function() {
            /**
             * The userForm element within the user list item.
             * @type {jQuery}
             */
            $(".userForm", userListItem).find('[name="action"]').val('odbij').end().submit()
            userListItem.remove()
        })
    })

})