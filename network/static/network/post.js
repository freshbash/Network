//This component represents each individual tile

const Post = (props) => {
    //State variables
    const [postContent, setPostContent] = React.useState('');
    const [numLikes, setNumLikes] = React.useState(0);
    const [hasLiked, setHasLiked] = React.useState(false);
    const [editMode, setEditMode] = React.useState(false);

    //Set state according to the props received
    setPostContent(props.content.post);
    setNumLikes(props.content.likes);
    setHasLiked(props.liked);

    //Edit button
    const editButton = <div><button className="edit" onClick={handleEdit}><i class="bi bi-pencil"></i></button></div>;

    //Cancel edit button
    const cancelButton = <div><button className="edit" onClick={handleEdit}><i class="bi bi-x-circle-fill"></i></button></div>;

    //Save edit button
    const saveButton = <div><button className="save" onClick={handleSave}>Save</button></div>;

    //Handle like button click
    function handleLike() {        

        //Send PUT request to the server to update the likes
        fetch(`/like/${props.content.id}`, {
            method: "PUT",
            body: JSON.stringify({                
                "hasLiked": !hasLiked
            })
        })
        .then(response => response.json())
        .then(data => {
            //Update the state

            //Increment decrement numLikes based of hasLiked
            setNumLikes(data.likes);

            //Update hasLiked state
            setHasLiked(!hasLiked);
        });
    }

    //Handle the edit button click
    function handleEdit() {
        //Change the state
        setEditMode(!editMode);
    }

    //Handle save edit button click
    function handleSave() {

        const newContent = document.querySelector("#enabledTextBox").value;

        //Set edit mode to off
        setEditMode(false);

        //If the content is not an empty string and is different from the existing content, send update request to server
        if (newContent !== postContent && newContent !== '') {
            //Send a PUT request to the server
            fetch(`/edit/${props.content.id}`, {
                method: "PUT",
                body: JSON.stringify({
                    "content": postContent
                })
            })
            .then(response => {
                //If the response code is 204, convert the response to json
                if (response.status === 204) {
                    response.json()
                }
            })
            .then(data => setPostContent(data.post)); //Update the state
        }
    }
    

    return (
        <div className="single-post">
            <div className="user-bar">
                <div id="user-name-post"><a href={`/user/${props.content.user}`}>{props.content.user}</a></div>
                {props.is_owner && !editMode ? editButton : props.is_owner && editMode ? cancelButton : null}
            </div>                    
            <div className="content-box" id="">
                {editMode ? <textarea id="enabledTextBox">{postContent}</textarea> : <textarea disabled>{postContent}</textarea>}
                {editMode ? saveButton : null}
            </div>
            <div className="timestamp">{props.content.timestamp}</div>
            <div className="likes">
                <button id="img" className="img" onClick={handleLike}>
                    {hasLiked ? <i class="bi bi-star-fill"></i> : <i class="bi bi-star"></i>}
                </button>
                <div class="like_count">{numLikes}</div>
            </div>
        </div>
    )
}

//Export the component
export default Post;
