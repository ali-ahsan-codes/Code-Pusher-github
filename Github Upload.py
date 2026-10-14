import os
import shutil
import json
import zipfile
import subprocess
from urllib.parse import urlparse, unquote
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Git Clone & Push Local Manager with Project Structure Lister")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Clone & Push Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        darkbg: '#0f172a',
                        darkcard: '#1e293b',
                        accent: '#6366f1'
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-darkbg text-slate-100 min-h-screen font-sans antialiased">
    <div class="max-w-xl mx-auto p-6 space-y-6 mt-6">
        
        <!-- Header -->
        <div class="bg-darkcard border border-slate-800 p-5 rounded-2xl shadow-xl flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="bg-indigo-600 p-2.5 rounded-xl text-white shadow-lg shadow-indigo-500/30">
                    <i class="fa-solid fa-code-branch text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-base tracking-wide">Git Clone & Push Manager</h1>
                    <p class="text-xs text-slate-400">ZIP Upload &bull; Auto list.md Generation</p>
                </div>
            </div>
            <span id="conn-badge" class="px-3 py-1 text-xs rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30 font-medium">Not Connected</span>
        </div>

        <!-- Main Form Card -->
        <div class="bg-darkcard border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            
            <!-- Step 1: Credentials -->
            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">1. Upload cred.json (Username & Token)</label>
                <input type="file" id="cred-file" accept=".json" class="block w-full text-xs text-slate-400 file:mr-2 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer bg-slate-900 border border-slate-700 rounded-xl p-1.5" onchange="loadCred(event)">
            </div>

            <!-- Step 2: GitHub Folder Link -->
            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">2. GitHub Target Folder Link</label>
                <input type="text" id="github-url" placeholder="https://github.com/owner/repo/tree/branch/subfolder" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500">
            </div>

            <!-- Step 3: ZIP Archive Selection -->
            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">3. Select Project ZIP File</label>
                <input type="file" id="project-zip" accept=".zip" class="block w-full text-xs text-slate-400 file:mr-2 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer bg-slate-900 border border-slate-700 rounded-xl p-1.5" onchange="handleZipSelection(event)">
            </div>

            <div id="file-preview" class="text-[11px] text-slate-400 font-mono bg-slate-900/50 p-2 rounded-xl border border-slate-800 hidden"></div>

            <!-- Action Buttons -->
            <div class="flex items-center space-x-3 mt-4">
                <button onclick="startGitWorkflow()" id="push-btn" class="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white py-3 rounded-xl text-sm font-semibold shadow-lg shadow-emerald-600/30 transition flex items-center justify-center space-x-2">
                    <i class="fa-solid fa-play"></i>
                    <span>Start Git Push & Generate list.md</span>
                </button>
            </div>

            <!-- Terminal / Log Output -->
            <div class="space-y-1">
                <div class="flex justify-between text-xs text-slate-400">
                    <span id="status-title">Status: Idle</span>
                </div>
                <div id="status-box" class="bg-slate-950 border border-slate-800 rounded-xl p-3 font-mono text-[11px] text-slate-300 h-36 overflow-y-auto space-y-1 mt-2">
                    <div class="text-slate-500">[System] Ready...</div>
                </div>
            </div>

        </div>
    </div>

    <script>
        let credentials = null;
        let selectedZipFile = null;

        function log(msg, isError=false, isSuccess=false) {
            const box = document.getElementById('status-box');
            let color = 'text-slate-300';
            if (isError) color = 'text-rose-400';
            if (isSuccess) color = 'text-emerald-400';
            
            const time = new Date().toLocaleTimeString();
            box.innerHTML += `<div class="${color}">[${time}] ${msg}</div>`;
            box.scrollTop = box.scrollHeight;
        }

        function loadCred(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    credentials = JSON.parse(e.target.result);
                    if (!credentials.username || !credentials.token) throw new Error("Invalid cred.json");
                    document.getElementById('conn-badge').className = 'px-3 py-1 text-xs rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium';
                    document.getElementById('conn-badge').innerText = `Connected: ${credentials.username}`;
                    log(`Credentials loaded for ${credentials.username}`, false, true);
                } catch(err) {
                    log(`Error loading credentials: ${err.message}`, true);
                }
            };
            reader.readAsText(file);
        }

        function handleZipSelection(event) {
            const file = event.target.files[0];
            if (!file) return;
            selectedZipFile = file;
            const previewBox = document.getElementById('file-preview');
            previewBox.classList.remove('hidden');
            previewBox.innerHTML = `Selected ZIP: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            log(`ZIP file ready: ${file.name}`);
        }

        async function startGitWorkflow() {
            if (!credentials) {
                alert('Please upload cred.json first.');
                return;
            }
            const githubUrl = document.getElementById('github-url').value.trim();
            if (!githubUrl) {
                alert('Please enter GitHub Target Folder Link.');
                return;
            }
            if (!selectedZipFile) {
                alert('Please select a ZIP file.');
                return;
            }

            document.getElementById('status-title').innerText = 'Status: Extracting & Generating list.md...';
            log('Uploading ZIP, generating list.md and starting Git workflow...');

            const formData = new FormData();
            formData.append('username', credentials.username);
            formData.append('token', credentials.token);
            formData.append('github_url', githubUrl);
            formData.append('file', selectedZipFile);

            try {
                const response = await fetch('/api/git-push', {
                    method: 'POST',
                    body: formData
                });

                const rawText = await response.text();
                let resJson;
                try {
                    resJson = JSON.parse(rawText);
                } catch(e) {
                    throw new Error(rawText || "Server error occurred");
                }

                if (!response.ok) {
                    throw new Error(resJson.detail || 'Git push failed');
                }

                log(`✔ Successfully pushed files and list.md to GitHub!`, false, true);
                alert('Git push and list.md generation completed successfully!');
            } catch (err) {
                log(`❌ Error: ${err.message}`, true);
                alert(`Error: ${err.message}`);
            } finally {
                document.getElementById('status-title').innerText = 'Status: Idle';
            }
        }
    </script>
</body>
</html>
"""

def remove_readonly(func, path, excinfo):
    """Error handler for shutil.rmtree to handle Windows file locks (.git files)"""
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTML_CONTENT

@app.post("/api/git-push")
async def git_push_workflow(
    username: str = Form(...),
    token: str = Form(...),
    github_url: str = Form(...),
    file: UploadFile = File(...)
):
    # 1. Parse GitHub Link & decode percent-encodings
    decoded_url = unquote(github_url)
    parsed_url = urlparse(decoded_url)
    path_parts = [part for part in parsed_url.path.strip("/").split("/") if part]

    if len(path_parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid GitHub link provided. Could not extract owner and repo.")

    repo_owner = path_parts[0]
    repo_name = path_parts[1]
    target_branch = "main"
    target_folder_in_repo = ""

    if len(path_parts) > 2 and path_parts[2] == "tree":
        if len(path_parts) >= 4:
            target_branch = path_parts[3]
        if len(path_parts) > 4:
            target_folder_in_repo = "/".join(path_parts[4:])

    clone_dir = os.path.join(os.getcwd(), "temp_repo_clone")
    temp_zip_path = os.path.join(os.getcwd(), "temp_uploaded.zip")

    # Clean up existing dirs/files safely
    if os.path.exists(clone_dir):
        try:
            shutil.rmtree(clone_dir, onexc=remove_readonly)
        except Exception:
            pass
    if os.path.exists(temp_zip_path):
        try:
            os.remove(temp_zip_path)
        except Exception:
            pass

    try:
        # Save uploaded ZIP temporarily
        with open(temp_zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Clone repository
        clone_url = f"https://{username}:{token}@github.com/{repo_owner}/{repo_name}.git"
        print(f"Cloning repository '{repo_name}' (Branch: '{target_branch}')...")
        
        subprocess.run(
            ["git", "clone", "-b", target_branch, clone_url, clone_dir],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir, ignore_errors=True)
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        raise HTTPException(status_code=400, detail=f"Git Clone Failed: {e.stderr.strip()}")

    try:
        # 3. Extract ZIP directly into destination folder inside the clone
        dest_dir = os.path.join(clone_dir, target_folder_in_repo) if target_folder_in_repo else clone_dir
        os.makedirs(dest_dir, exist_ok=True)

        print(f"Extracting ZIP archive into {dest_dir}...")
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)

        # 4. Generate list.md project structure inside dest_dir
        print("Generating project structure list.md...")
        md_lines = [
            f"# Project Structure: {repo_name}",
            f"",
            f"Target Directory: `{target_folder_in_repo if target_folder_in_repo else 'Root'}`",
            f"",
            f"---",
            f""
        ]

        for root, dirs, files in os.walk(dest_dir):
            # Skip .git directory and temp files
            if ".git" in root:
                continue
            
            rel_path = os.path.relpath(root, dest_dir)
            if rel_path == ".":
                indent_level = 0
                folder_name = "📁 **Root Directory**"
            else:
                indent_level = rel_path.count(os.sep) + 1
                folder_name = f"📁 **{os.path.basename(root)}**"

            indent = "    " * indent_level
            md_lines.append(f"{indent}- {folder_name}")

            for f in sorted(files):
                if f == "list.md":
                    continue
                file_indent = "    " * (indent_level + 1)
                md_lines.append(f"{file_indent}- 📄 `{f}`")

        list_md_path = os.path.join(dest_dir, "list.md")
        with open(list_md_path, "w", encoding="utf-8") as md_file:
            md_file.write("\n".join(md_lines))

        # 5. Git Config, Add, Commit, Push
        os.chdir(clone_dir)
        subprocess.run(["git", "config", "user.name", username], check=True)
        subprocess.run(["git", "config", "user.email", f"{username}@users.noreply.github.com"], check=True)
        
        subprocess.run(["git", "add", "."], check=True)
        
        commit_msg = f"Upload files & generated list.md to {target_folder_in_repo if target_folder_in_repo else 'root'} via Local Git Manager"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        print("Pushing changes to GitHub...")
        push_res = subprocess.run(["git", "push", "origin", target_branch], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else e.stdout.strip()
        raise HTTPException(status_code=400, detail=f"Git Push Failed: {error_output}")
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Extraction/Git Error: {str(ex)}")
    finally:
        # Cleanup safely
        if os.path.exists(temp_zip_path):
            try:
                os.remove(temp_zip_path)
            except:
                pass
        
        os.chdir(os.path.dirname(clone_dir))
        if os.path.exists(clone_dir):
            try:
                shutil.rmtree(clone_dir, onexc=remove_readonly)
            except:
                pass

    return {"status": "success", "message": "ZIP extracted, list.md generated, and pushed via Git successfully!"}

if __name__ == "__main__":
    print("Starting Git Clone & Push Manager on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)