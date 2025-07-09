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
