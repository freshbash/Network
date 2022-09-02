document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#follow').addEventListener('click', follow);
});

function follow(){
    // debugger;
    let status = document.querySelector('#follow').innerHTML;
    const user = document.querySelector('#usr').innerHTML;
    let follows = parseInt(document.querySelector('#followers').innerHTML);
    if (status === "Follow"){
        fetch(`/follow/${user}`,
        {
            method: 'PUT',
            body: JSON.stringify({
                followers: true
            })
        }
        )
        .then(result => {
            console.log(result);
            document.querySelector('#follow').innerHTML = "Unfollow";
            follows++;
            document.querySelector('#followers').innerHTML = follows;
        });
    } else {
        fetch(`/follow/${user}`, {
            method: "PUT",
            body: JSON.stringify({
                followers: false
            })
        })
        .then(result => {
            console.log(result);
            document.querySelector('#follow').innerHTML = "Follow";
            follows--;
            document.querySelector('#followers').innerHTML = follows;
        })
    }
}
