////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    var submitButton = null;
    $("input[type=submit]").click(function(){
        submitButton = $(this).attr("id");

    });

    $("form").on('submit',function(event){
        //Grey out input submit button
        //$("#scrape_items").attr("disabled", "disabled");
        if (submitButton == "scrape_queue"){
            $("#form_alert").show();
            $("#form_alert").append("Scrape starting!");
            event.preventDefault();
            //alert("scrape submitted!");


            var url = "do_scrape_queue";
            $.get(url, function(data, status){
                $("#debugText").append("Scrape finished!");
            });
        }
//        $("#scrape_items").removeAttr("disabled");
//        this.submit()

    });

});
