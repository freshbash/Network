document.addEventListener('DOMContentLoaded', function() {
    
    let edit_btns = document.querySelectorAll('.edit');


    edit_btns.forEach(btn => {
        btn.onclick = () => {
            debugger;
            let post = document.querySelector(`#post-${btn.value}`);            
            if (btn.innerHTML === "Edit"){
                btn.style.backgroundColor = 'darkred';
                btn.style.color = 'white';
                const content = post.innerHTML;
                post.innerHTML = '';
                let text = document.createElement('textarea');
                text.style.width = '100%';
                text.style.marginTop = '10px';
                text.style.borderRadius = '10px';
                text.style.padding = '10px';
                text.innerHTML = content;
                text.id = 'edited-text';
                post.appendChild(text);                  
                btn.innerHTML = 'Cancel';
                debugger;
                let save = document.createElement('button');
                save.innerHTML = 'Save';
                save.id = 'save';
                save.style.marginLeft = '10px';
                btn.parentElement.appendChild(save);
                save.disabled = true;
                text.onkeyup = () => {
                    const edited = document.querySelector('#edited-text').value;
                    if ((edited !== content) && edited !== ''){
                        save.disabled = false;
                    }
                    else {
                        save.disabled = true;
                    }
                }

                save.onclick = () => {
                    // Save the post to database.
                    const edited = document.querySelector('#edited-text').value;
                    fetch(`/edit/${btn.value}`, {
                        method: 'POST',
                        body: JSON.stringify({
                            "post": edited
                        })
                    })
                    .then(result => {
                        console.log(result);
                        btn.innerHTML = "Edit";
                        btn.style.backgroundColor = 'white';
                        btn.style.color = 'black';
                        const content = post.children[0].innerHTML;
                        post.innerHTML = edited;
                        btn.parentElement.removeChild(save);

                    });


                }
            } else {
                btn.innerHTML = "Edit";
                btn.style.backgroundColor = 'white';
                btn.style.color = 'black';
                const content = post.children[0].innerHTML;
                post.innerHTML = content;
                const save = document.querySelector('#save');
                btn.parentElement.removeChild(save);

            }
        }

    });
});
