import { getCSRFToken } from "../utils.js";
import { latestBacktestResult } from "./backtest_page.js";

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

    const payload = {
      name: name,
      description: description,
      start_date: latestBacktestResult.start_date,
      end_date: latestBacktestResult.end_date,
      max_drawdown: parseFloat(latestBacktestResult.max_drawdown || 0),
      volatility: parseFloat(latestBacktestResult.volatility || 0),
      sharpe_ratio: parseFloat(latestBacktestResult.sharpe_ratio || 0),
      sortino_ratio: parseFloat(latestBacktestResult.sortino_ratio || 0),
      strategy_id: latestBacktestResult.strategy_id || null,
    };
  });
});
