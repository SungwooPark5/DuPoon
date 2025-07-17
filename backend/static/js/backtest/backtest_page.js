import { getCSRFToken } from "../utils.js";

// Apply strategy to form
document.addEventListener("DOMContentLoaded", function () {
  // Listen for strategy selection event from strategy load modal
  window.addEventListener("strategySelected", (event) => {
    const strategy = event.detail;
    applyStrategyToForm(strategy);
  });

  const openSaveModal = document.getElementById("open-save-modal");
  const strategyNameInput = document.getElementById("strategyName");
  const strategyTypeInput = document.getElementById("strategyType");
  const saveStrategyModal = new bootstrap.Modal(
    document.getElementById("saveStrategyModal")
  );

  openSaveModal.addEventListener("click", () => {
    // Set strategy name and type in the save modal
    strategyNameInput.value =
      document.querySelector("input[name='strategy_name']").value || "";
    strategyTypeInput.value =
      document
        .querySelector("select[name='strategy_type']")
        .value.toUpperCase() || "STATIC";
  });

  function applyStrategyToForm(strategy) {
    document.querySelector("input[name='strategy_name']").value =
      strategy.name || "";
    document.querySelector("select[name='rebalance_frequency']").value =
      strategy.rebalance_frequency || "monthly";
    document.querySelector("select[name='include_cash']").value =
      strategy.include_cash ? "true" : "false";
    document.querySelector("input[name='cash_ticker']").value =
      strategy.cash_ticker || "CASH";
    document.querySelector("input[name='cash_weight']").value = (
      strategy.cash_weight * 100
    ).toFixed(2);

    fillAllocations(strategy.allocations || []);
  }

  function fillAllocations(allocations) {
    const allocationsDiv = document.getElementById("allocations");
    allocationsDiv.innerHTML = ""; // Clear existing allocations

    allocations.forEach((allocation, index) => {
      const newAllocation = document.createElement("div");
      newAllocation.className = "allocation row mb-2";

      newAllocation.innerHTML = `
          <div class="col-md-5">
              <input name="allocations[${index}][ticker]" placeholder="티커" class="form-control mb-1" value="${
        allocation.ticker
      }" required>
          </div>
          <div class="col-md-5">
              <input name="allocations[${index}][weight]" placeholder="비율 (%)" class="form-control mb-1" value="${(
        allocation.weight * 100
      ).toFixed(2)}" required>
          </div>
          <div class="col-md-2">
              <button type="button" class="btn btn-outline-danger remove-allocation">삭제</button>
          </div>
      `;

      allocationsDiv.appendChild(newAllocation);
    });
  }
});

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
      // strategy_name: formData.get("strategy_name") || null,
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
    const openSaveModal = document.getElementById("open-save-modal");

    spinner.classList.remove("collapse");
    resultsBox.textContent = "백테스트 결과를 불러오는 중입니다...";
    if (window.returnsChart) {
      window.returnsChart.destroy(); // Clear previous chart if exists
    }

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
      updateResultsBox(result);
      openSaveModal.classList.remove("collapse"); // 저장 모달 버튼 활성화
    } catch (error) {
      resultsBox.textContent =
        "백테스트 결과를 불러오는 중 오류가 발생했습니다.";
      console.error("백테스트 요청 중 오류 발생:", error);
    } finally {
      spinner.classList.add("collapse");
    }
  });

function updateResultsBox(result) {
  const resultsBox = document.getElementById("results-box");
  if (result && result.stats) {
    const { cagr, yearly_vol, max_drawdown, yearly_sharpe, yearly_sortino } =
      result.stats;

    resultsBox.innerHTML = `
        <table class="table table-bordered">
        <thead>
          <tr>
            <th>지표</th>
            <th>값</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>연평균 성장률 (CAGR)</td>
            <td>${(cagr * 100).toFixed(2)}%</td>
          </tr>
          <tr>
            <td>연평균 변동성</td>
            <td>${(yearly_vol * 100).toFixed(2)}%</td>
          </tr>
          <tr>
            <td>최대 낙폭</td>
            <td>${(max_drawdown * 100).toFixed(2)}%</td>
          </tr>
          <tr>
            <td>연평균 샤프 비율</td>
            <td>${yearly_sharpe.toFixed(2)}</td>
          </tr>
          <tr>
            <td>연평균 소르티노 비율</td>
            <td>${yearly_sortino.toFixed(2)}</td>
          </tr>
        </tbody>
      </table>
      `;
    if (result.price) {
      renderReturnsChart(result.price);
    }
  } else {
    resultsBox.textContent = "백테스트 결과가 없습니다.";
  }
}

function renderReturnsChart(priceData) {
  const labels = priceData.map((item) => item.date);
  const prices = priceData.map((item) => item.price);

  const ctx = document.getElementById("returns-chart").getContext("2d");

  if (window.returnsChart) {
    window.returnsChart.destroy();
  }

  window.returnsChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "자산 가격",
          data: prices,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day",
            tooltipFormat: "yyyy-MM-dd",
          },
        },
        y: {
          beginAtZero: false,
        },
      },
    },
  });
}
