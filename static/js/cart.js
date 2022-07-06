document.addEventListener('DOMContentLoaded', () => {
    let buttons = document.getElementsByClassName('add-to-cart');

    for (const button of buttons) {
        button.addEventListener('click', (event) => {
            const el = event.target;
            const product_id = el.dataset.productId;
            const url = el.href;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id }),
            })
            .then(response => response.json())
            .then(json => {
                toastr.success(json.message, 'Shopping cart updated')
            });

            event.preventDefault();
        });
    }
});

