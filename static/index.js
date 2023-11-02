document.addEventListener('DOMContentLoaded', function(){

    document.getElementById('add_document').addEventListener('click', addDocumentHandler);
    document.getElementById('search_btn').addEventListener('click', searchForWordsHandler);

    function addDocumentHandler() {
        var input_document = document.getElementById('input_document').value;

        fetch('/add', {
            method: "POST",
            body: JSON.stringify({
                document: input_document
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then(function( response ){
            return response.json();
        })
        .then(function( result ){
            console.log(JSON.stringify(result));	
        });
    }

    function searchForWordsHandler() {
        var input_document = document.getElementById('search_term').value;

        fetch('/search', {
            method: "POST",
            body: JSON.stringify({
                document: input_document
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then(function( response ){
            return response.json();
        })
        .then(function( result ){
            console.log(JSON.stringify(result));	
        });
    }
});