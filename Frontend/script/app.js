const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const clearClassList = function (el) {
  el.classList.remove("c-note--played");
  el.classList.remove("u-1-of-8")
  el.classList.remove("u-2-of-9")
  el.classList.remove("u-1-of-9")

};
let notes;
let knop;
let current_track;
let key;
let btt;
let time;
let savebtn;
var shown = true;
var timing = 0;
let timer
let timerunning = false


const listenToUI = function () {
  const sound = document.querySelector(".js-sound");
  const slidercont = document.querySelector(".js-slidercont");
  const slider = document.querySelector(".js-slider");
  const volume = document.querySelector(".js-volume");
  const start = document.querySelector(".js-start");
  const startcont = document.querySelector(".js-start--content");
  const stop = document.querySelector(".js-stop");
  const save = document.querySelector(".js-save");
  if(sound){
      sound.addEventListener("click", function() {
      if(shown){
        volume.classList.add("o-layout--row-reverse")
        slidercont.classList.remove("u-hidden")
        shown = false
      }
      else{
        volume.classList.remove("o-layout--row-reverse")
        slidercont.classList.add("u-hidden")
        shown = true
      }
    })
    slider.addEventListener("input", function(){
      let output = slider.value
      console.log(output)
      socket.emit("F2B_volume_changed", {'volume': output})
    })
    start.addEventListener("click", function(){
      if (startcont.getAttribute("stroke") == "white"){
        startcont.setAttribute("stroke", "#F91F57");
        timerunning = true;
        socket.emit("F2B_start");
      }
      else{
        startcont.setAttribute("stroke", "white");
        timerunning = false;
        socket.emit("F2B_pause");
      }
    })
    stop.addEventListener("click", function(){
      timer.innerHTML = '00:00:00';
      startcont.setAttribute("stroke", "white");
      timerunning = false;
      timing = 0;
      socket.emit("F2B_stop")
    })
    save.addEventListener("click", function(){
      socket.emit("F2B_duration", {duration: timer.innerHTML});
    })
  }
  const knop = document.querySelector(".js-button");
  if(knop){
    knop.addEventListener("click", function(){
      console.log("testclick")
      socket.emit("F2B_play_test")
    })
  }
  const playbuttons = document.querySelectorAll(".js-play");
  const deletebuttons =document.querySelectorAll(".js-delete");
  if(playbuttons){
    for(let playbutton of playbuttons){
    playbutton.addEventListener("click", function(){
      console.log("play")
      console.log(playbutton.dataset.track)
      socket.emit("F2B_play_track", {'track': playbutton.dataset.track});
    })
  }
    for(let deletebutton of deletebuttons){
      deletebutton.addEventListener("click", function(){
        console.log("delete")
        console.log(deletebutton.dataset.track)
        handleData(`http://${lanIP}/api/v1/tracks/remove/${deletebutton.dataset.track}`, callbackRemoveTrack, null, "DELETE");
      })
    }
  
  }
  if(savebtn){
    savebtn.addEventListener("click", function(){
      let name = document.querySelector(".js-name")
      socket.emit("F2B_save", {'trackName': name.value});
    })
    
  }
};

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    console.log(knop)
    const savetitle = document.querySelector(".js-savetitle")
    if(savetitle){
      gettracks();
      socket.emit('F2B_saved')
    };
    console.log(notes)
    if(notes.length != 0 && notes){
      socket.emit('F2B_play')
    }
    if(savebtn){
      socket.emit('F2B_saving')
    }

  });

  socket.on("B2F_noten_in_scale1", function(jsonObject){
    if(notes.length != 0 && notes){
      console.log(jsonObject)
    
      let i = 0
      for(let note of notes){
        i++
        note.innerHTML = jsonObject[i]
      }
      listenToUI();
    }
  })

  socket.on("B2F_noten_in_scale", function(jsonObject){
    if(notes.length != 0 && notes){
      console.log(jsonObject)
      
      let i = 0
      for(let note of notes){
        i++
        note.innerHTML = jsonObject[i]
      }
    }
  })

  socket.on("B2F_current_track", function(jsonObject){
    if(current_track){
      current_track.innerHTML = jsonObject['current']
    }
  })

  socket.on("B2F_note_on", function(jsonObject){
    if(notes.length != 0 && notes){
      console.log(jsonObject)
      for(let note of notes){
        clearClassList(note)
        if(note.innerHTML == jsonObject["Noot"]){
          note.classList.add("c-note--played")
          note.classList.add("u-2-of-9")
        }
        else{
          note.classList.add("u-1-of-9")
        }
      }
    }
  })

  socket.on("B2F_note_off", function(){
    
    if(notes.length != 0 && notes){
      for(let note of notes){
        clearClassList(note)
        note.classList.add("u-1-of-8")
        
      }
    }
  })
  socket.on("B2F_track_info", function(jsonObject){
    console.log(jsonObject)
    key = document.querySelector(".js-key")
    btt = document.querySelector(".js-tempo")
    time = document.querySelector(".js-time")
    console.log(key)
    if(key){
      key.innerHTML = jsonObject.key
      btt.innerHTML = jsonObject.btt
      time.innerHTML = jsonObject.time
    }
    listenToUI();
  })
};
const gettracks = function(){
  handleData(`http://${lanIP}/api/v1/tracks`, showtracks, null, "GET");
};
const showtracks = function(data){
  const tracks = document.querySelector(".js-tracks");
  console.log(data)
  let html = ''
  html = 
  `<div class="o-layout o-layout--align-center u-mb-sm">
  <div class="o-layout__item u-1-of-9">
    <div class="o-icon js-button">
        <svg class="o-icon__symbol" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-labelledby="playIconTitle" stroke="white" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" fill="none" color="white"> <title id="playIconTitle">Play</title> <path d="M20 12L5 21V3z"/> </svg>
    </div>
  </div>
  <div class="o-layout__item u-1-of-9">
      1
  </div>
  <div class="o-layout__item u-4-of-9">
      Game of Thrones
  </div>
  <div class="o-layout__item u-2-of-9">
      0:00:31
  </div>
  <div class="o-layout__item u-1-of-9" >
    <div class="o-icon ">
        <svg class="o-icon__symbol" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-labelledby="binIconTitle" stroke="white" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" fill="none" color="white"> <title id="binIconTitle">Bin</title> <path d="M19 6L5 6M14 5L10 5M6 10L6 20C6 20.6666667 6.33333333 21 7 21 7.66666667 21 11 21 17 21 17.6666667 21 18 20.6666667 18 20 18 19.3333333 18 16 18 10"/> </svg>
    </div>
  </div>
</div>`
  for(let track of data){
    console.log(track)

    html += `        
    <div class="o-layout o-layout--align-center u-mb-sm">
    <div class="o-layout__item u-1-of-9">
      <div class="o-icon js-play" data-track=${track.idPlaySession}>
          <svg class="o-icon__symbol" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-labelledby="playIconTitle" stroke="white" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" fill="none" color="white"> <title id="playIconTitle">Play</title> <path d="M20 12L5 21V3z"/> </svg>
      </div>
    </div>
    <div class="o-layout__item u-1-of-9">
        ${track.idPlaySession}
    </div>
    <div class="o-layout__item u-4-of-9">
        ${track.trackName}
    </div>
    <div class="o-layout__item u-2-of-9">
        ${track.duratiion}
    </div>
    <div class="o-layout__item u-1-of-9" >
      <div class="o-icon js-delete " data-track=${track.idPlaySession}>
          <svg class="o-icon__symbol" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-labelledby="binIconTitle" stroke="white" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" fill="none" color="white"> <title id="binIconTitle">Bin</title> <path d="M19 6L5 6M14 5L10 5M6 10L6 20C6 20.6666667 6.33333333 21 7 21 7.66666667 21 11 21 17 21 17.6666667 21 18 20.6666667 18 20 18 19.3333333 18 16 18 10"/> </svg>
      </div>
    </div>
  </div>
</div>`
      
  }
  tracks.innerHTML = html
  listenToUI();
};
const callbackRemoveTrack = function(data){
  console.log(data);
  gettracks();
}

function myCallback() {
  socket.emit("F2BCheck")
  if(timer){
    if(timerunning){
      timing++;

    
      minutes = Math.floor(timing/60);
      seconds = timing % 60
      if(minutes>9){
        if(seconds>9){
          timer.innerHTML = `00:${minutes}:${seconds}`
        }
        else{
          timer.innerHTML = `00:${minutes}:0${seconds}`
        }
      }
      else{
        if(seconds>9){
          timer.innerHTML = `00:0${minutes}:${seconds}`
        }
        else{
          timer.innerHTML = `00:0${minutes}:0${seconds}`
        }
      }
    }
    
  }
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  notes = document.querySelectorAll(".js-note");
  knop = document.querySelector(".js-button");
  current_track = document.querySelector(".js-ctrack")
  savebtn = document.querySelector(".js-savebtn")
  
  listenToSocket();

  
  timer = document.querySelector(".js-timer")
  var intervalID = window.setInterval(myCallback, 1000);
});
