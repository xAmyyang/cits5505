// Select all ingredient chips
const chips = document.querySelectorAll(".sc-chip");

// Select the container for selected ingredients and the empty message
const selectedBox = document.querySelector(".sc-selected-box");
const emptyText = document.querySelector(".sc-empty-text");
const selectedInputs = document.getElementById("selectedIngredientsInputs");
const findRecipesBtn = document.getElementById("findRecipesBtn");
const ingredientSearch = document.getElementById("ingredientSearch");
const ingredientSearchBtn = document.getElementById("ingredientSearchBtn");

function syncSelectionState() {
    const selectedCount = selectedBox.querySelectorAll("span").length;
    emptyText.style.display = selectedCount > 0 ? "none" : "block";
    findRecipesBtn.disabled = selectedCount === 0;
}

function filterIngredients() {
    const query = ingredientSearch.value.trim().toLowerCase();

    chips.forEach(chip => {
        const ingredient = chip.dataset.ingredient.toLowerCase();
        chip.style.display = ingredient.includes(query) ? "" : "none";
    });
}

// Add click event to each chip
chips.forEach(chip => {
    chip.addEventListener("click", () => {

        // Toggle selected state on the clicked chip
        chip.classList.toggle("selected");

        const ingredient = chip.dataset.ingredient;

        if (chip.classList.contains("selected")) {
            // If selected → create a new chip in the selected box
            const item = document.createElement("span");
            item.textContent = ingredient;

            // Apply same chip styling
            item.classList.add("sc-chip", "selected");

            // Store ingredient name for future reference
            item.setAttribute("data-name", ingredient);

            selectedBox.appendChild(item);

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "ingredients";
            input.value = ingredient;
            input.setAttribute("data-name", ingredient);
            selectedInputs.appendChild(input);

        } else {
            // If unselected → remove the corresponding chip from selected box
            const items = selectedBox.querySelectorAll("span");

            items.forEach(item => {
                if (item.textContent === ingredient) {
                    item.remove();
                }
            });

            const inputs = selectedInputs.querySelectorAll("input");
            inputs.forEach(input => {
                if (input.value === ingredient) {
                    input.remove();
                }
            });
        }

        syncSelectionState();
    });
});

ingredientSearch.addEventListener("input", filterIngredients);
ingredientSearchBtn.addEventListener("click", filterIngredients);

syncSelectionState();
