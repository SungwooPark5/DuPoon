document.getElementById("fetchPriceBtn").addEventListener("click", function () {
  fetch("/api/stock/price/fetch/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": window.CSRF_TOKEN,
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
});
