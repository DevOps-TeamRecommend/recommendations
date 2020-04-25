$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#recommendation_id").val(res._id);
        $("#product_1").val(res.product_1);
        $("#product_2").val(res.product_2);
        $("#recommendation_type").val(res.recommendation_type);
        if (res.active == true) {
            $("#recommendation_active").val("true");
        } else {
            $("#recommendation_active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_1").val("");
        $("#product_2").val("");
        $("#recommendation_type").val("");
        $("#recommendation_active").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        var product_1 = parseInt($("#product_1").val());
        var product_2 = parseInt($("#product_2").val());
        var recommendation_type = $("#recommendation_type").val();
        var active = $("#recommendation_active").val() == "true";

        var data = {
            "product_1": product_1,
            "product_2": product_2,
            "recommendation_type": recommendation_type,
            "active": active
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        var recommendation_id = parseInt($("#recommendation_id").val());
        var product_1 = parseInt($("#product_1").val());
        var product_2 = parseInt($("#product_2").val());
        var recommendation_type = $("#recommendation_type").val();
        var active = $("#recommendation_active").val() == 'true';
        console.log(active)
        var data = {
            "product_1": product_1,
            "product_2": product_2,
            "recommendation_type": recommendation_type,
            "active": active
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/" + recommendation_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        var recommendation_id = $("#recommendation_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations/" + recommendation_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        var recommendation_id = $("#recommendation_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/recommendations/" + recommendation_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#recommendation_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        var product_1 = $("#product_1").val();
        var product_2 = $("#product_2").val();
        var recommendation_type = $("#recommendation_type").val();
        var active = $("#recommendation_active").val();

        var queryString = ""

        if (recommendation_type) {
            queryString = 'recommendation_type=' + recommendation_type
        }
        if (active) {
            if (queryString.length > 0) {
                queryString += '&active=' + active
            } else {
                queryString += 'active=' + active
            }
        }

        console.log(queryString)

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Product 1</th>'
            header += '<th style="width:40%">Product 2</th>'
            header += '<th style="width:40%">Type</th>'
            header += '<th style="width:10%">Active</th></tr>'
            $("#search_results").append(header);
            var firstRecommendation = "";
            for(var i = 0; i < res.length; i++) {
                var recommendation = res[i];
                var row = "<tr><td>"+recommendation._id+"</td><td>"+recommendation.product_1+"</td><td>"+recommendation.product_2+"</td><td>"+recommendation.recommendation_type+"</td><td>"+recommendation.active+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstRecommendation = recommendation;
                }
            }

            $("#search_results").append('</table>');


            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
