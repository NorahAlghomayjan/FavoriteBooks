
const form = document.querySelectorAll('.register_form')
const first = document.querySelector('.name_reg')
form.addEventListener('submit',(e)=> {
    e.preventDefault();
    checkInputs();
});

function checkInputs()
{
    var first_name = first.value.trim()
    if (first_name.length < 2)
    {error(first,'first name should be 2 char at least')}
    
}

function error(input,msg)
{
    div = input.parentElement;
    small = div.querySelector('small');
    small.innerText = msg
    small.color = 'red'
    input.className = 'error'
}

function success(msg)
{}