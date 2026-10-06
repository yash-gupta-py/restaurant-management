async function getCount(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch ${url}`);
    }

    const data = await response.json();

    return data.length;
}


async function loadDashboard() {
    try {
        const menuCount = await getCount("/api/v1/menu/items/");
        const tableCount = await getCount("/api/v1/tables/");
        const reservationCount = await getCount("/api/v1/reservations/");
        const orderCount = await getCount("/api/v1/orders/");
        const paymentCount = await getCount("/api/v1/payments/");

        document.getElementById("menu-count").textContent = menuCount;
        document.getElementById("table-count").textContent = tableCount;
        document.getElementById("reservation-count").textContent = reservationCount;
        document.getElementById("order-count").textContent = orderCount;
        document.getElementById("payment-count").textContent = paymentCount;

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}


loadDashboard();