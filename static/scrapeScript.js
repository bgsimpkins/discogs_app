////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    var submitButton = null;
    $("input[type=submit]").click(function(){
        submitButton = $(this).attr("id");
        $("#debugTest").append("<p>clicked button: "+submitButton);

    });

    $("form").on('submit',function(event){
        //Grey out input submit button
        //$("#scrape_items").attr("disabled", "disabled");
        if (submitButton == "scrape_queue"){
            alert("scrape submitted!");
            event.preventDefault();

            var url = "do_scrape_queue";
            $.get(url, function(data, status){
                $("#debugTest").append("Scraping initiated!");
            });
        }
//        $("#scrape_items").removeAttr("disabled");
//        this.submit()

    });

});
