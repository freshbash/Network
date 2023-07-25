//Component representing all posts in a page

//Import the dependencies
import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import Post from './post.js';
import PageNavigator from './page-navigator.js';

//Component that contains all the user posts
const AllPosts = () => {

    //State variable to store the data received from the template
    const [numPages, setNumPages] = useState(0);
    const [pageNum, setPageNum] = useState(1);
    const [path, setPath] = useState('');
    const [posts, setPosts] = useState([]);

    //Get data from the template and update state once the component mounts to the dom.
    useEffect(() => {
        const dataElement = document.querySelector("#data");
        let dataReceived = JSON.parse(dataElement.textContent);
        setNumPages(dataReceived.num_pages);
        setPageNum(dataReceived.page_num);
        setPath(dataReceived.path);
        const listItems = dataReceived.page.map(post => <Post key={post.content.id} postData={post} />);
        setPosts(listItems);
    }, []);

    return (
        <div>            
            {posts}
            <PageNavigator numPages={numPages} pageNum={pageNum} path={path} />
        </div>
    )
}


//Mount AllPosts to the DOM
const domNode = document.querySelector("#all-posts-root");
const root = createRoot(domNode);
root.render(<AllPosts />);
