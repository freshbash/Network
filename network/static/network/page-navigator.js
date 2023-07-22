//Component to represent page navigator
const PageNavigator = (props) => {

    //Compute the number of tabs the navigator will display
    const tabs = []
    for (let i = 1; i <= props.numPages; i++) {        
        tabs.push(
            <li class={props.pageNum === i ? "page-item active" : "page-item"}><a class="page-link" href="#">i</a></li>
        )
    }

    return (
        <div>
            <nav>
                <ul class="pagination">
                    <li class={props.pageNum === 1 ? "page-item disabled" : "page-item"}>
                        <a class="page-link" href="#">Previous</a>
                    </li>
                    {tabs}
                    <li class={props.pageNum === props.numPages ? "page-item disabled" : "page-item"}>
                        <a class="page-link" href="#">Next</a>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

//Export the component
export default PageNavigator;
