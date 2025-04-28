const triggerSearchBar = () => {
    searchBar = document.getElementById('search-bar');

    display = searchBar.style.display;

    if (display == 'block'){
        searchBar.style.display = 'none';
    } else{
        searchBar.style.display = 'block';
    }
}