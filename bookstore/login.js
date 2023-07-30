function showmsg(msg){
    // const queryString = window.location.search;
    // const urlParams = new URLSearchParams(queryString);
    // const msg = urlParams.get('msg')
    // console.log(msg);
    if(msg != null){
        alert(msg);
        return true;
    }else{
        return false;
    }
}