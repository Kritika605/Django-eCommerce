$(document).ready(function () {
    $(".add-to-cart").click(function () {
        var id = $(this).attr("id");
        $.ajax({
            type : "GET",
            url : "/add-to-cart/",
            data : {
                prod_id : id
            },
            success : function(data) {
                console.log(data)
            }
        })
        })
    $(".plus_quantity").click(function () {
        var id = $(this).attr("pid");
        var curr = this.parentNode.parentNode.children[1].children[0]
        console.log(id);
        $.ajax({
            type : "GET",
            url : "/pluscart/",
            data : {
                prod_id : id
            },
            success : function(data) {
                console.log(data)
                console.log("success")
                curr.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("shipping_charge").innerText = data.shipping_charge
                document.getElementById("cart_total").innerText = data.cart_total
            }
        })
        })
    $(".minus_quantity").click(function () { 
        var id = $(this).attr("pid");
        var curr = this.parentNode.parentNode.children[1].children[0]
        $.ajax({
            type : "GET",
            url : "/minuscart/",
            data : {
                prod_id : id
            },
            success : function(data) {
                console.log(data)
                curr.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("shipping_charge").innerText = data.shipping_charge
                document.getElementById("cart_total").innerText = data.cart_total
            }
        })
        })
    $(".remove_cart").click(function () {
        var id = $(this).attr("id");
        var curr = this
        console.log(id);
        $.ajax({
            type : "GET",
            url : "/remove_cart/",
            data : {
                prod_id : id
            },
            success : function(data) {
                document.getElementById("amount").innerText = data.amount
                document.getElementById("shipping_charge").innerText = data.shipping_charge
                document.getElementById("cart_total").innerText = data.cart_total
                curr.parentNode.parentNode.parentNode.parentNode.parentNode.remove()

            }
        })
        })
    
});
