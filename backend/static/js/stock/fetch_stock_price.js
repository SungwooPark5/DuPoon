import { getCSRFToken } from "../utils.js";

const updateStockPriceButton = document.getElementById(
  "updateStockPriceButton"
);

updateStockPriceButton.addEventListener("click", async function (event) {
  event.preventDefault();
  const url = "/api/stock/price/fetch/";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() || "",
      },
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    alert("가격 업데이트 요청이 전달되었습니다.");
  } catch (error) {
    console.error("Error updating strategy:", error);
  }
});
