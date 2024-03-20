var updateBtns = document.body.getElementsByClassName('update-cart')


for (let i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId,action)
        console.log(user)

        if (user =='AnonymousUser'){
            // console.log("user is not logged in")
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

const addCookieItem = (productId, action) => {
    console.log("user is not logged in..")

    console.log(cart)

    if (action == 'add'){
        
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] +=1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -=1
        
        if(cart[productId]['quantity'] <=0){
            console.log("item is deleted from cart")
            delete cart[productId]
        }
    }
    console.log(cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}



const updateUserOrder = (productId, action) => {
    // console.log('user logged in data added')
    var post_url = '/update_item/'

    fetch(post_url,{
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
            
        },
        body: JSON.stringify({'productId': productId, 'action':action}),
    }
    )
    .then((response) => {
        
        return response.json()
    })
    .then(() => {
        location.reload()
    })
}