const cartItems = [];

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.id.split('-')[3];
            const product = {
                id: productId,
                title: document.querySelector(`#add-to-cart-${productId}`).previousElementSibling.previousElementSibling.previousElementSibling.textContent,
                price: document.querySelector(`#add-to-cart-${productId}`).previousElementSibling.previousElementSibling.textContent,
                image: document.querySelector(`#add-to-cart-${productId}`).previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.src
            };
            cartItems.push(product);
            updateCart(product);
        });
    });