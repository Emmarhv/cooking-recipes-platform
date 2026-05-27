// Lo mio

$(document).ready(function() {


    var base_url = $("#recipe-data").data("url");
 
 
 
 
    $('.original').hover(
        function() {
            if (!$(this).find("form.reply-form").length) {
                var link = $("<a>")
                    .attr("href", "#")
                    .addClass("reply")
                    .text("Give your opinion! Write your own comment!");
 
 
                link.click(function() {
                    var comment_id = parseInt(
                        $(this)
                            .parent()
                            .attr("data-comment-id")
                    );
 
 
                    var current_user_id = parseInt(
                        $(this)
                            .parent()
                            .attr("data-current-user-id")
                    );
 
 
                    // Ensure that 'recipe' is accessible in this scope
                    var recipeId = $('#recipe-data').data('recipe-id');
                    if (recipeId) {
                        var formAction = "/new_comment_on_recipe";
                        var form = create_response_form(comment_id, recipeId, current_user_id, formAction);
                        $(this).parent().append(form);
                        $(this).remove();
                    } else {
                        console.error("Recipe information is missing or invalid.");
                    }
                });
 
 
                $(this).append(link);
            }
        },
        function() {
            $(this).find("a.reply")
                .remove();
        }
    );
 });
 
 
 
 
 
 
 var create_response_form = function(comment_id, recipe_id, current_user_id, formAction) {
    var form = $("<form>")
        .attr("method", "post")
        .attr("action", formAction)
        .addClass("reply-form");
 
 
    var hiddenResponseTo = $("<input>")
        .attr("type", "hidden")
        .attr("name", "response_to")
        .attr("value", comment_id);
    var hiddenRecipeId = $("<input>")
        .attr("type", "hidden")
        .attr("name", "recipe_id")
        .attr("value", recipe_id);  // Insert the correct variable or value here
    var hiddenUserId = $("<input>")
        .attr("type", "hidden")
        .attr("name", "user_id")
        .attr("value", current_user_id);  // Insert the correct variable or value here
 
 
    // Add a hidden field to indicate if it's a comment on comment
    var hiddenCommentType = $("<input>")
        .attr("type", "hidden")
        .attr("name", "comment_type")
        .attr("value", "comment_on_recipe");
 
 
    var textarea = $("<textarea>")
        .attr("name", "text")
        .attr("rows", "5")
        .attr("cols", "50")
        .attr("placeholder", "Escribe tu comentario...");
    var submit = $("<input>")
        .attr("type", "submit")
        .attr("value", "Create comment");
    var cancel = $("<input>")
        .attr("type", "button")
        .attr("value", "Cancel")
        .click(function(){
            $(this).closest('.reply-form').remove();
        });
    form.append(hiddenResponseTo)
        .append(hiddenRecipeId)
        .append(hiddenUserId)
        .append(hiddenCommentType)  // Add the comment type field
        .append(textarea)
        .append(submit)
        .append(cancel);
    console.log('hola holita')
    return form;
 }
 
 







//EMMA
document.addEventListener("keyup", e => {
    if (e.target.matches("#searcher")) {
        const searchTerm = e.target.value.trim();
        //if (e.key === "Escape") e.target.value = "";

        if (searchTerm === "") {
            const listRecipes = document.getElementById('listRecipes');
            listRecipes.innerHTML = ''; // Limpiar la lista cuando el cuadro de búsqueda está vacío
            return;
        }

        fetch(`/api/search?term=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                console.log("Data from API:", data);
                // Manipular los datos aquí (por ejemplo, construir y mostrar resultados de búsqueda)
                const listRecipes = document.getElementById('listRecipes');
                listRecipes.innerHTML = ''; // Limpiar la lista antes de agregar nuevos elementos

                data.result.forEach(recipe => {
                    const recipeElement = document.createElement('li');
                    recipeElement.classList.add('recipe');
                    recipeElement.innerHTML = `<a href="/recipe/${recipe.id}">${recipe.title}</a>`;
                    listRecipes.appendChild(recipeElement);
                });
            })
            .catch(error => console.error('Error:', error));
    }
});






