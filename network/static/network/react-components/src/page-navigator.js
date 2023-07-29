//Component to represent page navigator


const PageNavigator = (props) => {

    //Compute the number of tabs the navigator will display
    const tabs = []
    for (let i = 1; i <= props.numPages; i++) {        
        tabs.push(
            <li key={"page-"+i} className={props.pageNum === i ? "page-item active disabled" : "page-item"}><a className="page-link link-color" href={i === 1 ? props.path : `${props.path}/page-${i}`}>{i}</a></li>
        )
    }    

    return (
        <div className="mt-3">
            <nav>
                <ul className="pagination">
                    <li className={props.pageNum === 1 ? "page-item disabled" : "page-item"}>
                        <a className="page-link link-color" href={props.pageNum - 1 === 1 ? `${props.path}` : `${props.path}/page-${props.pageNum - 1}`} id="prev" >Previous</a>
                    </li>
                    {tabs}
                    <li className={props.pageNum === props.numPages ? "page-item disabled" : "page-item"}>
                        <a className="page-link link-color" href={`${props.path}/page-${props.pageNum + 1}`} id="next" >Next</a>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

//Export the component
export default PageNavigator;
