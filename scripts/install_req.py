#!/usr/bin/env python3
"""
Error-Resilient Package Installer for Voice Assistant
Installs packages one by one, collecting errors instead of crashing
"""

import subprocess
import sys
import time
from typing import List, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def install_package(package: str, extra_args: List[str] = None) -> Tuple[bool, str]:
    """
    Install a single package and return success status with error message
    """
    cmd = [sys.executable, "-m", "pip", "install"]
    
    if extra_args:
        cmd.extend(extra_args)
    
    cmd.append(package)
    
    try:
        print_colored(f"Installing {package}...", Colors.CYAN)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per package
        )
        
        if result.returncode == 0:
            print_colored(f"✓ {package} installed successfully", Colors.GREEN)
            return True, ""
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            print_colored(f"✗ {package} failed: {error_msg[:100]}...", Colors.RED)
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "Installation timeout (5 minutes exceeded)"
        print_colored(f"✗ {package} failed: {error_msg}", Colors.RED)
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        print_colored(f"✗ {package} failed: {error_msg}", Colors.RED)
        return False, error_msg

def main():
    """Main installation process"""
    print_colored("🎤 Voice Assistant Package Installer", Colors.BOLD + Colors.PURPLE)
    print_colored("=====================================", Colors.PURPLE)
    print_colored("This installer will attempt to install all packages individually", Colors.BLUE)
    print_colored("Errors will be collected and reported at the end\n", Colors.BLUE)
    
    # Package lists organized by priority
    essential_packages = [
        "pip --upgrade",
        "wheel",
        "setuptools",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0", 
        "requests>=2.31.0",
        "python-multipart>=0.0.6",
        "numpy>=1.21.0",
        "scipy>=1.10.0"
    ]
    
    pytorch_packages = [
        "--index-url https://download.pytorch.org/whl/nightly/cu129 torch>=2.9.0.dev",
        "--index-url https://download.pytorch.org/whl/nightly/cu129 torchvision>=0.24.0.dev",
        "--index-url https://download.pytorch.org/whl/nightly/cu129 torchaudio>=2.8.0.dev",
        "--index-url https://download.pytorch.org/whl/nightly/cu129 pytorch-triton>=3.4.0"
    ]
    
    tts_packages = [
        "coqui-tts>=0.27.0",
        "openai-whisper>=20231117",
        "transformers>=4.35.0",
        "accelerate>=0.24.0"
    ]
    
    audio_packages = [
        "pyaudio>=0.2.11",
        "webrtcvad>=2.0.10", 
        "openwakeword>=0.4.0",
        "soundfile>=0.12.0",
        "librosa>=0.10.0",
        "pydub>=0.25.0",
        "resampy>=0.4.0"
    ]
    
    optional_packages = [
        "jinja2>=3.1.2",
        "urllib3>=2.0.0",
        "pathlib2>=2.3.7",
        "json5>=0.9.0",
        "pyyaml>=6.0.0",
        "datasets>=2.14.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.17.0",
        "coloredlogs>=15.0.1",
        "tqdm>=4.66.0",
        "rich>=13.6.0",
        "psutil>=5.9.0",
        "platformdirs>=3.10.0",
        "memory-profiler>=0.61.0",
        "pympler>=0.9.0",
        "cryptography>=41.0.0",
        "pillow>=10.0.0",
        "python-magic>=0.4.27",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.4.0",
        "tenacity>=8.2.0"
    ]
    
    nvidia_packages = [
        "nvidia-ml-py>=12.535.0"
    ]
    
    advanced_packages = [
        "onnxruntime>=1.16.0",
        "tokenizers>=0.14.0",
        "optimum>=1.14.0",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.9.0",
        "flake8>=6.0.0"
    ]
    
    # Track installation results
    successful_installs = []
    failed_installs = []
    
    def install_package_list(packages: List[str], category: str):
        """Install a list of packages and track results"""
        print_colored(f"\n📦 Installing {category} packages...", Colors.BOLD + Colors.BLUE)
        print_colored("-" * 50, Colors.BLUE)
        
        for package_spec in packages:
            # Handle packages with extra pip arguments
            if package_spec.startswith("--"):
                parts = package_spec.split()
                extra_args = []
                package = ""
                
                for i, part in enumerate(parts):
                    if part.startswith("--"):
                        extra_args.append(part)
                        if i + 1 < len(parts) and not parts[i + 1].startswith("--"):
                            extra_args.append(parts[i + 1])
                    elif not any(part in arg for arg in extra_args):
                        package = part
                        break
                        
                success, error = install_package(package, extra_args)
            else:
                success, error = install_package(package_spec)
            
            if success:
                successful_installs.append(package_spec)
            else:
                failed_installs.append((package_spec, error))
            
            time.sleep(0.5)  # Brief pause between installations
    
    # Install packages in order of importance
    install_package_list(essential_packages, "Essential")
    install_package_list(pytorch_packages, "PyTorch (CUDA 12.9)")
    install_package_list(tts_packages, "TTS Engines")
    install_package_list(audio_packages, "Audio Processing")
    install_package_list(optional_packages, "Optional Features")
    install_package_list(nvidia_packages, "NVIDIA (may fail without GPU)")
    install_package_list(advanced_packages, "Advanced/Development")
    
    # Install Bark separately (requires git)
    print_colored("\n🐕 Installing Bark TTS (from git)...", Colors.BOLD + Colors.BLUE)
    print_colored("-" * 50, Colors.BLUE)
    
    bark_success, bark_error = install_package("git+https://github.com/suno-ai/bark.git")
    if bark_success:
        successful_installs.append("bark (from git)")
    else:
        failed_installs.append(("bark (from git)", bark_error))
    
    # Final report
    print_colored("\n" + "=" * 60, Colors.BOLD)
    print_colored("📊 INSTALLATION SUMMARY", Colors.BOLD + Colors.PURPLE)
    print_colored("=" * 60, Colors.BOLD)
    
    print_colored(f"\n✅ Successfully installed ({len(successful_installs)} packages):", Colors.GREEN)
    for package in successful_installs:
        print_colored(f"  ✓ {package}", Colors.GREEN)
    
    if failed_installs:
        print_colored(f"\n❌ Failed installations ({len(failed_installs)} packages):", Colors.RED)
        for package, error in failed_installs:
            print_colored(f"  ✗ {package}", Colors.RED)
            print_colored(f"    Error: {error[:100]}...", Colors.YELLOW)
    
    # Success rate
    total_packages = len(successful_installs) + len(failed_installs)
    success_rate = (len(successful_installs) / total_packages) * 100 if total_packages > 0 else 0
    
    print_colored(f"\n📈 Success Rate: {success_rate:.1f}% ({len(successful_installs)}/{total_packages})", Colors.BOLD + Colors.CYAN)
    
    # Recommendations
    print_colored("\n💡 RECOMMENDATIONS:", Colors.BOLD + Colors.YELLOW)
    
    if any("pyaudio" in pkg for pkg, _ in failed_installs):
        print_colored("  • PyAudio failed - install system audio libraries:", Colors.YELLOW)
        print_colored("    Arch: sudo pacman -S portaudio", Colors.WHITE)
        print_colored("    Ubuntu: sudo apt-get install portaudio19-dev", Colors.WHITE)
    
    if any("nvidia" in pkg.lower() for pkg, _ in failed_installs):
        print_colored("  • NVIDIA packages failed - normal without CUDA GPU", Colors.YELLOW)
    
    if any("torch" in pkg for pkg, _ in failed_installs):
        print_colored("  • PyTorch failed - try stable version:", Colors.YELLOW)
        print_colored("    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121", Colors.WHITE)
    
    if len(failed_installs) > total_packages * 0.3:
        print_colored("  • Many packages failed - check internet connection and Python version", Colors.YELLOW)
    
    essential_failed = [pkg for pkg, _ in failed_installs if any(essential in pkg for essential in ["fastapi", "uvicorn", "requests", "numpy", "scipy"])]
    if essential_failed:
        print_colored(f"  ⚠️  CRITICAL: Essential packages failed: {essential_failed}", Colors.RED)
        print_colored("    The voice assistant may not work without these!", Colors.RED)
    else:
        print_colored("  ✅ All essential packages installed - voice assistant should work!", Colors.GREEN)
    
    print_colored("\n🎤 Installation complete! Check the summary above for any issues.", Colors.BOLD + Colors.PURPLE)
    return len(failed_installs) == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Installation interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n💥 Unexpected error: {e}", Colors.RED)
        sys.exit(1)
