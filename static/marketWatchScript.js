////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    var submitButton = null;

    $("#debug_message").show();
    $("input[type=submit]").click(function(){
        submitButton = $(this).attr("id");
        //$("#debug_message").append("<p>clicked button: "+submitButton);

    });

////Async kick off of scrape. Very inefficient. Now handled in app.py using scrape queue
//    $("form").on('submit',function(event){
//
//        //Grey out input submit button
//        $("#scrape_items").attr("disabled", "disabled");
//        if (submitButton == "scrape_items"){
//            event.preventDefault();
//            //TODO: Get total number to scrape (number checked) so we know when we're finished.
//            $(".searchResult").each(function(){
//                var selected = $(this).find("input").is(":checked");
//                if (selected == true){
//                    var masterId = $(this).find("#res_master_id").text();
//                    $("#debug_message").append("<p><b>scraping id:</b>"+masterId);
//
//                    var url = "scrape_service?master_id="+masterId;
//                    //$("#debug_message").append("<p>"+url);
//                    $.get(url, function(data, status){
//                        $("#debug_message").append("<p>id="+masterId+"&nbsp success="+data);
//                    });
//                }
//
//
//            });
//        }
////        $("#scrape_items").removeAttr("disabled");
////        this.submit()
//
//    });

     $(".clickable_col").click(function(){

        //Un-bold all rows
        $(".searchResult").each(function(key, value){
            $(this).css("font-weight","normal");
        });

        //Bold the clicked row
        $(this).parent().css("font-weight","bold");

        //Get master id and save to hidden value for form submit
        var master_id = $(this).parent().find("#res_master_id").text()
        $("#selected_master_id").val(master_id);

        $("form").submit();
    });
});

