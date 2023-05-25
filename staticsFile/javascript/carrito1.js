// cart
let cartIcon = document.querySelector("#cart-icon");
let cart = document.querySelector(".cart");
let closeCart = document.querySelector("#close-cart");

cartIcon.onclick = () =>{
    cart.classList.add("active");
};
// close cart
closeCart.onclick = () => {
    cart.classList.remove("active");
};

//cart working js
if (document.readyState == "loading"){
    document.addEventListener("DOMContentLoaded", ready);
} else{
    ready();
}

//MAKING FUNCTION
function ready(){
    //remover items del carro
    var reomveCartButtons = document.getElementsByClassName("cart-remove");
    console.log(reomveCartButtons);
    for (var i = 0; i < reomveCartButtons.length; i++){
        var button = reomveCartButtons[i];
        button.addEventListener("click", removeCarItem);
    }
    //quantity changes
    var quantityInputs
}

function removeCarItem(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.remove();
    updatetotal();
}

//update total
function updatetotal(){
   var cartContent = document.getElementsByClassName("cart-content")>[0];
   var cartBoxes = cartContent.getElementsByClassName("cart-box")>[0];
   var total = 0;
   for (var i = 0; i < cartBoxes.length; i++){
    var cartBoxes = cartBoxes[i];
    var priceElement= cartBox.getElementsByClassName('cart-price')[0];
    var quantityElement = cartBox.getElementsByClassName('cart-quantity')[0];
    var price = parseFloat(priceElement.innerText.replace("$", ""));
    var quantity = quantityElement.value;
    total = total + (price * quantity);

    document.getElementsByClassName('total-price')[0].innerText = "$" + total;

}
}
 

