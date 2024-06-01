let currentTrackElement = null;
let isPlaying = false;
let queue = [];
let currentIndex = -1;

function playTrack(button, url) {
    const audioPlayer = document.getElementById('audio-player');
    const bottomPlayer = document.getElementById('bottom-player');
    const bottomPlayerImage = document.getElementById('bottom-player-image');
    const bottomPlayerTitle = document.getElementById('bottom-player-title');
    const bottomPlayerArtist = document.getElementById('bottom-player-artist');

    // Get the track information
    const trackImage = button.parentElement.querySelector('img').src;
    const trackTitle = button.parentElement.querySelector('span').innerText;

    // Check if the clicked track is already playing
    if (currentTrackElement === button) {
        if (isPlaying) {
            audioPlayer.pause();
            button.innerHTML = '<i class="fas fa-play fa-fw"></i>';
        } else {
            audioPlayer.play();
            button.innerHTML = '<i class="fas fa-pause fa-fw"></i>';
        }
        isPlaying = !isPlaying;
    } else {
        if (currentTrackElement) {
            // Reset the previous track button and remove highlight
            currentTrackElement.innerHTML = '<i class="fas fa-play fa-fw"></i>';
            currentTrackElement.parentElement.classList.remove('highlight');
        }

        // Set the new track
        currentTrackElement = button;
        audioPlayer.src = url;
        audioPlayer.play();
        button.innerHTML = '<i class="fas fa-pause fa-fw"></i>';
        isPlaying = true;

        // Highlight the current track
        button.parentElement.classList.add('highlight');

        // Update the queue and current index
        updateQueue(button);

        // Update the bottom player
        bottomPlayerImage.src = trackImage;
        bottomPlayerTitle.innerText = trackTitle;
        bottomPlayerArtist.innerText = ""; // Replace with actual artist name if available

        // Show the bottom player
        bottomPlayer.style.display = 'flex';
    }

    // Update play/pause button in the bottom player
    document.getElementById('play-pause-button').innerHTML = isPlaying ? '<i class="fas fa-pause fa-fw"></i>' : '<i class="fas fa-play fa-fw"></i>';

    // Event listener for when the track ends
    audioPlayer.onended = function() {
        nextTrack();
    };

    // Update the seek bar and duration
    audioPlayer.ontimeupdate = function() {
        const currentTime = audioPlayer.currentTime;
        const duration = audioPlayer.duration;
        document.getElementById('current-time').innerText = formatTime(currentTime);
        document.getElementById('total-duration').innerText = formatTime(duration);
        document.getElementById('seek-bar').value = (currentTime / duration) * 100;
    };

    // Seek bar event listener
    document.getElementById('seek-bar').oninput = function() {
        const seekTime = (audioPlayer.duration * document.getElementById('seek-bar').value) / 100;
        audioPlayer.currentTime = seekTime;
    };
}

// Update the queue based on the clicked button
function updateQueue(button) {
    const trackElements = document.querySelectorAll('.track');
    queue = Array.from(trackElements).map(el => ({
        url: el.dataset.url,
        button: el.querySelector('.play-button')
    }));
    currentIndex = queue.findIndex(track => track.button === button);
}

function nextTrack() {
    if (currentIndex < queue.length - 1) {
        currentIndex++;
        playTrack(queue[currentIndex].button, queue[currentIndex].url);
    } else {
        // Reset if at the end of the queue
        resetPlayer();
    }
}

function prevTrack() {
    if (currentIndex > 0) {
        currentIndex--;
        playTrack(queue[currentIndex].button, queue[currentIndex].url);
    }
}

function togglePlayPause() {
    const audioPlayer = document.getElementById('audio-player');
    if (isPlaying) {
        audioPlayer.pause();
        document.getElementById('play-pause-button').innerHTML = '<i class="fas fa-play fa-fw"></i>';
    } else {
        audioPlayer.play();
        document.getElementById('play-pause-button').innerHTML = '<i class="fas fa-pause fa-fw"></i>';
    }
    isPlaying = !isPlaying;
}

function resetPlayer() {
    if (currentTrackElement) {
        currentTrackElement.innerHTML = '<i class="fas fa-play fa-fw"></i>';
        currentTrackElement.parentElement.classList.remove('highlight');
    }
    currentTrackElement = null;
    isPlaying = false;
    currentIndex = -1;
    document.getElementById('audio-player').src = '';
    document.getElementById('play-pause-button').innerHTML = '<i class="fas fa-play fa-fw"></i>';
    document.getElementById('bottom-player').style.display = 'none';
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

// Optional: Add CSS for highlighting
const style = document.createElement('style');
style.innerHTML = `
    .highlight {
        border-radius: 5px;
        background-color: #323232;
    }
`;
document.head.appendChild(style);
