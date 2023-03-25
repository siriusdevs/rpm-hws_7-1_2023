(function(){
    emailjs.init('0YiBCPA5DC-_Qq3Ob');
  })();
  
  document.getElementById('email-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Collect form data
    const email = document.querySelector('#email-form input[type="email"]').value;

    // Send email
    const templateParams = {
      email: email
    };
    emailjs.send('service_orinrog', 'template_ar2eb0e', templateParams)
      .then(function(response) {
        console.log('SUCCESS!', response.status, response.text);
      }, function(error) {
        console.log('FAILED...', error);
      });
    document.querySelector('#email-form input[type="email"]').value = '';
  });

  function addToCart(event) {
	event.preventDefault(); // prevent the default link behavior
  
	// get the product details
	const product = event.target.parentNode;
	const title = product.querySelector("h3").textContent;
	const price = product.querySelector(".price").textContent;
  
	// create a cart item object
	const item = { title, price };
  
	// add the item to the cart (you can use localStorage or a server-side database)
	console.log("Adding item to cart:", item);
  }
  
  document.getElementById("add-to-cart-1").addEventListener("click", addToCart);
  document.getElementById("add-to-cart-2").addEventListener("click", addToCart);
  document.getElementById("add-to-cart-3").addEventListener("click", addToCart);
  document.getElementById("add-to-cart-4").addEventListener("click", addToCart);
  
  function openCart() {
	var cartWindow = document.querySelector('.cart-window');
	cartWindow.classList.toggle('open');
  }