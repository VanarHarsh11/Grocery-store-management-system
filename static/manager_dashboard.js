const plusbutton = document.getElementById('plus-button') //add-category button
const formcontainer  = document.getElementById('form-container') //category form

const text = document.getElementById('text')
let isvisible = true;
plusbutton.addEventListener('click',() => {
    formcontainer.style.display = isvisible ? 'block':'none';
    text.style.display = false ? 'block':'none';
});

const prdctbutton = document.getElementsByClassName('product-button');
const pdrctform = document.getElementById('prdct-form-container');
const catbox = document.getElementById('category-list')

for(const button of prdctbutton){
    button.addEventListener('click',function(){
        pdrctform.style.display = 'block';
        catbox.style.display = 'none';
    });
}
