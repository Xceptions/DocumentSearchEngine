document.addEventListener('DOMContentLoaded', function(){

    document.getElementById('add_document').addEventListener('click', addDocumentHandler);

    function addDocumentHandler() {
        var input_document = document.getElementById('input_document').value;
        console.log(input_document)

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
});