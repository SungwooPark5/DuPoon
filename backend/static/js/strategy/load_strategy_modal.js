document.addEventListener("DOMContentLoaded", function () {
  const strategyList = document.getElementById("strategyList");

  async function fetchStrategies() {
    try {
      const response = await fetch("/api/strategy/strategies/");
      if (response.ok) {
        const data = await response.json();
        let strategies = data.results ? data.results : data;

        renderStrategyList(strategies);
      } else {
        console.error("Failed to fetch strategies:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching strategies:", error);
    }
  }

  function renderStrategyList(strategies) {
    strategyList.innerHTML = "";
    strategies.forEach((strategy) => {
      const listItem = document.createElement("li");
      listItem.className = "list-group-item";
      listItem.textContent = strategy.name;
      listItem.dataset.strategyId = strategy.id;
      listItem.addEventListener("click", () => {
        // applyStrategyToForm(strategy);
      });
      strategyList.appendChild(listItem);
    });
  }

  fetchStrategies();
});
