document.addEventListener('DOMContentLoaded', function() {
    const links = Array.from(document.querySelectorAll('.page-link'));
    const link = window.location.href;
    const page = parseInt(link.slice(-1));
    const last_page = parseInt(links.slice(-2, -1)[0].innerHTML);

    if (link.slice(-6, -2) === 'page'){
        document.querySelector('#prev').className = 'page-item';
    }

    if (page === last_page || links.length === 3){
        document.querySelector('#next').className = 'page-item disabled';
    }
    
    if (page){
        document.querySelector(`#item-${page}`).className = 'page-item disabled';
        if (link.includes('following')){
            document.querySelector('#link-prev').href = `/following/page-${page - 1}`;
            document.querySelector('#link-next').href = `/following/page-${page + 1}`;
        }
        else if (link.includes('profile')){
            document.querySelector('#link-prev').href = `/profile/page-${page - 1}`;
            document.querySelector('#link-next').href = `/profile/page-${page + 1}`;
        }
        else if(link.includes('all')){
            document.querySelector('#link-prev').href = `/all/page-${page - 1}`;
            document.querySelector('#link-next').href = `/all/page-${page + 1}`;
        }
        
    }
    else{
        document.querySelector('#item-1').className = 'page-item disabled';

        if (link.includes('following')){
            document.querySelector('#link-next').href = `/following/page-${2}`;
        }
        else if (link.includes('profile')){            
            document.querySelector('#link-next').href = `/profile/page-${2}`;
        }
        else{            
            document.querySelector('#link-next').href = `/all/page-${2}`;
        }
    }

});
