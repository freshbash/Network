//Component to represent page navigator


const PageNavigator = (props) => {

    //Compute the number of tabs the navigator will display
    const tabs = []
    for (let i = 1; i <= props.numPages; i++) {        
        tabs.push(
            <li className={props.pageNum === i ? "page-item active" : "page-item"}><a className="page-link" href="#">i</a></li>
        )
    }

    return (
        <div>
            <nav>
                <ul className="pagination">
                    <li className={props.pageNum === 1 ? "page-item disabled" : "page-item"}>
                        <a className="page-link" href="#">Previous</a>
                    </li>
                    {tabs}
                    <li className={props.pageNum === props.numPages ? "page-item disabled" : "page-item"}>
                        <a className="page-link" href="#">Next</a>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

//Export the component
export default PageNavigator;
