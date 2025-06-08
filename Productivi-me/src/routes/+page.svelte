<script lang="ts">
  import { invoke } from "@tauri-apps/api/core";
  import { onMount, onDestroy } from 'svelte';
  import { appWindow } from '@tauri-apps/api/window'; 
  
  // Stopwatch state
  let startTime: number | null = null;
  let elapsedTime: number = 0; // Stored in milliseconds
  let isRunning: boolean = false;
  let intervalId: number | undefined; 
  let displayTime: string = '00:00'; // The string to display in the UI

  // Function to update the display string
  function updateDisplay(): void {
    let currentElapsed = elapsedTime;
    if (isRunning && startTime !== null) {
      currentElapsed = Date.now() - startTime;
    }

    const totalSecs = Math.floor(currentElapsed / 1000);
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;

    displayTime = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  // Start function (now also called by onMount)
  function startStopwatch(): void {
    if (!isRunning) {
      startTime = Date.now() - elapsedTime; // Resume from elapsed
      isRunning = true;
      console.log('Stopwatch started.');
      // Start the interval to update the display
      intervalId = setInterval(updateDisplay, 100); // Update every 100ms
    }
  }

  // Stop function
  function stopStopwatch(): void {
    if (isRunning) {
      if (startTime !== null) { // Ensure startTime is not null before calculating
        elapsedTime = Date.now() - startTime;
      }
      isRunning = false;
      console.log('Stopwatch stopped at ' + displayTime); // Use current display time
      clearInterval(intervalId); // Stop the interval
      intervalId = undefined; // Clear the interval ID
    }
  }

  // Reset function (called by saveCurrentActivity now)
  function resetStopwatch(): void {
    stopStopwatch(); // Ensure it's stopped before resetting
    startTime = null;
    elapsedTime = 0;
    isRunning = false; // Explicitly set to false in case stop() wasn't called
    updateDisplay(); // Reset display to 00:00
    console.log('Stopwatch reset.');
  }

  // Modified save function: Now also resets the stopwatch after saving
  async function saveCurrentActivity(): Promise<void> {
    // If the stopwatch is currently running, stop it first to get the final elapsed time
    if (isRunning) {
        stopStopwatch();
    }
    
    // Only save if there's actual time on the stopwatch
    if (elapsedTime === 0) {
        console.warn("No activity duration to save.");
        // If it's already reset, no need to do anything else
        if (!isRunning && startTime === null) {
             console.log("Stopwatch already reset.");
        } else {
            resetStopwatch(); // Reset even if no time was recorded, to clear state
        }
        return; 
    }

    // You'd typically prompt the user for the skill title here,
    // e.g., using a Svelte input field and a confirmation dialog.
    const skillTitle = "Default Skill"; // Replace with actual input from user

    // Convert elapsedTime (milliseconds) to seconds for your backend
    const duration_seconds = Math.floor(elapsedTime / 1000);

    try {
      console.log("Attempting to save activity...");
      const response = await invoke("save_activity", { 
          durationSeconds: duration_seconds, 
          skillTitle: skillTitle 
      });
      console.log("Activity saved successfully:", response);
      
      // *** NEW BEHAVIOR: Reset stopwatch after successful save ***
      resetStopwatch(); 

    } catch (error) {
      console.error("Failed to save activity:", error);
      // You might want to notify the user about the save failure
      // And perhaps NOT reset the stopwatch if save failed, so data isn't lost
    }
  }

  // Logic for "Save on Quit" (via window close)
  let unlisten: Function | undefined; 

  onMount(() => {
    // *** NEW BEHAVIOR: Start stopwatch immediately on page load ***
    startStopwatch(); // This will auto-start the stopwatch

    // Initial display update
    updateDisplay(); 

    // Set up the listener for window close request
    unlisten = appWindow.onCloseRequested(async ({ preventDefault }) => {
      preventDefault(); // Prevent default close behavior

      console.log("Close requested. Attempting to save current activity...");
      await saveCurrentActivity(); // Calls the function which now also resets the stopwatch

      // After saving (or attempting to save), proceed to close the window
      appWindow.close(); 
    });
  });

  onDestroy(() => {
    if (intervalId !== undefined) {
      clearInterval(intervalId);
    }
    if (unlisten) {
      unlisten(); 
    }
  });
</script>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  h1 {
    font-size: 2rem;
    color: #333;
  }
  .stopwatch-display {
    font-size: 4rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: #007bff;
  }
  .controls button {
    margin: 5px;
    padding: 10px 20px;
    font-size: 1.2rem;
    cursor: pointer;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f0f0f0;
  }
  .controls button:hover {
    background-color: #e0e0e0;
  }
</style>

<main class="container">
  <h1>hi, welcome</h1>
  
  <div class="stopwatch-display">{displayTime}</div>

  <div class="controls">
    <button on:click={stopStopwatch}>Stop</button>
    <button on:click={saveCurrentActivity}>Save Activity</button> 
    </div>
</main>