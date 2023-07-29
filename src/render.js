const CLOSE_BTN = document.getElementById("close")
const CHAOS = document.getElementById("Chaos")



CLOSE_BTN.addEventListener("click", () => {
    api.close();
});
setInterval(updateTotal,500)
console.log('hi')
async function updateTotal() {
    fetch("total.txt")
  .then((res) => res.text())
  .then((text) => {
    CHAOS.innerText = text;
   })
  .catch((e) => console.error(e));

}