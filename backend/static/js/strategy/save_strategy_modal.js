import { getCSRFToken } from "../utils.js";

document.addEventListener("DOMContentLoaded", function () {
  const strategyForm = document.getElementById("strategyForm");
  const strategyModal = bootstrap.Modal.getOrCreateInstance(
    document.getElementById("saveStrategyModal")
  );

  strategyForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    // Save strategy logic here
    const name = document.getElementById("strategyName").value.trim();
    const description = document
      .getElementById("strategyDescription")
      .value.trim();
    const type = document.getElementById("strategyType").value.toUpperCase();

    // Get backtest data from backtest-form
    const backtestForm = document.getElementById("backtest-form");
    const formBacktestFormData = new FormData(backtestForm);

    if (!name) {
      alert("전략 이름을 입력해주세요.");
      return;
    }

    const payload = {
      name: name,
      description: description,
      type: type,
      allocations: getAllocationsFromBacktestForm(),
      rebalance_frequency: formBacktestFormData.get("rebalance_frequency"),
      include_cash: formBacktestFormData.get("include_cash") || false,
      cash_ticker: formBacktestFormData.get("cash_ticker") || null,
      cash_weight: parseFloat(formBacktestFormData.get("cash_weight") || 0),
    };

    const strategyID = formBacktestFormData.get("strategy_id") || null;
    console.log(strategyID);
    // save strategy via API
    if (strategyID) {
      update_strategy(strategyID, payload);
    } else {
      create_strategy(payload);
    }
  });

  // Function to update an existing strategy
  async function update_strategy(id, payload) {
    try {
      const response = await fetch(`/api/strategy/strategies/${id}/`, {
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
      console.log("Strategy updated successfully:", data);
      strategyModal.hide(); // Hide the modal after updating
      alert("전략이 업데이트되었습니다.");
    } catch (error) {
      console.error("Error updating strategy:", error);
    }
  }
  // Function to create a new strategy
  async function create_strategy(payload) {
    try {
      const response = await fetch("/api/strategy/strategies/", {
        method: "POST",
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
      console.log("Strategy created successfully:", data);
      strategyModal.hide(); // Hide the modal after creating
      alert("전략이 생성되었습니다.");

      strategyForm.reset();
      console.log("New strategy ID:", data.id);

      if (window.openResultModalAfterSave) {
        window.openResultModalAfterSave = false;
        const saveResultModal = new bootstrap.Modal(
          document.getElementById("saveResultModal")
        );
        saveResultModal.show();
      }

      return data.id; // Return the new strategy ID
    } catch (error) {
      console.error("Error creating strategy:", error);
    }
  }
  function getAllocationsFromBacktestForm() {
    const allocations = [];
    const allocationElements = document.querySelectorAll(".allocation");
    allocationElements.forEach((allocation) => {
      const ticker = allocation
        .querySelector("input[name^='allocations'][name$='[ticker]']")
        .value.trim();
      const weight =
        parseFloat(
          allocation
            .querySelector("input[name^='allocations'][name$='[weight]']")
            .value.trim()
        ) / 100; // Convert to decimal
      if (ticker && !isNaN(weight)) {
        allocations.push({ ticker, weight });
      }
    });
    return allocations;
  }
});
