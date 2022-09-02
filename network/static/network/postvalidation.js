document.addEventListener('DOMContentLoaded', function() {
    let text = document.querySelector('.form-control');
    let btn = document.querySelector('.btn');
    btn.disabled = true;

    text.onkeyup = () => {
        let user_content = document.querySelector('.form-control').value;
        if (user_content.length > 0){
            btn.disabled = false;
        }
        else{
            btn.disabled = true;
        }
    }
})