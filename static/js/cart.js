var updateButton = document.getElementsByClassName('update-cart-data')

for(var i=0; i<updateButton.length; i++){
    updateButton[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)

        if (user== 'AnonymousUser'){
            console.log('not logged in')

        }
        else{
            updateOrders(productId, action)
        }
    })

}

// sending data to update_data_view
function updateOrders(productId, action){
    console.log('logged in')

    var url = '/update-cart/'

    //using fetch api to send data

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })


}