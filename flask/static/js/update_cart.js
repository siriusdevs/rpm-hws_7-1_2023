function updateCart(product) {
	let cartItem = document.createElement('div');
	cartItem.classList.add('cart-item');
	cartItem.innerHTML = `
		<img src="${product.image}" alt="Product">
		<div>
		<h3>${product.title}</h3>
		<p class="price">${product.price}</p>
		<div class="quantity-container">
			<button class="decrement-btn"><</button>
			<input type="text" value="1" class="quantity">
			<button class="increment-btn">></button>
		</div>
		<button class="remove-btn">Remove</button>
		</div>
	`;
  let cartItems = document.querySelector('.cart-items');
  let cartTotal = document.querySelector('.cart-total h3');
  let items = cartItems.getElementsByClassName('cart-item');
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    let itemPrice = parseFloat(items[i].querySelector('.price').textContent.replace('$', ''));
    let itemQuantity = items[i].querySelector('.quantity').value;
    total += itemPrice * itemQuantity;
  }
  total = Math.round(total * 100) / 100;
  cartTotal.textContent = `Total: $${total}`;
  cartItems.append(cartItem);

  let removeBtns = document.querySelectorAll('.remove-btn');
  removeBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      btn.parentElement.parentElement.remove();
      updateTotal();
    });
  });

  let quantityInputs = document.querySelectorAll('.quantity');
  quantityInputs.forEach(function(input) {
    updateTotal();
    input.addEventListener('change', function() {
      if (input.value <= 0) {
        input.value = 1;
      }
      updateTotal();
    });
  });

  let incrementBtns = document.querySelectorAll('.increment-btn');
  incrementBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      let quantityInput = btn.previousElementSibling;
      let currentQuantity = parseInt(quantityInput.value);
      quantityInput.value = currentQuantity + 1;
      updateTotal();
    });
  });

  let decrementBtns = document.querySelectorAll('.decrement-btn');
  decrementBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      let quantityInput = btn.nextElementSibling;
      let currentQuantity = parseInt(quantityInput.value);
      if (currentQuantity > 1) {
        quantityInput.value = currentQuantity - 1;
        updateTotal();
      }
    });
  });

  function updateTotal() {
    let items = cartItems.getElementsByClassName('cart-item');
    let total = 0;
    for (let i = 0; i < items.length; i++) {
      let itemPrice = parseFloat(items[i].querySelector('.price').textContent.replace('$', ''));
      let itemQuantity = items[i].querySelector('.quantity').value;
      total += itemPrice * itemQuantity;
    }
    total = Math.round(total * 100) / 100;
    cartTotal.textContent = `Total: $${total}`;
  }
}