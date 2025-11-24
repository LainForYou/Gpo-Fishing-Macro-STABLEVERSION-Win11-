import os
import sys
import time
import json
import threading
import tkinter.messagebox as msgbox

class UpdateManager:
    def __init__(self, app):
        self.app = app
        self.repo_url = "https://api.github.com/repos/arielldev/gpo-fishing/commits/main"
        self.version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'installed_version.json')
        self.last_check = 0
        self.check_interval = 300  # 5 minutes
        self.pending_update = None
        
        # Initialize version tracking - this is the key to stopping nagging
        self.installed_commit = self._load_installed_version()
        if not self.installed_commit:
            self._mark_current_as_installed()

    def _load_installed_version(self):
        """Load the currently installed commit hash from JSON file"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    return data.get('commit_hash')
        except Exception as e:
            print(f"Error loading installed version: {e}")
        return None

    def _save_installed_version(self, commit_data):
        """Save commit data to JSON file - this prevents future nagging"""
        try:
            save_data = {
                'commit_hash': commit_data['sha'][:7],
                'full_hash': commit_data['sha'],
                'message': commit_data['commit']['message'].split('\n')[0],
                'date': commit_data['commit']['committer']['date'],
                'updated_at': time.time()
            }
            
            with open(self.version_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            self.installed_commit = save_data['commit_hash']
            print(f"✅ Marked version as installed: {save_data['commit_hash']} - {save_data['message']}")
            
        except Exception as e:
            print(f"Error saving installed version: {e}")

    def _mark_current_as_installed(self):
        """Mark the current latest commit as installed (stops all nagging)"""
        try:
            import requests
            response = requests.get(self.repo_url, timeout=10)
            if response.status_code == 200:
                commit_data = response.json()
                self._save_installed_version(commit_data)
                print("🔄 First run - marked current version as installed")
                return True
        except Exception as e:
            print(f"Error marking current as installed: {e}")
        return False

    def _is_new_version_available(self):
        """Check if there's actually a new version - the core anti-nagging logic"""
        try:
            import requests
            response = requests.get(self.repo_url, timeout=10)
            if response.status_code == 200:
                commit_data = response.json()
                latest_hash = commit_data['sha'][:7]
                
                # Only return True if it's genuinely different from what we have installed
                if self.installed_commit and latest_hash != self.installed_commit:
                    return commit_data
                    
        except Exception as e:
            print(f"Error checking for updates: {e}")
        return None

    def check_for_updates(self):
        """Main update check - only prompts if there's actually something new"""
        if self.app.main_loop_active:
            return
        
        current_time = time.time()
        if current_time - self.last_check < self.check_interval:
            return
        
        self.last_check = current_time
        
        new_commit = self._is_new_version_available()
        if new_commit:
            commit_hash = new_commit['sha'][:7]
            commit_message = new_commit['commit']['message'].split('\n')[0]
            self.app.root.after(0, lambda: self._prompt_update(commit_hash, commit_message, new_commit))
        else:
            self.app.root.after(0, lambda: self.app.update_status('Up to date!', 'success', '✅'))

    def _prompt_update(self, commit_hash, commit_message, commit_data):
        """Prompt user for update - includes option to skip and never ask again"""
        if self.app.main_loop_active:
            self.pending_update = {'hash': commit_hash, 'message': commit_message, 'data': commit_data}
            self.app.update_status('Update available - will prompt when fishing stops', 'info', '🔄')
            return
        
        message = f"New update available!\\n\\nCommit: {commit_hash}\\nChanges: {commit_message}\\n\\nChoose an option:"
        
        # Custom dialog with three options
        result = self._show_update_dialog(message, commit_hash, commit_message)
        
        if result == "update":
            self._download_and_install_update(commit_data)
        elif result == "skip_forever":
            # Mark this version as installed even though we didn't update
            # This stops all future nagging about this specific version
            self._save_installed_version(commit_data)
            self.app.update_status('Update skipped - won\'t ask again for this version', 'info', '⏭️')
        else:  # skip_once
            self.app.update_status('Update skipped', 'warning', '⏭️')

    def _show_update_dialog(self, message, commit_hash, commit_message):
        """Show custom update dialog with three options"""
        import tkinter as tk
        from tkinter import ttk
        
        result = {"choice": "skip_once"}
        
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Update Available")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Message
        msg_frame = ttk.Frame(dialog)
        msg_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(msg_frame, text=f"New update available!", font=("Arial", 12, "bold")).pack()
        ttk.Label(msg_frame, text=f"Commit: {commit_hash}").pack(pady=(10,0))
        ttk.Label(msg_frame, text=f"Changes: {commit_message}", wraplength=350).pack(pady=(5,0))
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", padx=20, pady=(0,20))
        
        def on_update():
            result["choice"] = "update"
            dialog.destroy()
        
        def on_skip_forever():
            result["choice"] = "skip_forever"
            dialog.destroy()
        
        def on_skip_once():
            result["choice"] = "skip_once"
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Update Now", command=on_update).pack(side="left", padx=(0,5))
        ttk.Button(btn_frame, text="Skip Forever", command=on_skip_forever).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Skip Once", command=on_skip_once).pack(side="left", padx=(5,0))
        
        dialog.wait_window()
        return result["choice"]

    def _download_and_install_update(self, commit_data):
        """Download and install the update"""
        try:
            import requests
            import zipfile
            import tempfile
            import shutil
            from datetime import datetime
            
            self.app.update_status('Downloading update...', 'info', '⬇️')
            
            # Download the zip
            zip_url = "https://github.com/arielldev/gpo-fishing/archive/refs/heads/main.zip"
            response = requests.get(zip_url, timeout=60)
            
            if response.status_code != 200:
                self.app.update_status('Download failed', 'error', '❌')
                return
            
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                
                # Save and extract
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find extracted folder
                extracted_folder = None
                for item in os.listdir(temp_dir):
                    if os.path.isdir(os.path.join(temp_dir, item)) and 'gpo-fishing' in item:
                        extracted_folder = os.path.join(temp_dir, item)
                        break
                
                if not extracted_folder:
                    self.app.update_status('Extraction failed', 'error', '❌')
                    return
                
                # Get project root
                project_root = os.path.dirname(os.path.dirname(__file__))
                
                # Create backup
                backup_dir = os.path.join(project_root, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(backup_dir, exist_ok=True)
                
                # Files to preserve
                preserve_files = ['default_settings.json', 'presets', '.git', '.gitignore', 'installed_version.json']
                
                # Backup current files
                for item in os.listdir(project_root):
                    if item.startswith('backup_'):
                        continue
                    src = os.path.join(project_root, item)
                    dst = os.path.join(backup_dir, item)
                    try:
                        if os.path.isdir(src):
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                    except:
                        pass
                
                self.app.update_status('Installing update...', 'info', '⚙️')
                
                # Copy new files (except preserved ones)
                for item in os.listdir(extracted_folder):
                    if item in preserve_files:
                        continue
                    
                    src = os.path.join(extracted_folder, item)
                    dst = os.path.join(project_root, item)
                    
                    try:
                        if os.path.exists(dst):
                            if os.path.isdir(dst):
                                shutil.rmtree(dst)
                            else:
                                os.remove(dst)
                        
                        if os.path.isdir(src):
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                    except Exception as e:
                        print(f"Error updating {item}: {e}")
                
                # Mark this version as installed - THIS IS KEY TO STOP NAGGING
                self._save_installed_version(commit_data)
                
                self.app.update_status('Update complete! Restarting...', 'success', '✅')
                self.app.root.after(2000, self._restart)
                
        except Exception as e:
            self.app.update_status(f'Update error: {str(e)[:30]}...', 'error', '❌')

    def _restart(self):
        """Restart the application"""
        try:
            import subprocess
            self.app.root.quit()
            self.app.root.destroy()
            
            if getattr(sys, 'frozen', False):
                subprocess.Popen([sys.executable])
            else:
                # Find the main script to restart
                main_script = None
                project_root = os.path.dirname(os.path.dirname(__file__))
                for file in ['main.py', 'app.py', 'run.py']:
                    if os.path.exists(os.path.join(project_root, file)):
                        main_script = os.path.join(project_root, file)
                        break
                
                if main_script:
                    subprocess.Popen([sys.executable, main_script])
                else:
                    subprocess.Popen([sys.executable, __file__])
            
            sys.exit(0)
            
        except Exception as e:
            print(f"Restart failed: {e}")
            sys.exit(1)

    def show_pending_update(self):
        """Show pending update that was delayed during fishing"""
        if not self.pending_update:
            return
        
        update_info = self.pending_update
        self._prompt_update(update_info['hash'], update_info['message'], update_info['data'])
        self.pending_update = None

    def startup_update_check(self):
        """Check for updates on startup"""
        if hasattr(self.app, 'auto_update_enabled') and self.app.auto_update_enabled and not self.app.main_loop_active:
            self.last_check = 0  # Force immediate check
            threading.Thread(target=self.check_for_updates, daemon=True).start()

    def start_auto_update_loop(self):
        """Start the auto-update checking loop"""
        if hasattr(self.app, 'auto_update_enabled') and self.app.auto_update_enabled and not self.app.main_loop_active:
            threading.Thread(target=self.check_for_updates, daemon=True).start()
        
        # Schedule next check
        if hasattr(self.app, 'auto_update_enabled') and self.app.auto_update_enabled:
            self.app.root.after(self.check_interval * 1000, self.start_auto_update_loop)