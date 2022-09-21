let updateBtns = document.getElementById('update_cart')

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        location.reload()
        
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateCart(productId,action)

        }

    })
}
function  updateCart(id,action){
    console.log('User is authenticated, sending data..')
    let url = "/updatecart/"
    fetch(url,{
        method:'POST',
        headers:{
            "Content-Type":"application/json",
            'X-CSRFToken':csftoken,
        },
        body:JSON.stringify({'productId':id,'action':action})
    })
    .then(response => response.json())
     
    .then(data => console.log('data:',data))
       
       
    }


