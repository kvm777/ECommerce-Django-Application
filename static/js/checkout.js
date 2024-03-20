
// check wether the internal is override external or not...

var shipping = '{{order.shipping}}'
var total = '{{order.get_cart_total}}'

if (user != 'AnonymousUser'){
    document.getElementById('user-info').innerHTML = ''
}

if (shipping == 'False'){
    document.getElementById('shipping-info').innerHTML = ''
}

if (shipping == 'False' && user != 'AnonymousUser'){
    //hide entire form if user is logged in and show payment info 
    document.getElementById('form-wrapper').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
}

var form = document.getElementById('form')

form.addEventListener('submit', function(e){
    e.preventDefault()
    document.getElementById('form-button').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
})

document.getElementById('make-payment').addEventListener('click', function(){
    submitFormData();
})

function submitFormData(){
    console.log('data submitted successfully')

    var userFormData = {
        'name':null,
        'email':null,
        'total': total
    }
    var shippingInfo = {
        'address':null,
        'city':null,
        'state':null,
        'zipcode':null
    }

    if (shipping != 'False'){
        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.state = form.state.value
        shippingInfo.zipcode = form.zipcode.value
    }

    if (user == 'AnonymousUser'){
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }

    var post_url = '/process_order/'
    fetch(post_url,{
        method : 'POST',
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'userFormData': userFormData,
            'shippingInfo' : shippingInfo
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("data:", data)
        alert('payment Successfully completed')

        // var cart  = JSON.parse(getCookie('cart'))

        cart = {};
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

        window.location.href = "/"
    })
}



