function openNotice(type) {
  const overlay = document.getElementById("noticeOverlay");
  const img = document.getElementById("noticeImg");

  if (type === "ticket") {
    img.src = "/static/img/notice_ticket.jpg";
  } else if (type === "entry") {
    img.src = "/static/img/notice_entry.jpg";
  }

  overlay.classList.add("show");
}

function closeNotice(e) {
  // 只有點到黑色背景才會關
  if (e.target.id === "noticeOverlay") {
    e.target.classList.remove("show");
  }
}
