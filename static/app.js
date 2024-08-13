

var iconA = L.Icon.extend({
    options: {
        iconSize:     [30, 30],
        popupAnchor:  [0, -20]
    }
});


var mapOptions = {
        center: [6.880817761383014, -5.229036370820243],
        zoom: 20
    }
    var layer = new L.TileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});
    var map = new L.map('mapid', mapOptions);
    map.addLayer(layer);
    var markerOptions = {
        title: "AlertINP",
        clickable: true,
}

// fetch("static/js/limite_inphb.geojson")
// .then(function(response) {
//     return response.json();
// })
// .then(function(data) {
//     L.geoJSON(data).addTo(map);
// });

var icon_utilisateur=new iconA({iconUrl:"/static/icon/utilisateur2.png"})
window.onload = function() {
        add_alert(listAlert)
        // vider_form()
}
// map.locate({setView: true, watch: true}) /* This will return map so you can do chaining */
// map.on('locationfound', function(e){
//             var marker = L.marker([e.latitude, e.longitude], {icon: icon_utilisateur}).bindPopup('Vous êtes ici');
//             var circle = L.circle([e.latitude, e.longitude], e.accuracy/2, {
//                 weight: 1,
//                 color: 'blue',
//                 fillColor: '#cacaca',
//                 fillOpacity: 0.2
//             });
//             map.addLayer(marker);
//             map.addLayer(circle);
//             add_alert(listAlert)
//             vider_form()
            
//         })
//        .on('locationerror', function(e){
//             console.log(e);
//             alert("Accès à votre localisation réfusé.");
// });


// setInterval(function() {  
//     let requet = new XMLHttpRequest();
//     requet.open('GET', "map.html");
//     add_alert(listAlert);
//     requet.send();
//     return true;  
// }, 5000);

// async function updateAlerts() {
//   let promesse = new Promise(function(resolution) {
//     setTimeout(function() {
//     let requet = new XMLHttpRequest();
//     requet.open('GET', "map.html");
//     requet.onload = function() {
//       if (requet.status == 200) {
//         // console.log(requet.response);
//         add_alert(listAlert)
//         resolution(requet.response);
//       } else {
//         resolution("Erreur");
//       }
//     };
//     requet.send();},5000);
//   });
//     listAlert = await promesse;
    
// }

// updateAlerts();

function add_alert(listAlert){
  console.log("ok")
  var datas=listAlert
  // var datas=Array.from(listAlert)
  console.log(datas)
  // console.log(datas)
  console.log(Object.keys(datas).length)
  for (i = 1; i < Object.keys(datas).length+1; i++){
            console.log(i)
            var titre =datas[i]['titre']
            var auteur =datas[i]['auteurId']
            var typeAlert =datas[i]["typeAlert"]
            var icon_alerte=select_icon(typeAlert)
            var message =datas[i]["message"]
            var file_data = datas[i]["picture"]
            var coord_x= datas[i]["x"]
            var coord_y= datas[i]["y"]
            var tmpl=renderAlertTpl2(auteur,titre,file_data,typeAlert,message)
            console.log("ok")
            var mp = new L.Marker([coord_y, coord_x], {icon: icon_alerte}).bindPopup(tmpl).addTo(map);
            vider_form()
            // setTimeout (1000)
            // return false
  }
}

function select_icon (typealerte) {
    // body... 
    var AlertType=typealerte
    link="/static/icon/"+AlertType+".png"
    var iconAlert=new iconA({iconUrl:link})
    return iconAlert
}

var contents=""
async function onSubmit() {
  const file = document.getElementById('id_picture').files[0];
  contents = await select_img_data(file);
            // var tmpl=renderAlertTpl2(auteur,titre,file_data,typeAlerte,message)

}

function vider_form(){
            document.getElementById("id_alerte_titre").value="";
            document.getElementById("id_type_alerte").value="";
            document.getElementById("id_alerte_message").value="";
            document.getElementById("id_x").value="";
            document.getElementById("id_y").value="";
}

map.on("dblclick", function(e){
        document.getElementById("id_alerte_titre").value=""
        document.getElementById("id_alerte_message").value=""
        w3.show('#form')
        var y=e.latlng.lat
        var x=e.latlng.lng
        document.getElementById("id_x").value = x;
        document.getElementById("id_y").value = y;     
 });

// var alertForm=document.forms["alertForm"];
// alertForm.onSubmit()= function(event){
//     event.preventDefault();
//             var titre =document.getElementById("id_alerte_titre").value
//             var auteur =emailAuteur
//             var typeAlerte =document.getElementById("id_type_alerte").value
//             var message =document.getElementById("id_alerte_message").value
//             var file_data = contents
//             var coord_x= document.getElementById("id_x").value
//             var coord_y= document.getElementById("id_y").value
//             var tmpl=renderAlertTpl2(auteur,titre,file_data,typeAlerte,message)
//             var mp = new L.Marker([coord_y, coord_x]).bindPopup(tmpl).addTo(map);
//             w3.hide('#form')
// }


function select_img_data(input) {
        let file = input.files[0]; 
        let fileReader = new FileReader(); 
        fileReader.readAsDataURL(file); 
        fileReader.onload = function() {
        contents=fileReader.result;
          var image_zone=document.getElementById("id_picture_title");
          show_img(image_zone,contents);
          // console.log(contents)
        }; 
        fileReader.onerror = function() {
          console.log(fileReader.error);
      }; 
}

function show_img(img_place, dataURL){
              img_place.innerHTML = "";
              var img = new Image();
              img.src = dataURL;
              img_place.appendChild(img);
}

// function renderAlertTpl(auteur,titre,file_data,typeAlerte,message){
//             var template=document.getElementById('alert-template').content.cloneNode(true)
//             template.getElementById("pop-autor").innerHTML=auteur
//             image_zone=template.getElementById("pop-image")
//             show_img(image_zone, file_data)
//             template.getElementById("pop-titre").innerHTML=titre
//             template.getElementById("pop-type").innerHTML=typeAlerte
//             template.getElementById("pop-message").innerHTML=message

//             return template

// }
function renderAlertTpl2(auteur,titre,file_data,typeAlerte,message){
            var templateModel=`
              <b><h3 id="pop-autor" style="color:green" class=" padding-left">${auteur}</h3></b>
              <center><div id="pop-image" class="rond-xlarge padding-bottom" style="width: 80px;height: 80px;"><img src="${file_data}" alt="" style="width: 80px;height: 80px;"></div></center>
              <h5 id="pop-titre" class="padding-left padding-bottom">${titre}</h5>
              <h5 id="pop-type" class="padding-left padding-bottom">${typeAlerte}</h5>
              <h5 id="pop-message" class="padding-left padding-bottom">${message}</h5>
            `
            return templateModel
}