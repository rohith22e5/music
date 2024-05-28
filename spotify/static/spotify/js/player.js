
    let currentTrackElement = null;
    let isPlaying = false;
    
    function playTrack(button, url) {
        const audioPlayer = document.getElementById('audio-player');
    
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
        }
    
        // Event listener for when the track ends
        audioPlayer.onended = function() {
            button.innerHTML = '<i class="fas fa-play fa-fw"></i>';
            button.parentElement.classList.remove('highlight');
            isPlaying = false;
        };
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
    

