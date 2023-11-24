function fetch_coordinates() {
  fetch('http://localhost:8080/get_coordinates')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(coords => {
    process_coordinates(coords, calculator)
  })
  .catch(error => {
    console.error('There was a problem fetching the file:', error);
  });
}


function process_coordinates(coords){
  if (first_read){
    calculator.setExpression({id:'beacon0', latex:'B_{0}=(0, 0)'});
    calculator.setExpression({id:'beacon1', latex:'B_{1}=(' + coords.beacon1.x + ',0)'});
    calculator.setExpression({id:'beacon2', latex:'B_{2}=(' + coords.beacon2.x + ',' + coords.beacon2.y + ')'});
    first_read = false
  }
  calculator.setExpression({id:'tracker', latex:'T=(' + coords.tracker.x + ',' + coords.tracker.y + ')'});
}

first_read = true
let elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);
setInterval(fetch_coordinates, 2000);

