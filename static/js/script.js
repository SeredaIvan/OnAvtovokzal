/////               Form buy ticket



    document.addEventListener('DOMContentLoaded', function () {
        document.querySelector('input[name="phone"]').addEventListener('input', function () {
            phoneValid()
        });
    });

    function phoneValid(event=""){
        let phone=document.querySelector('input[name="phone"]')
        let phoneNumber = phone.value

        if (phoneNumber.length === 10) {
            phone.style.border = "2px solid green";
            redirectToSelect()
        }
        else {
            phone.style.border = "2px solid red";
            setValidationMessage("Введіть коректний номер");
            event.preventDefault()
        }
        console.log(phoneNumber)
    }

    function setValidationMessage(message) {
        let labphone = document.getElementById('labphone');
        labphone.innerHTML = message;
    }


    document.addEventListener('DOMContentLoaded', function () {
        document.querySelector('input[name="finishtime"]').addEventListener('change', function () {
            let timestart = document.querySelector('input[name="starttime"]')
            let timefinish = document.querySelector('input[name="finishtime"]')

            if ( timefinish.value > timestart.value) {
                timefinish.style.border = "solid 2px green"
            }
            else {
                timefinish.style.border = "solid 2px red";
            }
        })
    })

    async function redirectToSelect() {
        const citystart = document.querySelector('select[name="citystart"]').value;
        const cityfinish = document.querySelector('select[name="cityfinish"]').value;
        const starttime = document.querySelector('select[name="starttime"]').value;
        const finishtime = document.querySelector('select[name="finishtime"]').value;
        const name = document.querySelector('select[name="name"]').value;
        const phone = document.querySelector('select[name="phone"]').value;

        const formData = new FormData();
        formData.append('item_sort', name);
        formData.append('direction', phone);
        formData.append('citystart', citystart);
        formData.append('cityfinish', cityfinish);
        formData.append('starttime', starttime);
        formData.append('finishtime', finishtime);;

        try {
            const response = await fetch('/formbuyticket', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Перезавантаження сторінки після успішної відправки POST-запиту
                window.location.href='/journeys';
                window.location.reload();
            } else {
                // Обробка помилок
                console.error('Помилка при відправці POST-запиту');
            }
        } catch (error) {
            console.error('Помилка при виконанні fetch:', error);
        }
    }





    /////