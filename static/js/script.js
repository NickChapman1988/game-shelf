$(document).ready(function(){
    //Materialize mobile navbar
    $('.sidenav').sidenav({edge: "right"});
    //Materialize accordion for reviews//
    $('.collapsible').collapsible();
    // Materialize Autocomplete Form Input //
    $('input.autocomplete').autocomplete({
        data: {
            // need to add mongo.db.catalogue.game_title here somehow //
        },
    });
    $('select').formSelect();
});