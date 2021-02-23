updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if (user === "AnonymousUser") {
      console.log("Not Logged in");
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  var url = "/update_item/";

  $.ajax({
    url: url,
    data: {
      productId: productId,
      action: action,
    },
    dataType: "json",

    success: function (data) {
      window.location.reload();

      console.log("save");
    },
  });

  console.log("productId:", productId, "action:", action);
  console.log("USER:", user);
  console.log(" User is logged in , Sending data...");
}
