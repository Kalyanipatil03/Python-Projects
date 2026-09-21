document.addEventListener("DOMContentLoaded", () => {
  // Handle async article likes without reloading the page
  const likeButtons = document.querySelectorAll(".like-btn");

  likeButtons.forEach((button) => {
    button.addEventListener("click", async (e) => {
      e.preventDefault();
      const articleId = button.getAttribute("data-article-id");
      if (!articleId) return;

      try {
        const response = await fetch(`/post/${articleId}/like`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          const countSpan = button.querySelector(".like-count");
          const icon = button.querySelector("i");

          if (countSpan) countSpan.textContent = data.likes_count;

          if (data.liked) {
            button.classList.add("text-rose-500");
            if (icon) {
              icon.classList.remove("fa-regular");
              icon.classList.add("fa-solid");
            }
          } else {
            button.classList.remove("text-rose-500");
            if (icon) {
              icon.classList.remove("fa-solid");
              icon.classList.add("fa-regular");
            }
          }
        } else if (response.status === 401) {
          window.location.href = "/auth/login";
        }
      } catch (err) {
        console.error("Error toggling like:", err);
      }
    });
  });

  // Auto-hide alert messages after 4 seconds
  const flashMessages = document.querySelectorAll("[data-flash-message]");
  flashMessages.forEach((msg) => {
    setTimeout(() => {
      msg.style.transition = "opacity 0.5s ease";
      msg.style.opacity = "0";
      setTimeout(() => msg.remove(), 500);
    }, 4000);
  });
});