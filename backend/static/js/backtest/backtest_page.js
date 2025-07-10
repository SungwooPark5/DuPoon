import { getCSRFToken } from "../utils.js";

document
  .getElementById("add-allocation")
  .addEventListener("click", function () {
    const allocationsDiv = document.getElementById("allocations");
    const index = allocationsDiv.children.length;

    const newAllocation = document.createElement("div");
    newAllocation.className = "allocation row mb-2";

    newAllocation.innerHTML = `
        <div class="col-md-5">
            <input name="allocations[${index}][ticker]" placeholder="티커" class="form-control mb-1" required="required">
        </div>
        <div class="col-md-5">
            <input name="allocations[${index}][weight]" placeholder="비율 (%)" class="form-control mb-1" required="required">
        </div>
        <div class="col-md-2">
            <button type="button" class="btn btn-outline-danger remove-allocation">삭제</button>
        </div>
    `;

    allocationsDiv.appendChild(newAllocation);
  });

document
  .getElementById("allocations")
  .addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-allocation")) {
      const allocationDiv = event.target.closest(".allocation");
      allocationDiv.remove();
    }
  });

document.getElementById("include_cash").addEventListener("change", function () {
  const value = this.value;
  const cashOptions = document.getElementById("cash-options");
  if (value === "true") {
    cashOptions.classList.remove("collapse");
  } else {
    cashOptions.classList.add("collapse");
  }
});

// request backtest result
document
  .getElementById("backtest-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
      allocations: [],
      start_date: formData.get("start_date") || null,
      end_date: formData.get("end_date") || null,
      rebalance_freq: formData.get("rebalance_frequency"),
      slippage: parseFloat(formData.get("slippage") || 0),
      include_cash: formData.get("include_cash") || false,
      cash_ticker: formData.get("cash_ticker") || "CASH",
      cash_weight: parseFloat(formData.get("cash_weight") / 100 || 0),
    };

    // Calculate allocations
    const allocationKeys = [...formData.keys()].filter((k) =>
      k.startsWith("allocations[")
    );
    const tickers = allocationKeys.filter((k) => k.endsWith("[ticker]"));
    const weights = allocationKeys.filter((k) => k.endsWith("[weight]"));

    for (let i = 0; i < tickers.length; i++) {
      const ticker = formData.get(tickers[i]);
      const weight = parseFloat(formData.get(weights[i]) || 0) / 100; // Convert to decimal
      if (ticker) {
        data.allocations.push({ ticker, weight });
      }
    }

    // Loading spinner and results box
    const spinner = document.getElementById("loading");
    const resultsBox = document.getElementById("results-box");
    spinner.classList.remove("collapse");
    resultsBox.textContent = "백테스트 결과를 불러오는 중입니다...";

    // Reset backtest results
    try {
      const res = await fetch("/api/backtest/static-allocation/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken() || "",
        },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      console.log(result);
      resultsBox.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
      resultsBox.textContent =
        "백테스트 결과를 불러오는 중 오류가 발생했습니다.";
      console.error("백테스트 요청 중 오류 발생:", error);
    } finally {
      spinner.classList.add("collapse");
    }
  });
