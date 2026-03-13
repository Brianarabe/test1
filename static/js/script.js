let menu = document.querySelector('.header .menu');

document.querySelector('#menu-btn').onclick = () =>{
   menu.classList.toggle('active');
}

window.onscroll = () =>{
   menu.classList.remove('active');
}

document.querySelectorAll('input[type="number"]').forEach(inputNumber => {
   inputNumber.oninput = () =>{
      if(inputNumber.value.length > inputNumber.maxLength) inputNumber.value = inputNumber.value.slice(0, inputNumber.maxLength);
   };
});

document.querySelectorAll('.view-property .details .thumb .small-images img').forEach(images =>{
   images.onclick = () =>{
      src = images.getAttribute('src');
      document.querySelector('.view-property .details .thumb .big-image img').src = src;
   }
});

document.querySelectorAll('.faq .box-container .box h3').forEach(headings =>{
   headings.onclick = () =>{
      headings.parentElement.classList.toggle('active');
   }
});

// role_message.js
document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.role-message');

    messages.forEach(msg => {
        const messageText = msg.dataset.message;
        const userType = msg.dataset.userType;

        if (messageText) {
            alert(messageText);  // simple pop-up
            // Optionally, you could customize with SweetAlert or a nicer modal
            console.log(`User type: ${userType}`);
        }
    });
});

