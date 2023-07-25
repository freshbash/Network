//This component represents each individual tile

//Import the dependencies
import { useState } from "react";

const Post = (props) => {
    //State variables
    const [postContent, setPostContent] = useState(props.postData.content.post);
    const [numLikes, setNumLikes] = useState(props.postData.content.likes);
    const [hasLiked, setHasLiked] = useState(props.postData.liked);
    const [editMode, setEditMode] = useState(false);

    //Edit button
    const editButton = <div><button className="edit" onClick={handleEdit}><i className="bi bi-pencil"></i></button></div>;

    //Cancel edit button
    const cancelButton = <div><button className="edit" onClick={handleEdit}><i className="bi bi-x-circle-fill"></i></button></div>;

    //Save edit button
    const saveButton = <div><button className="save" onClick={handleSave}>Save</button></div>;

    //Handle like button click
    function handleLike() {        

        //Send PUT request to the server to update the likes
        fetch(`like/${props.postData.content.id}`, {
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

        //Get the newly inputted content
        const newContent = document.querySelector("#enabledTextBox").value;

        //Set edit mode to off
        setEditMode(false);

        //If the content is not an empty string and is different from the existing content, send update request to server
        if (newContent !== postContent && newContent !== '') {
            //Send a PUT request to the server            
            fetch(`edit/${props.postData.content.id}`, {
                method: "PUT",
                body: JSON.stringify({
                    "content": newContent
                })
            })
            .then(response => response.json()) //convert the response to json
            .then(data => setPostContent(data.post)); //Update the state
        }
    }
    

    return (
        <div className="single-post">
            <div className="user-bar">
                <div id="user-name-post"><a href={`/user/${props.postData.content.user}`}>{props.postData.content.user}</a></div>
                {props.postData.is_owner && !editMode ? editButton : props.postData.is_owner && editMode ? cancelButton : null}
            </div>                    
            <div className="content-box" id="">
                {editMode ? <textarea id="enabledTextBox" defaultValue={postContent}></textarea> : <div>{postContent}</div>}
                {editMode ? saveButton : null}
            </div>
            <div className="timestamp">{new Date(props.postData.content.timestamp).toString()}</div>
            <div className="likes">
                <button id="img" className="img" onClick={handleLike}>
                    {hasLiked ? <i className="bi bi-star-fill"></i> : <i className="bi bi-star"></i>}
                </button>
                <div className="like_count">{numLikes}</div>
            </div>
        </div>
    )
}

//Export the component
export default Post;
