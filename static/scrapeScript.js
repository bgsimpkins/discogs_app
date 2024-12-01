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

            event.preventDefault();
            $("#form_alert").show();
            $("#alert_div").append("<div id='form_alert'>Scrape running! <a href='/scrape_queue'>Refresh</a></div>");
            $("#scrape_queue").prop("disabled",true);

            var url = "do_scrape_queue";
            $.get(url, function(data, status){
                $("#debugText").append("Scrape finished!");
            });
        }
//        $("#scrape_items").removeAttr("disabled");
//        this.submit()

    });

});
