function addToCart(id, place, to, price) {
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "place": place,
            "to": to,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }).catch(function(err){
        console.error(err)
    })
}


function updateCart(id, obj) {
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementById('total-amount')
        d2.innerText = new Intl.NumberFormat('de-DE').format(data.total_amount)
    }) // js promise
}

function deleteCart(id) {
    if (confirm("Quý khách muốn xóa vé đã đặt?") == true) {
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Conten-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            console.info(data)
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementById('total-amount')
            d2.innerText = new Intl.NumberFormat('de-DE').format(data.total_amount)

            let c = document.getElementById("product" + id)
            c.style.display = "none"
        }).catch(err => console.info(err)) // js promise
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch("/api/pay", {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                location.reload();
        }).catch(err => console.error(err))
    }
}