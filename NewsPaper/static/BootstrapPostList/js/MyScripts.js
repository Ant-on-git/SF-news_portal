
// добавляем класс в форму поиска (элемент категория) чтобы было в одну строчку
let filter_category = document.getElementById('id_category');
if (filter_category) {
    filter_category.classList.add('d-sm-flex');
    filter_category.classList.add('justify-content-sm-start');
    for (let div of filter_category.children) {
        div.classList.add('px-sm-2')
    }
}

// добавляем классы в форму добавления/изменения поста (элемент тип), чтобы radio было в одну строчку (display:inline-block)
let addPost_type = document.getElementById('id_type');
if (addPost_type) {
    addPost_type.classList.add('d-sm-inline-block')
    for (let div of addPost_type.children) {
        div.classList.add('d-sm-inline-block')
        div.classList.add('px-sm-2')
    }
}


