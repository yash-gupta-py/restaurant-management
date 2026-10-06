function getCSRFToken() {
    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
}

async function loadMenuItems() {
    const menuList = document.getElementById("menu-list");

    try {
        const response = await fetch("/api/v1/menu/menu-items/");

        if (!response.ok) {
            throw new Error("Failed to fetch menu items");
        }

        const items = await response.json();

        menuList.innerHTML = "";

        if (items.length === 0) {
            menuList.innerHTML = "<p>No menu items found.</p>";
            return;
        }

        items.forEach(item => {
            const card = document.createElement("div");

            card.className = "menu-card";

            card.innerHTML = `
                <div class="menu-card-content">

                    <h3>${item.name}</h3>

                    <p class="category">
                        ${item.category_name}
                    </p>

                    <p class="description">
                        ${item.description || "No description available"}
                    </p>

                    <div class="menu-card-footer">

                        <strong>₹${item.price}</strong>

                        <span class="${item.is_available ? "available" : "unavailable"}">
                            ${item.is_available ? "Available" : "Unavailable"}
                        </span>

                    </div>

                    <div class="menu-actions">

                        <button onclick="editMenuItem(${item.id})">
                            ✏️ Edit
                        </button>

                        <button
                            class="delete-button"
                            onclick="deleteMenuItem(${item.id})">
                            🗑️ Delete
                        </button>

                    </div>

                </div>
            `;

            menuList.appendChild(card);
        });

    } catch (error) {
        console.error("Menu error:", error);

        menuList.innerHTML = `
            <p class="error">
                Failed to load menu items.
            </p>
        `;
    }
}


async function loadCategories() {

    const addCategorySelect =
        document.getElementById("item-category");

    const editCategorySelect =
        document.getElementById("edit-item-category");


    try {

        const response =
            await fetch("/api/v1/menu/categories/");


        if (!response.ok) {
            throw new Error(
                "Failed to fetch categories"
            );
        }


        const categories =
            await response.json();


        categories.forEach(category => {

            if (!category.is_active) {
                return;
            }


            // Add form category

            const addOption =
                document.createElement("option");

            addOption.value = category.id;

            addOption.textContent =
                category.name;

            addCategorySelect.appendChild(
                addOption
            );


            // Edit form category

            const editOption =
                document.createElement("option");

            editOption.value = category.id;

            editOption.textContent =
                category.name;

            editCategorySelect.appendChild(
                editOption
            );

        });


    } catch (error) {

        console.error(
            "Category error:",
            error
        );
    }
}

async function createMenuItem(event) {
    event.preventDefault();

    const message = document.getElementById("form-message");

    const item = {
        name: document.getElementById("item-name").value,
        description: document.getElementById("item-description").value,
        price: document.getElementById("item-price").value,
        category: document.getElementById("item-category").value,
        is_available: document.getElementById("item-available").checked
    };

    try {
        const response = await fetch("/api/v1/menu/menu-items/", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },

            body: JSON.stringify(item)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(data));
        }

        message.textContent = "Menu item added successfully.";
        message.className = "success";

        document.getElementById("menu-form").reset();
        document.getElementById("item-available").checked = true;

        await loadMenuItems();

    } catch (error) {

        console.error("Create menu item error:", error);

        message.textContent = "Failed to add menu item.";
        message.className = "error";
    }
}

let editingItemId = null;


async function editMenuItem(id) {

    editingItemId = id;

    try {

        const response = await fetch(
            `/api/v1/menu/menu-items/${id}/`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch menu item");
        }

        const item = await response.json();

        document.getElementById("edit-item-name").value =
            item.name;

        document.getElementById("edit-item-description").value =
            item.description || "";

        document.getElementById("edit-item-price").value =
            item.price;

        document.getElementById("edit-item-category").value =
            item.category;

        document.getElementById("edit-item-available").checked =
            item.is_available;

        document
            .getElementById("edit-form-message")
            .textContent = "";

        document
            .getElementById("edit-menu-form")
            .classList.remove("hidden");

    } catch (error) {

        console.error("Edit load error:", error);

        alert("Failed to load menu item.");
    }
}

async function updateMenuItem(event) {

    event.preventDefault();

    const message =
        document.getElementById("edit-form-message");

    const item = {

        name:
            document.getElementById("edit-item-name").value,

        description:
            document.getElementById("edit-item-description").value,

        price:
            document.getElementById("edit-item-price").value,

        category:
            document.getElementById("edit-item-category").value,

        is_available:
            document.getElementById("edit-item-available").checked
    };


    try {

        const response = await fetch(
            `/api/v1/menu/menu-items/${editingItemId}/`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },

                body: JSON.stringify(item)
            }
        );


        const data = await response.json();


        if (!response.ok) {

            console.error(data);

            throw new Error(
                "Failed to update menu item"
            );
        }


        message.textContent =
            "Menu item updated successfully.";

        message.className = "success";


        await loadMenuItems();


        setTimeout(() => {

            closeEditForm();

        }, 700);


    } catch (error) {

        console.error("Update error:", error);

        message.textContent =
            "Failed to update menu item.";

        message.className = "error";
    }
}

function closeEditForm() {

    document
        .getElementById("edit-menu-form")
        .classList.add("hidden");

    document
        .getElementById("edit-form")
        .reset();

    editingItemId = null;
}

async function deleteMenuItem(id) {

    const confirmed = confirm(
        "Are you sure you want to delete this menu item?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `/api/v1/menu/menu-items/${id}/`,
            {
                method: "DELETE",

                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete menu item");
        }

        await loadMenuItems();

    } catch (error) {

        console.error("Delete error:", error);

        alert("Failed to delete menu item.");
    }
}

document
    .getElementById("refresh-menu")
    .addEventListener("click", loadMenuItems);


document
    .getElementById("show-add-form")
    .addEventListener("click", () => {
        document
            .getElementById("add-menu-form")
            .classList.remove("hidden");
    });


document
    .getElementById("cancel-form")
    .addEventListener("click", () => {
        document
            .getElementById("add-menu-form")
            .classList.add("hidden");
    });


document
    .getElementById("menu-form")
    .addEventListener("submit", createMenuItem);

document
    .getElementById("edit-form")
    .addEventListener(
        "submit",
        updateMenuItem
    );


document
    .getElementById("cancel-edit-form")
    .addEventListener(
        "click",
        closeEditForm
    );


document
    .getElementById("close-edit-form")
    .addEventListener(
        "click",
        closeEditForm
    );

loadMenuItems();
loadCategories();