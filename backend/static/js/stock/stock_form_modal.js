import { getCSRFToken } from "../utils.js";
import { parseDate } from "../utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const stockForm = document.getElementById("stockForm");
  const stockModal = bootstrap.Modal.getOrCreateInstance(
    document.getElementById("stockFormModal")
  );

  let currentStockId = null;

  // Clicking edit button in stock list
  document.querySelectorAll(".edit-stock").forEach((button) => {
    button.addEventListener("click", (event) => {
      const row = event.target.closest("tr");
      currentStockId = row.dataset.id;

      document.getElementById("stockName").value = row.dataset.name;
      document.getElementById("stockTicker").value = row.dataset.ticker;
      document.getElementById("stockMarket").value = row.dataset.market;
      document.getElementById("stockType").value = row.dataset.type;
      document.getElementById("stockListedDate").value = parseDate(
        row.dataset.listed_date
      );

      stockModal.show();
    });
  });

  stockForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    // Save stock logic here
    const name = document.getElementById("stockName").value.trim();
    const ticker = document.getElementById("stockTicker").value.trim();
    const stockMarket = document
      .getElementById("stockMarket")
      .value.toLowerCase();
    const stockType = document.getElementById("stockType").value.toLowerCase();
    const stockListedDate = document
      .getElementById("stockListedDate")
      .value.trim();

    if (!name) {
      alert("종목 이름을 입력해주세요.");
      return;
    }

    if (!ticker) {
      alert("종목 티커를 입력해주세요.");
      return;
    }

    if (!stockMarket) {
      alert("종목 시장을 입력해주세요.");
      return;
    }

    if (!stockListedDate) {
      alert("상장일을 입력해주세요.");
      return;
    }

    const payload = {
      name: name,
      ticker: ticker,
      market: stockMarket,
      type: stockType,
      listed_date: stockListedDate,
    };

    // save stock via API
    if (currentStockId) {
      await update_stock(currentStockId, payload);
    } else {
      await create_stock(payload);
    }

    window.location.reload(); // Reload the page to reflect changes
  });

  // Function to update an existing stock
  async function update_stock(id, payload) {
    try {
      const response = await fetch(`/api/stock/stocks/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken() || "",
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log("Stock updated successfully:", data);
      stockModal.hide(); // Hide the modal after updating
      alert("종목이 업데이트되었습니다.");
    } catch (error) {
      console.error("Error updating stock:", error);
    }
  }
  // Function to create a new stock
  async function create_stock(payload) {
    try {
      const response = await fetch("/api/stock/stocks/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken() || "",
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        if (response.status === 400) {
          alert("입력한 정보가 올바르지 않거나 이미 존재하는 종목입니다.");
          return;
        } else {
          alert("네트워크 오류가 발생했습니다. 나중에 다시 시도해주세요.");
          throw new Error("Network response was not ok");
        }
      }
      const data = await response.json();
      console.log("Stock created successfully:", data);
      stockModal.hide(); // Hide the modal after creating
      alert("종목이 생성되었습니다.");

      stockForm.reset();

      return data.id; // Return the new stock ID
    } catch (error) {
      console.error("Error creating stock:", error);
    }
  }
});
