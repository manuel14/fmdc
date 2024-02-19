const audioElements = document.querySelectorAll('audio');
const playAllButton = document.querySelector(".playAll");

let currentlyPlaying = null;

// Function to stop the currently playing audio
function stopCurrentlyPlaying() {
    if (currentlyPlaying) {
        currentlyPlaying.pause();
        currentlyPlaying.currentTime = 0;
    }
}

// Add click event listener to each audio element
audioElements.forEach(audio => {
    audio.addEventListener('play', () => {
        if (audio !== currentlyPlaying) {
            console.log("distinto")
            
            if (currentlyPlaying) {
                currentlyPlaying.pause()
                currentlyPlaying.currentTime = 0;
            }
            audio.play();
            currentlyPlaying = audio;
            
        } else {
            currentlyPlaying = null
        }
    });
    
});


function player(albumId) {
    console.log(albumId)
    var supportsAudio = true; // Assuming this is defined elsewhere
    if (supportsAudio) {
        var index = 0,
            playing = false,
            tracks = document.querySelectorAll('#' + albumId + ' > audio'),
            trackCount = tracks.length;

        tracks.forEach(function(track, index) {
            track.removeEventListener('play', onPlay);
            track.removeEventListener('pause', onPause);
            track.removeEventListener('ended', onEnded);

            track.addEventListener('play', onPlay);
            track.addEventListener('pause', onPause);
            track.addEventListener('ended', onEnded);
        });

        function onPlay() {
            playing = true;
        }

        function onPause() {
            playing = false;
        }

        function onEnded() {
            if ((index + 1) < trackCount) {
                index++;
                var audio = getAudio(index, tracks);
                audio.play();
            } else {
                playing = false;
                index = 0;
            }
        }

        var audio = getAudio(index, tracks);
        audio.play();
    }
}

function getAudio(index, tracks) {
    return tracks[index];
}

const playAll = document.querySelector('.playAll')
playAll.addEventListener("click", (e) => {
    e.preventDefault();
    const albumId = playAll.dataset.albumid;
    player(albumId)
})