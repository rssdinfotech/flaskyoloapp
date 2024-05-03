document.addEventListener("DOMContentLoaded", function () {
  // Open Modal 1
  document.getElementById("openModal1").addEventListener("click", function () {
    document.getElementById("myModal1").style.display = "block";
  });

  // Close Modal 1
  document.getElementById("closeModal1").addEventListener("click", function () {
    document.getElementById("myModal1").style.display = "none";
  });

  // Open Modal 2
  document.getElementById("openModal2").addEventListener("click", function () {
    document.getElementById("myModal2").style.display = "block";
  });

  // Close Modal 2
  document.getElementById("closeModal2").addEventListener("click", function () {
    document.getElementById("myModal2").style.display = "none";
  });

  // Close any modal
  const closeModalBtns = document.querySelectorAll(".closeModalBtn");
  closeModalBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const modal = this.closest(".modal");
      modal.style.display = "none";
    });
  });
});

//

document.addEventListener("DOMContentLoaded", function () {
  const openModalBtn = document.getElementById("openModal");
  const closeModalBtn = document.getElementById("closeModal");
  const modal = document.getElementById("modal");
  const triggerPopupBtn = document.getElementById("triggerPopup");
  const popupContent = document.getElementById("popupContent");
  const closeModalBtn2 = document.getElementById("closeModalBtn");

  openModalBtn.addEventListener("click", function () {
    modal.classList.add("show");
  });

  closeModalBtn.addEventListener("click", function () {
    modal.classList.remove("show");
  });

  triggerPopupBtn.addEventListener("click", function () {
    popupContent.classList.toggle("show");
  });

  closeModalBtn2.addEventListener("click", function () {
    modal.classList.remove("show");
  });
});
