import { getCSRFToken } from "../utils.js";

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".delete-result").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const row = event.target.closest("tr");
      const resultId = row.dataset.id;

      if (!confirm("정말 삭제하시겠습니까?")) return;

      try {
        const response = await fetch(
          `/api/backtest/backtest-stats/${resultId}/`,
          {
            method: "DELETE",
            headers: {
              "X-CSRFToken": getCSRFToken(),
            },
          }
        );

        if (response.ok) {
          row.remove(); // 테이블에서 행 삭제
          alert("결과가 삭제되었습니다.");
        } else {
          alert("삭제 실패: " + response.status);
        }
      } catch (error) {
        console.error("삭제 중 오류:", error);
        alert("삭제 요청 중 오류가 발생했습니다.");
      }
    });
  });
});
