// Select all ingredient chips
const chips = document.querySelectorAll(".sc-chip");

// Select the container for selected ingredients and the empty message
const selectedBox = document.querySelector(".sc-selected-box");
const emptyText = document.querySelector(".sc-empty-text");

// Add click event to each chip
chips.forEach(chip => {
    chip.addEventListener("click", () => {

        // Toggle selected state on the clicked chip
        chip.classList.toggle("selected");

        const ingredient = chip.textContent;

        if (chip.classList.contains("selected")) {
            // If selected → create a new chip in the selected box
            const item = document.createElement("span");
            item.textContent = ingredient;

            // Apply same chip styling
            item.classList.add("sc-chip", "selected");

            // Store ingredient name for future reference
            item.setAttribute("data-name", ingredient);

            selectedBox.appendChild(item);

        } else {
            // If unselected → remove the corresponding chip from selected box
            const items = selectedBox.querySelectorAll("span");

            items.forEach(item => {
                if (item.textContent === ingredient) {
                    item.remove();
                }
            });
        }

        // Show or hide empty message depending on selection
        const hasItems = selectedBox.querySelectorAll("span").length > 0;
        emptyText.style.display = hasItems ? "none" : "block";
    });
});