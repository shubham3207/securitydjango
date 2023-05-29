var discountPrice = document.getElementsByClassName('discount-price')


for(var i=0; i<discountPrice.length; i++){
    discountPrice[i].addEventListener('click', function(){
        var orderId = this.dataset.product
        var action = this.dataset.action

        console.log('orderId:', orderId, 'action:', action)

        console.log('USER:', user)

        if(user == 'AnonymousUser'){
            console.log('not logged in')
        }

        else{
            updateDiscount(orderId, action)
        }

        



        

    })
}

function updateDiscount(orderId, action){

    var url = '/update-discount/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            
        },
        body: JSON.stringify({'orderId': orderId, 'action': action})
    })

    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })



}