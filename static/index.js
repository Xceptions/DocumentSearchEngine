document.addEventListener('DOMContentLoaded', function(){

    document.getElementById('add_document').addEventListener('click', addDocumentHandler);
    document.getElementById('search_btn').addEventListener('click', searchForWordsHandler);
    document.getElementById('clear_db').addEventListener('click', clearDBHandler);

    function delInput(user_input) {

        fetch('/delete', {
            method: "POST",
            body: JSON.stringify({
                document: user_input
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
            result_val = result['document_id']
            var added_strings = '<div class="">';
            for (let idx in result_val) {
                var temp = '<p>';
                temp += result_val[idx];
                temp += '<button onclick=delInput("' + result_val[idx] + '") type="button">Delete input</button></p>';
                added_strings += temp;
            };
            added_strings += '</div>';
            console.log(added_strings)
            document.getElementById('wordsAddedToCorpus').innerHTML = added_strings;	
        });
    }

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
            result_val = result['document_id']
            var added_strings = '<div class="">';
            for (let idx in result_val) {
                var temp = '<p>';
                temp += result_val[idx];
                temp += '<button onclick=delInput("' + result_val[idx] + '") type="button">Delete input</button></p>';
                added_strings += temp;
            };
            added_strings += '</div>';
            console.log(added_strings)
            document.getElementById('wordsAddedToCorpus').innerHTML = added_strings;	
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

    function clearDBHandler() {
        fetch('/cleardb')
        .then(function( response ){
            return response.json();
        })
        .then(function( result ){
            console.log(JSON.stringify(result));
        });
    }
});