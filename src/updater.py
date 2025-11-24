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
        self.update_check_failures = 0  # Track consecutive failures
        self.max_failures = 3  # Stop nagging after 3 consecutive failures
        
        # Initialize version tracking - this is the key to stopping nagging
        self.installed_commit = self._load_installed_version()
        
        if not self.installed_commit:
            print("⚠️ No installed version found - attempting to fetch current version...")
            if not self._mark_current_as_installed():
                # If we can't fetch current version, create a dummy one to prevent endless nagging
                print("⚠️ Could not fetch current version - creating placeholder to prevent update nagging")
                self._create_placeholder_version()

    def _load_installed_version(self):
        """Load the currently installed commit hash from JSON file with validation"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    commit_hash = data.get('commit_hash')
                    
                    # CRITICAL FIX: Validate the timestamp to detect corrupted data
                    updated_at = data.get('updated_at', 0)
                    current_time = time.time()
                    
                    # If timestamp is in the future or too old (>1 year), the data is corrupted
                    if updated_at > current_time + 86400:  # More than 1 day in future
                        print(f"⚠️ Corrupted version file detected (future timestamp: {updated_at})")
                        return None
                    
                    if commit_hash and len(commit_hash) >= 7:
                        print(f"✅ Loaded installed version: {commit_hash}")
                        return commit_hash
                    else:
                        print("⚠️ Invalid commit hash in version file")
                        return None
        except Exception as e:
            print(f"❌ Error loading installed version: {e}")
        return None

    def _save_installed_version(self, commit_data):
        """Save commit data to JSON file - this prevents future nagging"""
        try:
            # CRITICAL FIX: Validate commit data before saving
            if not commit_data or not commit_data.get('sha'):
                print("❌ Invalid commit data - cannot save version")
                return False
            
            save_data = {
                'commit_hash': commit_data['sha'][:7],
                'full_hash': commit_data['sha'],
                'message': commit_data['commit']['message'].split('\n')[0] if commit_data.get('commit', {}).get('message') else 'Unknown',
                'date': commit_data['commit']['committer']['date'] if commit_data.get('commit', {}).get('committer', {}).get('date') else time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'updated_at': time.time()
            }
            
            # Create backup of existing version file
            if os.path.exists(self.version_file):
                backup_file = self.version_file + '.backup'
                try:
                    import shutil
                    shutil.copy2(self.version_file, backup_file)
                except:
                    pass
            
            with open(self.version_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            self.installed_commit = save_data['commit_hash']
            print(f"✅ Marked version as installed: {save_data['commit_hash']} - {save_data['message']}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving installed version: {e}")
            return False

    def _mark_current_as_installed(self):
        """Mark the current latest commit as installed (stops all nagging)"""
        try:
            import requests
            print("🔄 Fetching latest version from GitHub...")
            response = requests.get(self.repo_url, timeout=15)
            
            if response.status_code == 200:
                commit_data = response.json()
                if self._save_installed_version(commit_data):
                    print("✅ Successfully marked current version as installed")
                    return True
                else:
                    print("❌ Failed to save version data")
                    return False
            else:
                print(f"❌ GitHub API returned status {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Timeout connecting to GitHub - network issue")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - check internet connection")
            return False
        except Exception as e:
            print(f"❌ Error marking current as installed: {e}")
            return False

    def _create_placeholder_version(self):
        """Create a placeholder version to prevent endless update nagging when offline"""
        try:
            placeholder_data = {
                'commit_hash': 'offline',
                'full_hash': 'offline_placeholder_to_prevent_update_nagging',
                'message': 'Offline placeholder - prevents update nagging',
                'date': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'updated_at': time.time()
            }
            
            with open(self.version_file, 'w') as f:
                json.dump(placeholder_data, f, indent=2)
            
            self.installed_commit = 'offline'
            print("✅ Created offline placeholder version to prevent update nagging")
            return True
            
        except Exception as e:
            print(f"❌ Error creating placeholder version: {e}")
            return False

    def _is_new_version_available(self):
        """Check if there's actually a new version - the core anti-nagging logic"""
        try:
            import requests
            
            # CRITICAL FIX: Don't check if we're offline or have too many failures
            if self.installed_commit == 'offline':
                print("📴 Offline mode - skipping update check")
                return None
                
            if self.update_check_failures >= self.max_failures:
                print(f"⚠️ Skipping update check - too many failures ({self.update_check_failures})")
                return None
            
            print("🔍 Checking for updates...")
            response = requests.get(self.repo_url, timeout=15)
            
            if response.status_code == 200:
                commit_data = response.json()
                latest_hash = commit_data['sha'][:7]
                
                print(f"📊 Current: {self.installed_commit} | Latest: {latest_hash}")
                
                # CRITICAL FIX: Only return True if it's genuinely different AND we have a valid installed version
                if self.installed_commit and latest_hash != self.installed_commit and self.installed_commit != 'offline':
                    print(f"🆕 New version available: {latest_hash}")
                    self.update_check_failures = 0  # Reset failure counter on success
                    return commit_data
                else:
                    print("✅ Already on latest version")
                    self.update_check_failures = 0  # Reset failure counter on success
                    return None
            else:
                print(f"❌ GitHub API error: {response.status_code}")
                self.update_check_failures += 1
                return None
                    
        except requests.exceptions.Timeout:
            print("❌ Update check timeout - network slow")
            self.update_check_failures += 1
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Update check failed - no internet connection")
            self.update_check_failures += 1
            return None
        except Exception as e:
            print(f"❌ Error checking for updates: {e}")
            self.update_check_failures += 1
            return None

    def check_for_updates(self):
        """Main update check - only prompts if there's actually something new"""
        # CRITICAL FIX: Don't check during fishing to avoid interruptions
        if self.app.main_loop_active:
            print("🎣 Skipping update check - fishing in progress")
            return
        
        current_time = time.time()
        if current_time - self.last_check < self.check_interval:
            print(f"⏰ Update check too soon - {int(self.check_interval - (current_time - self.last_check))}s remaining")
            return
        
        self.last_check = current_time
        
        # CRITICAL FIX: Proper error handling and user feedback
        try:
            new_commit = self._is_new_version_available()
            if new_commit:
                commit_hash = new_commit['sha'][:7]
                commit_message = new_commit['commit']['message'].split('\n')[0] if new_commit.get('commit', {}).get('message') else 'Unknown changes'
                print(f"🔔 Update available: {commit_hash} - {commit_message}")
                self.app.root.after(0, lambda: self._prompt_update(commit_hash, commit_message, new_commit))
            else:
                print("✅ No updates available")
                self.app.root.after(0, lambda: self.app.update_status('Up to date!', 'success', '✅'))
                
        except Exception as e:
            print(f"❌ Update check failed: {e}")
            self.app.root.after(0, lambda: self.app.update_status('Update check failed', 'error', '❌'))

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
        """Check for updates on startup with proper validation"""
        try:
            if hasattr(self.app, 'auto_update_enabled') and self.app.auto_update_enabled:
                if not self.app.main_loop_active:
                    print("🚀 Running startup update check...")
                    self.last_check = 0  # Force immediate check
                    threading.Thread(target=self.check_for_updates, daemon=True).start()
                else:
                    print("🎣 Skipping startup update check - fishing already active")
            else:
                print("📴 Auto-update disabled - skipping startup check")
        except Exception as e:
            print(f"❌ Error in startup update check: {e}")

    def start_auto_update_loop(self):
        """Start the auto-update checking loop with proper error handling"""
        try:
            # CRITICAL FIX: Only check if auto-update is enabled and not fishing
            if hasattr(self.app, 'auto_update_enabled') and self.app.auto_update_enabled:
                if not self.app.main_loop_active:
                    print("🔄 Running scheduled update check...")
                    threading.Thread(target=self.check_for_updates, daemon=True).start()
                else:
                    print("🎣 Skipping scheduled update check - fishing active")
                
                # CRITICAL FIX: Schedule next check with error handling
                try:
                    self.app.root.after(self.check_interval * 1000, self.start_auto_update_loop)
                except Exception as e:
                    print(f"❌ Error scheduling next update check: {e}")
            else:
                print("📴 Auto-update disabled - stopping loop")
                
        except Exception as e:
            print(f"❌ Error in auto-update loop: {e}")
            # Try to reschedule anyway to prevent complete failure
            try:
                self.app.root.after(self.check_interval * 1000, self.start_auto_update_loop)
            except:
                print("❌ Could not reschedule update loop")