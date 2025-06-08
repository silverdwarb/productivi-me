// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]


  
#[tauri::command]
async fn save_activity(duration_seconds: u64, skill_title: String) -> Result<String, String> {
    // Just print the received data and return success
    println!("Rust received save request: Duration: {}s, Skill: {}", duration_seconds, skill_title);
    Ok(format!("Successfully received: Duration {}s, Skill: '{}'", duration_seconds, skill_title))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_activity])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
