//Component to represent page navigator

const PageNavigator = (props) => {
    return (
        <div>
            <nav class="pgn" aria-label="Page navigation example">
                <ul class="pagination justify-content-center">
                    <li id="prev" class="page-item disabled">
                        <a id="link-prev" href="" class="page-link" tabindex="-1" aria-disabled="true">Previous</a>
                    </li>            
                    <li id="item-{{ page }}" class="page-item"><a id="link-{{ page }}" class="page-link" href="{% url 'nthpage' 'all' page %}">{{ page }}</a></li>
                    <li id="next" class="page-item">
                            <a id="link-next" href="" class="page-link">Next</a>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

export default PageNavigator;