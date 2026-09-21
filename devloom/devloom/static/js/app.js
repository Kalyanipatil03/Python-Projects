document.addEventListener("DOMContentLoaded", () => {
    // Interactive Like Button Handler
    const likeBtn = document.getElementById("like-btn");
    if (likeBtn) {
        likeBtn.addEventListener("click", async () => {
            const postId = likeBtn.dataset.postId;
            try {
                const response = await fetch(`/post/${postId}/like`, { method: "POST" });
                const data = await response.json();
                const countSpan = document.getElementById("like-count");
                if (countSpan) countSpan.textContent = data.likes_count;
                
                if (data.liked) {
                    likeBtn.classList.add("text-emerald-400");
                    likeBtn.classList.remove("text-zinc-400");
                } else {
                    likeBtn.classList.remove("text-emerald-400");
                    likeBtn.classList.add("text-zinc-400");
                }
            } catch (err) {
                console.error("Error liking post:", err);
            }
        });
    }

    // Interactive Bookmark Button Handler
    const bookmarkBtn = document.getElementById("bookmark-btn");
    if (bookmarkBtn) {
        bookmarkBtn.addEventListener("click", async () => {
            const postId = bookmarkBtn.dataset.postId;
            try {
                const response = await fetch(`/post/${postId}/bookmark`, { method: "POST" });
                const data = await response.json();
                
                if (data.saved) {
                    bookmarkBtn.classList.add("text-amber-400");
                    bookmarkBtn.classList.remove("text-zinc-400");
                } else {
                    bookmarkBtn.classList.remove("text-amber-400");
                    bookmarkBtn.classList.add("text-zinc-400");
                }
            } catch (err) {
                console.error("Error bookmarking post:", err);
            }
        });
    }
});