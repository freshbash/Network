//Component to let user follow or unfollow another profile

//Import the dependencies
import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

//Component
const Follow = () => {
    //State
    const [userName, setUserName] = useState('');
    const [followerCount, setFollowerCount] = useState(null);
    const [isFollowing, setIsFollowing] = useState(false);

    //Fetch data on mount
    useEffect(() => {
        const domNode = document.querySelector("#component-data");
        const componentData = JSON.parse(domNode.textContent);
        setUserName(componentData.username);
        setFollowerCount(componentData.follower_count);
        setIsFollowing(componentData.is_following);
    }, [])

    //Function to handle click on the follow/unfollow button
    function handleClick() {
        fetch(`/follow/${userName}`, {
            method: "PUT",
            body: JSON.stringify({
                "follow": !isFollowing
            })
        })
        .then(response => {
            if (response.status === 204) {
                if (isFollowing) {
                    setFollowerCount(followerCount - 1);
                }
                else {
                    setFollowerCount(followerCount + 1)
                }
                setIsFollowing(!isFollowing);
            }
        })
    }

    return (
        <div className="d-flex flex-row">
            <div className="d-flex flex-column">
                <div className="fs-5 fw-bold">Followers</div>
                <div>{ followerCount }</div>
            </div>
            <div>
                <button className="btn btn-primary" onClick={handleClick}>{isFollowing ? "Unfollow" : "Follow"}</button>
            </div>
        </div>
    )
}

//Mount the component to the dom

//Get the dom element
const domNode = document.querySelector("#follow-button");
const root = createRoot(domNode);
root.render(<Follow />);
