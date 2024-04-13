////JQuery

$(document).ready(function()
{
    $(".searchResult").click(function(){

        //Un-bold all rows
        $(".searchResult").each(function(key, value){
            $(this).css("font-weight","normal");
        });

        //Bold the clicked row
        $(this).css("font-weight","bold");

        //Get master id and save to hidden value for form submit
        var master_id = $(this).find("#res_master_id").text()
        $("#selected_master_id").val(master_id);

    });

    $("form").on('submit', function(event){
        $("#overlay").show();
        this.submit();
    });

});

