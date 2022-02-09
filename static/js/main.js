function RemoveDiv() {
  let verif = `
  <div class="flex justify-center items-center mt-6 w-full">
    <div class="lds-dual-ring"></div>
  </div>
  `
  let element = document.getElementById("remove");

  if (element.innerHTML != '') {
    if (document.getElementById("remove").innerHTML != verif) {
      document.getElementById("input-data").value = ''
    }

    element.innerHTML = ''

  }
}

function EditPage(rep) {
  RemoveDiv()

  if (rep['sentiment'] == "Negative") {
    let element = document.getElementById("remove");
    element.innerHTML = `
    <div class="flex justify-center items-center mt-6 w-full">
      <div class="relative w-2/5" id="remove">
        <div class="bg-white h-auto w-full pl-5 rounded-lg pt-2 pb-2" style="color: #303030">
            <h4 class="font-bold">Ce texte dégage un sentiment négatif.</h4>
            <p class="font-normal">Attention, cela ne veut pas dire que le text contient une fake news, seulement de nombreuse fake news utilisent nos sentiment pour nous faire changer d'avis, soyez vigilent !</p>
        </div>
      </div>
    </div>
    `
  }


  if (Object.keys(rep['warning_link']).length != 0) {
    Object.entries(rep['warning_link']).forEach(([key, value]) => {

      let element = document.getElementById("remove");
      element.innerHTML += `
      <div class="flex justify-center items-center mt-6 w-full">
        <div class="relative w-2/5">
          <div class="bg-white h-auto w-full pl-5 rounded-lg pt-2 pb-2" style="color: #303030">
              <h4 class="font-bold">Un lien a été détecté, voici la source de celui ci.</h4>
              <p class="font-normal">${key} : ${value}</p>
          </div>
        </div>
      </div>
      `
    });
  }

  if (Object.keys(rep['news']).length != 0) {
    Object.entries(rep['news']).forEach(([key, value]) => {

      let element = document.getElementById("remove");
      element.innerHTML += `
      <div class="flex justify-center items-center mt-6 w-full">
        <div class="relative w-2/5">
          <div class="bg-white h-auto w-full pl-5 rounded-lg pt-2 pb-2" style="color: #303030">
              <h4 class="font-bold">Voici des informations en lien avec ce sujet.</h4>
              <p class="font-normal">${value[0]}<br /><br />${value[3]}<br /><br /><a href="${value[2]}">Lire l'article.</a></p>
          </div>
        </div>
      </div>
      `

    });
  } else {
    let element = document.getElementById("remove");
    element.innerHTML += `
    <div class="flex justify-center items-center mt-6 w-full">
      <div class="relative w-2/5">
        <div class="bg-white h-auto w-full pl-5 rounded-lg pt-2 pb-2" style="color: #303030">
            <h4 class="font-bold">Aucun sujet n'a été trouvé en lien avec cette phrase.</h4>
        </div>
      </div>
    </div>
    `
  }

}

function PostData() {
  let element = document.getElementById("input-data");
  let data = element.value

  if (document.getElementById("remove").innerHTML != '') {
    element.value = ""
  }


  element = document.getElementById("remove");
  element.innerHTML = `
  <div class="flex justify-center items-center mt-6 w-full">
    <div class="lds-dual-ring"></div>
  </div>
  `
  fetch("/detect", {
    method: 'post',
    body: JSON.stringify({'text': data}),
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
  .then(response => response.json())
  .then(json => EditPage(json))
}
