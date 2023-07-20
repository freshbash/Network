//This component represents each individual tile

const post = (props) => {
    //State variables
    const [numLikes, setNumLikes] = React.useState(0);
    const [hasLiked, setHasLiked] = React.useState(false);
    const [editMode, setEditMode] = React.useState(false);

    return (
        <div class="single-post">
            <div class="user-bar">
                <div id="user-name-post"><a href="/user/"></a></div>                
                <div><button class="edit" value="">Edit</button></div>
            </div>                    
            <div class="content-box" id=""></div>
            <div class="timestamp"></div>
            <div class="likes">
                <div id="img" class="img">
                    <i class="bi bi-star"></i>
                </div>
                <div class="like_count">{numLikes}</div>
            </div>
        </div>
    )
}