  function increaseValue() {
    let value = parseInt(document.getElementById('number').value, 10);
    value = isNaN(value) ? 1 : value;
    if (value < 99) {
      value++;
    }
    document.getElementById('number').value = value;
  }

  function decreaseValue() {
    let value = parseInt(document.getElementById('number').value, 10);
    value = isNaN(value) ? 1 : value;
    value < 1 ? value = 1 : '';
    if (value > 1) {
      value--;
    }
    document.getElementById('number').value = value;
  }

