import { getCSRFToken } from "../utils.js";
import { parseDate } from "../utils.js";
import { getLatestBacktestResult } from "./backtest_page.js";

document.addEventListener("DOMContentLoaded", function () {
  const resultForm = document.getElementById("resultForm");
  const resultModal = bootstrap.Modal.getOrCreateInstance(
    document.getElementById("saveResultModal")
  );

  resultForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    // Save strategy logic here
    const name = document.getElementById("resultName").value.trim();
    const description = document
      .getElementById("resultDescription")
      .value.trim();

    // Get backtest data from backtest-form
    const backtestForm = document.getElementById("backtest-form");
    const formBacktestFormData = new FormData(backtestForm);

    const strategyId = formBacktestFormData.get("strategy_id") || null;

    if (!strategyId) {
      alert("전략을 먼저 저장해주세요.");
      return;
    }

    if (!name) {
      alert("결과 이름을 입력해주세요.");
      return;
    }

    const latestBacktestStats = getLatestBacktestResult().stats;
    if (!latestBacktestStats) {
      alert("백테스트 결과가 없습니다. 백테스트를 먼저 실행해주세요.");
      return;
    }

    console.log(latestBacktestStats);

    const payload = {
      name: name,
      description: description,
      start_date: parseDate(latestBacktestStats.start), // format: YYYY-MM-DD
      end_date: parseDate(latestBacktestStats.end), // format: YYYY-MM-DD
      cagr: parseFloat(latestBacktestStats.cagr || 0),
      total_return: parseFloat(latestBacktestStats.total_return || 0),
      max_drawdown: parseFloat(latestBacktestStats.max_drawdown || 0),
      volatility: parseFloat(latestBacktestStats.yearly_vol || 0),
      sharpe_ratio: parseFloat(latestBacktestStats.yearly_sharpe || 0),
      sortino_ratio: parseFloat(latestBacktestStats.yearly_sortino || 0),
      strategy: strategyId,
    };

    // save result via API
    try {
      const response = await fetch("/api/backtest/backtest-stats/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken() || "",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to save result");
      }

      const resultData = await response.json();
      console.log("Result saved successfully:", resultData);
      alert("결과가 성공적으로 저장되었습니다.");
      resultModal.hide();
    } catch (error) {
      console.error("Error saving result:", error);
      alert("결과 저장에 실패했습니다. 다시 시도해주세요.");
    }
  });
});
